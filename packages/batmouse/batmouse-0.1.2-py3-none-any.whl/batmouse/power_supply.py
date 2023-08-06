"""Abstract type for power supplies."""
from enum import Enum

from typing_extensions import Protocol


class ChargingStatus(Enum):
    """Representation for a power supply's charging status."""

    DISCHARGING = 'discharging'
    CHARGING = 'charging'
    CHARGED = 'charged'


class PowerSupply(Protocol):  # pragma: no cover
    """Protocol for objects representing a power supply."""

    @property
    def model(self) -> str:
        """Get the model name."""
        ...

    @property
    def status(self) -> ChargingStatus:
        """Get the current supply status (discharging/charging/charged)."""
        ...

    @property
    def voltage(self) -> float:
        """Get the current voltage."""
        ...
