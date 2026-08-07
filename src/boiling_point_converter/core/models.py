from dataclasses import dataclass
from enum import StrEnum


class SolverMode(StrEnum):
    PRESSURE = "pressure"
    TEMPERATURE = "temperature"


@dataclass(frozen=True)
class MolarHeatOfVaporization:
    """A compound and its associated molar heat of vaporization.

    :param compound: The name of the compound.
    :param dh_vap_kj_per_mol: The molar heat of vaporization measure in kilojoules per
        mole.
    """

    compound: str
    dh_vap_kj_per_mol: float
