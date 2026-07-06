import math

from .constants import K, R


def calculate_temperature_at_pressure(
    pressure_torr: float,
    temperature_c: float,
    target_pressure_torr: float,
    dh_vap_kj_per_mol_k: float,
) -> float:
    dh_vap_j_per_mol_k = dh_vap_kj_per_mol_k * 1000
    temperature_k = temperature_c + K
    calculated_temperature_k = 1 / (
        (math.log(pressure_torr / target_pressure_torr) * (R / dh_vap_j_per_mol_k))
        + (1 / temperature_k)
    )
    calculated_temperature_c = calculated_temperature_k - K
    return calculated_temperature_c


def calculate_pressure_at_temperature(
    pressure_torr: float,
    temperature_c: float,
    target_temperature_c: float,
    dh_vap_kj_per_mol_k: float,
) -> float:
    dh_vap_j_per_mol_k = dh_vap_kj_per_mol_k * 1000
    temperature_k = temperature_c + K
    target_temperature_k = target_temperature_c + K
    calculated_pressure_torr = pressure_torr / (
        math.exp(
            (dh_vap_j_per_mol_k / R) * (1 / target_temperature_k - 1 / temperature_k)
        )
    )
    return calculated_pressure_torr


def format_output(p1: float, t1: float, p2: float, t2: float, dh_vap: float) -> str:
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
