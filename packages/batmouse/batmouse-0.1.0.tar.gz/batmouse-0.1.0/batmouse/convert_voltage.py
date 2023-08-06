"""Conversion functions from voltages to battery percentages."""
from bisect import bisect

from .table import LOGITECH_G703_VOLTAGE_TABLE, VoltageTable


def convert_by_table(table: VoltageTable, voltage: float) -> float:
    """Convert a voltage to a battery percentage through a VoltageTable."""
    if voltage < table[0]:
        return 0.0

    if voltage >= table[-1]:
        return 100.0

    index = bisect(table, voltage)

    left_percentage = index - 1
    right_percentage = index

    left_voltage = table[left_percentage]
    right_voltage = table[right_percentage]

    voltage_diff = voltage - left_voltage
    voltage_span = right_voltage - left_voltage

    percentage_span = right_percentage - left_percentage
    percentage_factor = percentage_span / voltage_span

    percentage_diff = voltage_diff * percentage_factor

    return left_percentage + percentage_diff


def convert_logitech_g703(voltage: float) -> float:
    """Conversion function for Logitech G703."""
    return convert_by_table(LOGITECH_G703_VOLTAGE_TABLE, voltage)
