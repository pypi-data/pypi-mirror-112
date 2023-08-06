"""Linux's /sys/power_supply PowerSupply representation."""
from dataclasses import dataclass
from pathlib import Path

from .power_supply import ChargingStatus


@dataclass(frozen=True)
class SysPowerSupply:  # pragma: no cover
    """Represent a power supply as on Linux's entries on /sys/class/power_supply."""

    power_supply_path: Path

    def _read_attribute(self, attribute: str) -> str:
        """Read an attribute from the power supply sys entry."""
        attribute_path = self.power_supply_path / attribute
        with attribute_path.open() as attribute_file:
            return attribute_file.read().strip()

    @property
    def model(self) -> str:
        """Get the model name."""
        return self._read_attribute('model_name')

    @property
    def status(self) -> ChargingStatus:
        """Get the current supply status (discharging/charging/charged)."""
        return ChargingStatus(self._read_attribute('status').lower())

    @property
    def voltage(self) -> float:
        """Get the current voltage."""
        return float(self._read_attribute('voltage_now'))
