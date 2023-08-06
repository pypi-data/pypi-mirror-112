from __future__ import annotations

from pathlib import Path
from importlib import metadata
from typing import Any, Optional, Tuple

from attr import attrs, attrib, Attribute
from attr.converters import optional

pkg_version = metadata.version("px4stack")
Position = Tuple[float, float]


@attrs(frozen=True)
class ContainerImage:
    name: str = attrib(converter=str)
    tag: str = attrib("latest", converter=str)

    def __str__(self) -> str:
        return f"{self.name}:{self.tag}"


def _image_converter(obj: Any) -> ContainerImage:
    if isinstance(obj, ContainerImage):
        return obj
    elif not isinstance(obj, str):
        raise ValueError(f"cannot convert {type(obj)} to ContainerImage")

    parts = obj.split(":")
    parts_len = len(parts)

    if parts_len > 2:
        raise ValueError("image string parse resulted in too many parts")

    return ContainerImage(*parts)


@attrs(frozen=True)
class Px4FirmwareConfig:
    """Configuration object to control PX4 firmware mounting.
    The source_path may be provided as relative and will be converted into an absolute path, but
    the the mount path must be provided as absolute.

    Attributes:
        source_path: Path to firmware on host machine
        mount_path: Path to mount firmware directory inside container
    """

    source_path: Path = attrib(Path("px4-autopilot"), converter=Path)
    mount_path: Path = attrib(Path("/src/firmware"), converter=Path)

    @source_path.validator
    def _validate_source_path(self, attr: Attribute[Path], source_path: Path) -> None:
        if not source_path.is_dir():
            raise ValueError("source path must be an existing directory")

    @mount_path.validator
    def _validate_mount_path(self, attr: Attribute[Path], mount_path: Path) -> None:
        if not mount_path.is_absolute():
            raise ValueError("mount path must be absolute")


def _firmware_config_converter(obj: Any) -> Px4FirmwareConfig:
    """Convert objects into Px4FirmwareConfig instances.

    Args:
        obj: Data to convert to Px4FirmwareConfig object

    Returns:
        config: The Px4FirmwareConfig object
    """

    if isinstance(obj, Px4FirmwareConfig):
        return obj
    elif isinstance(obj, dict):
        return Px4FirmwareConfig(**obj)
    elif isinstance(obj, (str, Path)):
        return Px4FirmwareConfig(obj, obj)
    else:
        raise ValueError(f"Cannot value type {type(obj)} to Px4FirmwareConfig")


def _position_converter(obj: Any) -> Position:
    return float(obj[0]), float(obj[1])


def _resolve_log_path(log_path: Path, config: Optional[Px4FirmwareConfig]) -> Path:
    if config is None:
        return Path("/") / log_path

    return config.mount_path / log_path


PX4_DEFAULT_IMAGE = ContainerImage("registry.gitlab.com/sbtg/px4stack/px4", pkg_version)


@attrs(frozen=True)
class Px4ContainerConfig:
    """Configuration object for PX4 container in stack.

    Attributes:
        image: The name of the docker image to use for the PX4 container
        command: The command to start the PX4 container
        firmware: Configuration object to control PX4 firmware mounting behavior
        log_path: Path to PX4 log directory in container
        speed: Speed factor of simulation
        initial_position: Initial lat, lon position of the drone
    """

    image: ContainerImage = attrib(PX4_DEFAULT_IMAGE, converter=_image_converter)
    command: Optional[str] = attrib(None, converter=optional(str))
    firmware: Optional[Px4FirmwareConfig] = attrib(
        factory=Px4FirmwareConfig, converter=optional(_firmware_config_converter)
    )
    log_path: Path = attrib(Path("build/px4_sitl_default/tmp/rootfs/log"), converter=Path)
    speed: float = attrib(1.0, converter=float)
    initial_position: Position = attrib((0, 0), converter=_position_converter)
    cleanup: bool = attrib(True)

    @speed.validator
    def _validate_speed(self, attr: Attribute[float], speed: float) -> None:
        if speed <= 0:
            raise ValueError("Speed must be greater than zero")

    @initial_position.validator
    def _validate_position(self, attr: Attribute[Position], position: Position) -> None:
        if position[0] < -90 or position[0] > 90:
            raise ValueError("initial_position[0] must be in range [-90, 90]")

        if position[1] < -180 or position[1] > 180:
            raise ValueError("initial_position[1] must be in range [-180, 180]")

    def __attrs_post_init__(self) -> None:
        if not self.log_path.is_absolute():
            object.__setattr__(self, "log_path", _resolve_log_path(self.log_path, self.firmware))


MAVSDK_DEFAULT_IMAGE = ContainerImage("registry.gitlab.com/sbtg/px4stack/mavsdk", pkg_version)


@attrs(frozen=True)
class MavsdkContainerConfig:
    """Configuration object for MAVSDK server container in stack.

    Attributes:
        image: The name of the image to use for the MAVSDK container
        command: The command to start the MAVSDK container
        port: Port of the MAVSDK container to bind to the host
    """

    image: ContainerImage = attrib(MAVSDK_DEFAULT_IMAGE, converter=_image_converter)
    command: Optional[str] = attrib(None, converter=optional(str))
    port: int = attrib(50051, converter=int)
    cleanup: bool = attrib(True)


@attrs(frozen=True)
class NetworkConfig:
    cleanup: bool = attrib(True)


@attrs(frozen=True)
class Px4StackConfig:
    """Configuration object for PX4 simulator stack.

    Attributes:
        px4: The PX4 container configuration object
        mavsdk: The MAVSDK container configuration object
    """

    px4: Px4ContainerConfig = attrib(factory=Px4ContainerConfig)
    mavsdk: MavsdkContainerConfig = attrib(factory=MavsdkContainerConfig)
    network: NetworkConfig = attrib(factory=NetworkConfig)
