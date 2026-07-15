"""Core utilities for the boiling point converter.

Provides utility functions for performing integrated Clausius-Clapeyron
calculations and formatting the displayed output.

The calculations assume ideal gas behavior in the vapor phase, negligible
liquid molar volume, and a constant molar heat of vaporization across the
temperature range.
"""

import math

from .constants import GAS_CONSTANT_J_PER_MOL_K, KELVIN_CELSIUS_OFFSET


def calculate_temperature_at_pressure(
    pressure_torr: float,
    temperature_c: float,
    target_pressure_torr: float,
    dh_vap_kj_per_mol: float,
) -> float:
    """Calculate the boiling point temperature at a target pressure.

    Uses the integrated Clausius-Clapeyron equation to estimate the
    new boiling point temperature at a target pressure.

    This is the inverse function of
    :func:`calculate_pressure_at_temperature`.

    :param pressure_torr: The reference pressure in torr.
    :param temperature_c: The reference temperature in degrees
        Celsius.
    :param target_pressure_torr: The target pressure in torr.
    :param dh_vap_kj_per_mol: The molar heat of vaporization of the
        reference substance, measured in kilojoules per mole Kelvin.
    :returns: The target temperature in degrees Celsius.
    """

    dh_vap_j_per_mol = dh_vap_kj_per_mol * 1000
    temperature_k = temperature_c + KELVIN_CELSIUS_OFFSET
    calculated_temperature_k = 1 / (
        (
            math.log(pressure_torr / target_pressure_torr)
            * (GAS_CONSTANT_J_PER_MOL_K / dh_vap_j_per_mol)
        )
        + (1 / temperature_k)
    )
    calculated_temperature_c = calculated_temperature_k - KELVIN_CELSIUS_OFFSET
    return calculated_temperature_c


def calculate_pressure_at_temperature(
    pressure_torr: float,
    temperature_c: float,
    target_temperature_c: float,
    dh_vap_kj_per_mol: float,
) -> float:
    """Calculate the pressure required for a target boiling point temperature.

    Uses the integrated Clausius-Clapeyron equation to estimate the
    pressure required to achieve a target boiling point temperature.

    This is the inverse function of :func:`calculate_temperature_at_pressure`.

    :param pressure_torr: The reference pressure in torr.
    :param temperature_c: The reference temperature in degrees
        Celsius.
    :param target_temperature_c: The target temperature in degrees
        Celsius.
    :param dh_vap_kj_per_mol: The molar heat of vaporization to use for
        the estimation, measures in kilojoules.
    :returns: The target pressure in torr.
    """

    dh_vap_j_per_mol = dh_vap_kj_per_mol * 1000
    temperature_k = temperature_c + KELVIN_CELSIUS_OFFSET
    target_temperature_k = target_temperature_c + KELVIN_CELSIUS_OFFSET
    calculated_pressure_torr = pressure_torr / (
        math.exp(
            (dh_vap_j_per_mol / GAS_CONSTANT_J_PER_MOL_K)
            * (1 / target_temperature_k - 1 / temperature_k)
        )
    )
    return calculated_pressure_torr


def format_output(p1: float, t1: float, p2: float, t2: float, dh_vap: float) -> str:
    """Perform multiline formatting of Clausius-Clapeyron relation values.

    :param p1: The reference pressure in torr.
    :param t1: The reference temperature in degrees Celsius.
    :param p2: The target pressure in torr.
    :param t2: The target temperature in degrees Celsius.
    :param dh_vap: The molar heat of vaporization to use for the estimate.
    :returns: A formatted multiline string suitable for application
        display.
    """

    lines = [
        f"Using Heat of Vaporization: {dh_vap} kJ/mol",
        "",
        f"Pressure: {p1:0.2f} torr",
        f"Boiling Point: {t1:0.2f} \u00b0C",
        "",
        "Equates to,",
        "",
        f"Pressure: {p2:0.2f} torr",
        f"Boiling Point: {t2:0.2f} \u00b0C",
    ]
    return "\n".join(lines)
