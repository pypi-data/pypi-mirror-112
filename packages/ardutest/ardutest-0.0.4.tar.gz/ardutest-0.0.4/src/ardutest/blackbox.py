from __future__ import annotations

from asyncio import run
from csv import writer as csv_writer
from hashlib import md5
from pathlib import Path
from typing import Tuple, Callable, Optional

from numpy import ndarray, vstack
from arductl.stack import ArduStack
from arductl.models import ArduStackConfig, Mission, Waypoint
from arductl.storage import store_mission

from staliro.models import (
    blackbox,
    Blackbox,
    StaticParameters,
    SignalTimes,
    SignalValues,
    BlackboxResult,
)

from .config import ArduPilotTestConfig

MissionFactory = Callable[[ndarray, ndarray, ndarray], Mission]


def _default_factory(X: ndarray, *args: ndarray) -> Mission:
    waypoints = tuple(Waypoint(lat=X[i], lon=X[i + 1], alt=5) for i in range(0, X.size, 2))
    geofences = ()

    return Mission(waypoints=waypoints, geofences=geofences)


def _store_flight_trajectory(dest_path: Path, positions: ndarray, times: ndarray) -> None:
    with dest_path.open("w") as file:
        writer = csv_writer(file)
        writer.writerow(("t", "lat", "lon"))

        for i in range(positions.shape[0]):
            writer.writerow((times[i], positions[i][0], positions[i][1]))


def ardupilot_blackbox_factory(
    config: ArduPilotTestConfig,
    stack_config: ArduStackConfig,
    mission_factory: Optional[MissionFactory] = None,
) -> Blackbox:
    """Factory function to create ardupilot blackbox instances that have access to additional variables."""

    @blackbox()
    def ardupilot_blackbox(X: StaticParameters, T: SignalTimes, U: SignalValues) -> BlackboxResult:
        mission = mission_factory(X, T, U) if mission_factory is not None else _default_factory(X)
        mission_id = md5(X.tobytes()).hexdigest()
        ardustack = ArduStack(prefix=mission_id, config=stack_config)
        positions, timestamps = ardustack.execute(mission)

        if config.log_dest is not None:
            log_path = config.log_dest / f"{mission_id}.csv"
            _store_flight_trajectory(log_path, positions, timestamps)

        if config.mission_dest is not None:
            store_mission(mission, str(config.mission_dest / f"{mission_id}.json"))

        return positions, timestamps

    return ardupilot_blackbox
