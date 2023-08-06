import json
from hashlib import md5
from pathlib import Path

from .models import Mission


def _checksum(obj: object) -> str:
    return md5(str(obj).encode("utf-8")).hexdigest()


def _mission_file_path(mission_name: str) -> Path:
    file_path = Path(mission_name)

    if file_path.suffix != ".json":
        return file_path.with_suffix(".json")

    return file_path



def store_mission(mission: Mission, mission_name: str) -> None:
    """Store a mission in a file.

    Generates a checksum of the mission to ensure mission is not modified when reloaded. If the provided filename does
    not end in a json extension, one will be added.

    Args:
        mission: Mission to store
        file_name: Name of the file to store the mission to
    """

    data = mission.dict()
    checksum = _checksum(data)
    file_path = _mission_file_path(mission_name)

    with file_path.open("w") as mission_file:
        json.dump({"mission": data, "checksum": checksum}, mission_file)

