from logging import getLogger, NullHandler

from .models import Mission, FenceType
from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command

logger = getLogger("arductl")

def _setup_mission_waypoints(vehicle, waypoints):
    cmds = vehicle.commands
    
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

def _setup_mission_geofences(vehicle, geofences):
    for geofence in geofences:
        fence_type = geofence.fence_type
        vertice_count = len(geofence.vertices)
        for vertice in geofence.vertices:
            if fence_type == FenceType.INCLUSIVE:
                # MAV_CMD_NAV_FENCE_POLYGON_VERTEX_INCLUSION
                msg = vehicle.message_factory.mav_cmd_nav_fence_polygon_vertex_inclusion_encode(
                    vertice_count,
                    1,
                    0,
                    0,
                    vertice.lat,
                    vertice.lon,
                    0
                )
                vehicle.send_mavlink(msg)
            else:
                # MAV_CMD_NAV_FENCE_POLYGON_VERTEX_INCLUSION
                msg = vehicle.message_factory.mav_cmd_nav_fence_polygon_vertex_exclusion_encode(
                    vertice_count,
                    1,
                    0,
                    0,
                    vertice.lat,
                    vertice.lon,
                    0
                )
                vehicle.send_mavlink(msg)

    # Enable fence
    vechile.parameters['FENCE_ACTION'] = 2
    msg = vechile.message_factory.mav_cmd_do_fence_enable_encode(
        1, 0, 0, 0, 0, 0, 0
    )
    vehicle.send_mavlink(msg)
    pass

def _arm_and_takeoff(vehicle, aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    logger.info("Basic pre-arm checks")
    # Don't let the user try to arm until autopilot is ready
    while not vehicle.is_armable:
        logger.info(" Waiting for vehicle to initialise...")
        time.sleep(1)

    logger.info("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:      
        logger.info(" Waiting for arming...")
        time.sleep(1)

    logger.info("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        logger.info(" Altitude: ", vehicle.location.global_relative_frame.alt)      
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: #Trigger just below target alt.
            logger.info("Reached target altitude")
            break
        time.sleep(1)


def _distance_to_current_waypoint(vehicle):
    """
    Gets distance in metres to the current waypoint. 
    It returns None for the first waypoint (Home location).
    """
    nextwaypoint = vehicle.commands.next
    if nextwaypoint==0:
        return None
    missionitem=vehicle.commands[nextwaypoint-1] #commands are zero indexed
    lat = missionitem.x
    lon = missionitem.y
    alt = missionitem.z
    targetWaypointLocation = LocationGlobalRelative(lat,lon,alt)
    distancetopoint = get_distance_metres(vehicle.location.global_frame, targetWaypointLocation)
    return distancetopoint


def _commence_and_monitor_mission(vehicle, mission):
    # From Copter 3.3 you will be able to take off using a mission item. Plane must take off using a mission item (currently).
    _arm_and_takeoff(vehicle, 10)

    logger.info("Starting mission")
    # Reset mission set to first (0) waypoint
    vehicle.commands.next=0

    # Set mode to AUTO to start mission
    vehicle.mode = VehicleMode("AUTO")


    # Monitor mission. 
    # Demonstrates getting and setting the command number 
    # Uses distance_to_current_waypoint(), a convenience function for finding the 
    #   distance to the next waypoint.

    while True:
        nextwaypoint = vehicle.commands.next
        logger.info('Distance to waypoint (%s): %s' % (nextwaypoint, distance_to_current_waypoint()))
    
        if nextwaypoint == len(mission.waypoints): #Dummy waypoint - as soon as we reach waypoint 4 this is true and we exit.
            print("Exit 'standard' mission when start heading to final waypoint")
            break
        time.sleep(1)

    logger.info('Return to launch')
    vehicle.mode = VehicleMode("RTL")


def execute(mission: Mission, system_address: str, verbose: bool):
    logger.setLevel(INFO if verbose else WARN)

    drone = connect(system_address, wait_ready=True)
    _setup_mission_geofences(drone, mission.geofences)
    _setup_mission_waypoints(drone, mission.waypoints)
    _commence_and_monitor_mission(drone, mission)

    logger.info("Closing drone object; cleaning up")
    drone.close()
    
    

