from __future__ import annotations

from pathlib import Path
from logging import getLogger, NullHandler
from tempfile import TemporaryDirectory
from time import sleep
from types import TracebackType
from typing import Dict, Optional, TYPE_CHECKING

from docker import from_env as docker_client, DockerClient
from docker.models import containers, networks
from docker.errors import NotFound, ImageNotFound

from .config import ContainerImage, MavsdkContainerConfig, Px4ContainerConfig, Px4StackConfig
from .context import Px4StackContext

if TYPE_CHECKING:
    LogPath = TemporaryDirectory[str]

logger = getLogger("px4stack")
logger.addHandler(NullHandler())


class Px4StackError(Exception):
    pass


class ContainerFactoryError(Exception):
    pass


def _ensure_image(client: DockerClient, image: ContainerImage) -> None:
    try:
        client.images.get(str(image))
    except ImageNotFound:
        logger.info(f"Pulling image {image}")
        client.images.pull(image.name, image.tag)


class Px4ContainerFactory:
    def __init__(self, client: DockerClient, prefix: str, config: Px4ContainerConfig):
        self.client = client
        self.prefix = prefix
        self.config = config

    @property
    def container_name(self) -> str:
        return f"{self.prefix}_px4"

    @property
    def firmware_volumes(self) -> Dict[str, containers.VolumeConfig]:
        if self.config.firmware is None:
            return {}

        source_path = self.config.firmware.source_path.resolve()
        build_path = source_path / "build"

        if not build_path.is_dir():
            raise ContainerFactoryError("firmware must be compiled before execution")

        return {str(source_path): {"bind": str(self.config.firmware.mount_path), "mode": "rw"}}

    def create(self, network: networks.Network, log_dest: LogPath) -> containers.Container:
        logger.debug("Creating px4 container")

        _ensure_image(self.client, self.config.image)

        environment = {
            "PX4_SIM_SPEED_FACTOR": str(self.config.speed),
            "PX4_HOME_LAT": str(self.config.initial_position[0]),
            "PX4_HOME_LON": str(self.config.initial_position[1]),
        }

        volumes: Dict[str, containers.VolumeConfig] = {
            log_dest.name: {"bind": str(self.config.log_path), "mode": "rw"},
            **self.firmware_volumes,
        }

        return self.client.containers.create(
            str(self.config.image),
            command=self.config.command,
            network=network.name,
            environment=environment,
            volumes=volumes,
            name=self.container_name,
            tty=True,
            stdin_open=True,
        )


class MavsdkContainerFactory:
    def __init__(self, client: DockerClient, prefix: str, config: MavsdkContainerConfig):
        self.client = client
        self.prefix = prefix
        self.config = config

    @property
    def container_name(self) -> str:
        return f"{self.prefix}_mavsdk"

    @property
    def port_name(self) -> str:
        return f"{self.config.port}/tcp"

    def create(self, network: networks.Network, px4: containers.Container) -> containers.Container:
        logger.debug("Creating MAVSDK container")

        _ensure_image(self.client, self.config.image)

        return self.client.containers.create(
            str(self.config.image),
            command=self.config.command,
            network=network.name,
            links={px4.name: "px4"},
            ports={self.port_name: None},
            name=self.container_name,
            tty=True,
        )


def _start_stack(*stack: containers.Container) -> None:
    for container in stack:
        logger.debug(f"Starting container {container.name}")

        try:
            container.reload()
        except NotFound:
            raise Px4StackError(f"Could not find {container.name} to reload before starting")

        if container.status != "created":
            raise Px4StackError(f"container {container.name} has not been created")

        try:
            container.start()
        except NotFound:
            raise Px4StackError(f"Could not find {container.name} to start")


def _stop_stack(*stack: containers.Container) -> None:
    for container in stack:
        logger.debug(f"Stopping container {container.name}")

        try:
            container.reload()
        except NotFound:
            raise Px4StackError(f"Could not find {container.name} to reload before stopping")

        if container.status != "running":
            raise Px4StackError(f"container {container.name} is not running")

        try:
            container.kill()
        except NotFound:
            raise Px4StackError(f"Could not find {container.name} to kill")


def _cleanup_stack(*stack: containers.Container) -> None:
    for container in stack:
        logger.debug(f"Cleaning up container {container.name}")

        try:
            container.remove()
        except NotFound:
            pass


def _stack_ready(*stack: containers.Container) -> bool:
    def is_running(container: containers.Container) -> bool:
        try:
            container.reload()
        except NotFound:
            raise Px4StackError(f"Could not find {container.name} to reload to check status")

        return container.status == "running"

    return all(is_running(container) for container in stack)


class Px4Stack:
    def __init__(self, prefix: str, config: Px4StackConfig):
        client = docker_client()
        px4_factory = Px4ContainerFactory(client, prefix, config.px4)
        mavsdk_factory = MavsdkContainerFactory(client, prefix, config.mavsdk)

        self.config = config

        logger.debug("Creating temporary directory")
        self.log_dest = TemporaryDirectory(prefix=f"{prefix}_", suffix="_logs")

        logger.debug("Creating network")
        self.network = client.networks.create(f"{prefix}_net", driver="bridge")

        self.px4_container = px4_factory.create(self.network, self.log_dest)
        self.mavsdk_container = mavsdk_factory.create(self.network, self.px4_container)
        self.mavsdk_port_name = mavsdk_factory.port_name

    def start(self) -> Px4StackContext:
        _start_stack(self.px4_container, self.mavsdk_container)

        while not _stack_ready(self.px4_container, self.mavsdk_container):
            sleep(0.05)

        return Px4StackContext(
            self.network,
            self.px4_container,
            self.mavsdk_container,
            self.mavsdk_port_name,
            Path(self.log_dest.name),
        )

    def stop(self) -> None:
        _stop_stack(self.mavsdk_container, self.px4_container)

    def cleanup(self) -> None:
        containers = []

        if self.config.mavsdk.cleanup:
            containers.append(self.mavsdk_container)

        if self.config.px4.cleanup:
            containers.append(self.px4_container)

        _cleanup_stack(*containers)

        if self.config.network.cleanup:
            self.network.remove()

        self.log_dest.cleanup()

    def __enter__(self) -> Px4StackContext:
        return self.start()

    def __exit__(
        self, ex_type: Optional[Exception], value: object, traceback: TracebackType
    ) -> None:
        self.stop()

        if not isinstance(ex_type, Px4StackError):
            self.cleanup()
