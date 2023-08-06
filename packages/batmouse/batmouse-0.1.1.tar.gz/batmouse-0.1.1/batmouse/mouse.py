"""Implementation of a Mouse class for querying mouse battery data."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Optional

from .convert_voltage import convert_logitech_g703
from .power_supply import ChargingStatus, PowerSupply

PercentageConverter = Callable[[float], float]


CONVERTERS = {'G703 LIGHTSPEED Wireless Gaming Mouse w/ HERO': convert_logitech_g703}


@dataclass(frozen=True)
class Mouse:
    """Represent a mouse's battery ."""

    power_supply: PowerSupply
    model: str
    converter: Optional[PercentageConverter]

    @property
    def status(self) -> ChargingStatus:
        """Get the current mouse battery status (discharging/charging/charged)."""
        return self.power_supply.status

    @property
    def voltage(self) -> float:
        """Get the current mouse battery voltage."""
        return self.power_supply.voltage

    @property
    def percentage(self) -> float:
        """Get the current mouse battery percentage."""
        assert self.converter is not None
        return self.converter(self.voltage)

    @staticmethod
    def from_sys_power_supply(
        power_supply_path: Path,
    ) -> Optional[Mouse]:  # pragma: no cover
        """Try to create a Mouse object based on a power supply entry

        Args:
            power_supply_path: An entry on /sys/class/power_supply.

        Returns:
            A mouse object, if the model name read from /sys/class/power_supply
            has a known voltage-to-percentage conversion function.
        """
        from .sys_power_supply import SysPowerSupply

        power_supply = SysPowerSupply(power_supply_path)
        model = power_supply.model
        converter = CONVERTERS.get(model)

        if model not in CONVERTERS:
            return None

        return Mouse(power_supply, model, converter)


def get_sys_power_supply_mice() -> Iterable[Mouse]:  # pragma: no cover
    """Get Mouse objects from entries in /sys/class/power_supply."""
    for power_supply_path in Path('/sys/class/power_supply/').glob('*'):
        model_name_path = power_supply_path / 'model_name'
        if model_name_path.exists():
            mouse = Mouse.from_sys_power_supply(power_supply_path)
            if mouse is not None:
                yield mouse
