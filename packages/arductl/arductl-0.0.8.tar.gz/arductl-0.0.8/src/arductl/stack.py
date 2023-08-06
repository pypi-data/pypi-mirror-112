import math
from logging import getLogger, NullHandler, INFO
import pprint
from pydantic import BaseModel
import time

from docker import from_env as docker_client, DockerClient
from docker.models import containers, networks
from docker.errors import NotFound, ImageNotFound
from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command, APIException
from numpy import array
import numpy as np
from pymavlink import mavutil

from .models import Mission, FenceType, Waypoint, ArduStackConfig

logger = getLogger("ardustack")
np.set_printoptions(suppress=True)
# logger.addHandler(NullHandler())

def _container_ready(container: containers.Container):
    try:
        container.reload()
    except NotFound as nf:
        return False
    
    return True


class ArduStack:
    def __init__(self, prefix: str, config: ArduStackConfig):
        logger.setLevel(INFO if config.verbose else WARN)

        self.config = config
        self.vehicle = None
        self.prefix = prefix
        self.t0 = None
        self.flight_log = []

    def _start_container(self, mission):
        home_location = mission.waypoints[0]
        docker_env = {
            'LAT': home_location.lat,
            'LON': home_location.lon,
            'ALT': 5,
            'SPEEDUP': self.config.simulation_speedup
        }

        client = docker_client()
        container = client.containers.run("ardupilot_master", 
                    remove=True, tty=True, ports={'5760/tcp': 5760}, 
                    name=self.prefix, environment=docker_env, detach=True)
        
        while not _container_ready(container):
            logger.info("Waiting for container to start")
            time.sleep(0.5)

        time.sleep(5)
        
        return container

    def _setup_mission_geofences(self, geofences):
        for geofence in geofences:
            fence_type = geofence.fence_type
            vertice_count = len(geofence.vertices)
            for vertice in geofence.vertices:
                if fence_type == FenceType.INCLUSIVE:
                    # MAV_CMD_NAV_FENCE_POLYGON_VERTEX_INCLUSION
                    msg = self.vehicle.message_factory.command_long_encode(
                        0, 0,
                        mavutil.mavlink.MAV_CMD_NAV_FENCE_POLYGON_VERTEX_INCLUSION, 0,
                        vertice_count,
                        1,
                        0,
                        0,
                        vertice.lat,
                        vertice.lon,
                        0
                    )
                    self.vehicle.send_mavlink(msg)
                else:
                    # MAV_CMD_NAV_FENCE_POLYGON_VERTEX_INCLUSION
                    msg = self.vehicle.message_factory.command_long_encode(
                        0, 0,
                        mavutil.mavlink.MAV_CMD_NAV_FENCE_POLYGON_VERTEX_INCLUSION, 0,
                        vertice_count,
                        1,
                        0,
                        0,
                        vertice.lat,
                        vertice.lon,
                        0
                    )
                    self.vehicle.send_mavlink(msg)

        # Enable fence
        self.vehicle.parameters['FENCE_ACTION'] = 2

        msg = self.vehicle.message_factory.command_long_encode(
            0, 0,
            mavutil.mavlink.MAV_CMD_DO_FENCE_ENABLE, 0,
            1, 0, 0, 0, 0, 0, 0
        )
        self.vehicle.send_mavlink(msg)

        return

    def _setup_mission_waypoints(self, waypoints):
        cmds = self.vehicle.commands
        
        logger.info("Clearing existing commands, starting clean")
        cmds.clear()

        logger.info("Adding new commands")

        # Take off command
        cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 0, 10))

        for waypoint in waypoints:
            cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, waypoint.lat, waypoint.lon, waypoint.alt))

        # dummy waypoint using the last wp for callback to destination
        cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, waypoint.lat, waypoint.lon, waypoint.alt))

        logger.info("Uploading commands")
        cmds.upload()

    def _arm_and_takeoff(self, aTargetAltitude):
        """
        Arms vehicle and fly to aTargetAltitude.
        """

        logger.info("Basic pre-arm checks")
        # Don't let the user try to arm until autopilot is ready
        while not self.vehicle.is_armable:
            logger.info(" Waiting for vehicle to initialise...")
            time.sleep(1)

        logger.info("Arming motors")
        # Copter should arm in GUIDED mode
        self.vehicle.mode = VehicleMode("GUIDED")
        self.vehicle.armed = True

        while not self.vehicle.armed:      
            logger.info(" Waiting for arming...")
            time.sleep(1)

        self.t0 = time.time()

        logger.info("Taking off!")
        self.vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

        # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
        #  after Vehicle.simple_takeoff will execute immediately).
        while True:
            logger.info(" Altitude: {}".format(self.vehicle.location.global_relative_frame.alt))      
            if self.vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: #Trigger just below target alt.
                logger.info("Reached target altitude")
                break
            time.sleep(1)

        return

    @staticmethod
    def get_distance_metres(aLocation1, aLocation2):
        """
        Returns the ground distance in metres between two LocationGlobal objects.

        This method is an approximation, and will not be accurate over large distances and close to the 
        earth's poles. It comes from the ArduPilot test code: 
        https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
        """
        dlat = aLocation2.lat - aLocation1.lat
        dlong = aLocation2.lon - aLocation1.lon
        return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5
    
    def _distance_to_current_waypoint(self):
        """
        Gets distance in metres to the current waypoint. 
        It returns None for the first waypoint (Home location).
        """
        nextwaypoint = self.vehicle.commands.next
        if nextwaypoint == 0:
            return None
        missionitem = self.vehicle.commands[nextwaypoint-1] #commands are zero indexed
        lat = missionitem.x
        lon = missionitem.y
        alt = missionitem.z
        targetWaypointLocation = LocationGlobalRelative(lat,lon,alt)
        distancetopoint = self.get_distance_metres(self.vehicle.location.global_frame, targetWaypointLocation)
        return distancetopoint
    
    def _commence_and_monitor_mission(self, mission):
        # From Copter 3.3 you will be able to take off using a mission item. Plane must take off using a mission item (currently).
        self._arm_and_takeoff(mission.waypoints[0].alt)

        logger.info("Starting mission")
        # Reset mission set to first (0) waypoint
        self.vehicle.commands.next = 0

        # Set mode to AUTO to start mission
        self.vehicle.mode = VehicleMode("AUTO")

        while True:
            nextwaypoint = self.vehicle.commands.next
            logger.info('Distance to waypoint (%s): %s' % (nextwaypoint, self._distance_to_current_waypoint()))
        
            if nextwaypoint == len(mission.waypoints) + 1: #Dummy waypoint - as soon as we reach waypoint 4 this is true and we exit.
                logger.info("Exit 'standard' mission when start heading to final waypoint")
                break
            time.sleep(1)

        logger.info('Return to launch')
        self.vehicle.mode = VehicleMode("RTL")

    def _location_callback(self, v, attr, msg):
        if self.t0 is not None:
            self.flight_log.append({'ts': time.time() - self.t0, 'lat': msg.lat, 'lon': msg.lon, 'alt': msg.alt})
        # logger.info("Location Callback: {}, {}, {}".format(msg.lat, msg.lon, msg.alt))

    def _read_flight_log(self):
        positions = []
        timestamps = []

        for log in self.flight_log:
            positions.append([log['lat'], log['lon']])
            timestamps.append(log['ts'])

        return array(positions), array(timestamps)

    def _close(self):
        if self.vehicle is not None:
            self.vehicle.close()
        self.container.stop()

    def execute(self, mission: Mission):
        retry_count = 0
        self.container = self._start_container(mission)

        print("Connecting to {}".format(self.config.connection_string))

        try:
            self.vehicle = connect(self.config.connection_string, wait_ready=True, heartbeat_timeout=60)
        except APIException as ae:
            print(ae)
            while retry_count < self.config.retries:
                print("Retrying {}".format(retry_count))
                self._close()
                time.sleep(5)
                self.container = self._start_container(mission)
                try:
                    self.vehicle = connect(self.config.connection_string, wait_ready=True, heartbeat_timeout=60)
                    print(self.vehicle)
                    break
                except APIException as ae1:
                    pass
                
                if self.vehicle is not None:
                    break
                retry_count += 1

        self.vehicle.add_attribute_listener('location.global_frame', self._location_callback)

        self._setup_mission_geofences(mission.geofences)
        self._setup_mission_waypoints(mission.waypoints)
        self._commence_and_monitor_mission(mission)
        logger.info("Closing drone object; cleaning up")
        self._close()
        positions, timestamps = self._read_flight_log()

        return positions, timestamps



# if __name__ == "__main__":
#     mission = Mission()

#     wp1 = Waypoint(lat=0.00044915764205976077, lon=-0.00044915764205976077)
#     wp2 = Waypoint(lat=0.00044915764205976077, lon=0.00044915764205976077)
#     wp3 = Waypoint(lat=-0.00044915764205976077, lon=0.00044915764205976077)
#     wp4 = Waypoint(lat=-0.00044915764205976077, lon=-0.00044915764205976077)

#     mission = mission.add_waypoint(wp1)
#     mission = mission.add_waypoint(wp2)
#     mission = mission.add_waypoint(wp3)
#     mission = mission.add_waypoint(wp4)

#     logger.info(mission.waypoints)

#     stack_config = ArduStackConfig(connection_string="tcp:127.0.0.1:5760", verbose=True, simulation_speedup=1)
#     ardustack = ArduStack(prefix="abcdefgh", config=stack_config)
#     ardustack.execute(mission)
