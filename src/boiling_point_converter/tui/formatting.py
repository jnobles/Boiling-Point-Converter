from boiling_point_converter.core.models import SolverMode

def format_output(
    mode: str | SolverMode,
    p1: float,
    t1: float,
    at_value: float,
    result: float,
    dh_vap: float,
) -> str:
    """Format the used values and estimated results for display.

    :param mode: The requested solver mode.
    :param p1: The reference pressure in torr.
    :param t1: The reference temperature in degrees Celsius.
    :param at_value: The target temperature or pressure, based on ``mode``.
    :param result: The estimated temperature or pressure, based on ``mode``.
    :param dh_vap: The molar heat of vaporization to use for the
        estimation, measured in kilojoules per mole.
    :returns: The formatted, multiline string.
    :raises ValueError: If ``mode`` is not a valid ``SolverMode``.
    """
    mode = SolverMode(mode.lower())
    if mode is SolverMode.PRESSURE:
        p2 = at_value
        t2 = result
    elif mode is SolverMode.TEMPERATURE:
        t2 = at_value
        p2 = result
    else:
        raise ValueError(f"Unhandled solver mode: {mode}")

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
