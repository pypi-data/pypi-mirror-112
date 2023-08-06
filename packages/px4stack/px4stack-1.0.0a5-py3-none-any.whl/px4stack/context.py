from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from time import sleep

from docker.models import containers, networks
from docker.errors import NotFound


def _port_bound(container: containers.Container, name: str) -> bool:
    return len(container.ports.get(name, [])) > 0


def _port_binding(container: containers.Container, name: str, index: int) -> int:
    return int(container.ports[name][index]["HostPort"])


def _flight_log_path(logs_path: Path) -> Path:
    for subpath in logs_path.iterdir():
        if not subpath.is_dir():
            continue

        for file in subpath.iterdir():
            if file.suffix == ".ulg":
                return file

    raise RuntimeError(f"{logs_path} does not contain a flight log")


def _stack_running(*stack: containers.Container) -> bool:
    def is_running(container: containers.Container) -> bool:
        container.reload()
        return container.status == "running"

    return all(is_running(container) for container in stack)


@dataclass(frozen=True)
class Px4StackContext:
    _network: networks.Network
    _px4_container: containers.Container
    _mavsdk_container: containers.Container
    _port_name: str
    _log_path: Path

    @property
    def port(self) -> int:
        while not _port_bound(self._mavsdk_container, self._port_name):
            sleep(0.05)
            self._mavsdk_container.reload()

        return _port_binding(self._mavsdk_container, self._port_name, 0)

    @property
    def flight_log(self) -> Path:
        if not self._log_path.is_dir():
            raise RuntimeError(f"{self._log_path} is not a directory")

        return _flight_log_path(self._log_path)

    @property
    def running(self) -> bool:
        return _stack_running(self._px4_container, self._mavsdk_container)
