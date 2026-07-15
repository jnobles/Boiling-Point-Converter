"""Data structures and reference values for molar heat of vaporization.

Defines the :class:`MolarHeatOfVaporization` data model and provides a
reference collection of molar heats of vaporization for common compounds.

The included values are expressed in kilojoules per mole and are used as
reference values for Clausius-Clapeyron calculations.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class MolarHeatOfVaporization:
    """A compound and its associated molar heat of vaporization.

    :param compound: The name of the compound.
    :param dh_vap_kj_per_mol: The molar heat of vaporization measure in kilojoules per
        mole.
    """

    compound: str
    dh_vap_kj_per_mol: float


REFERENCE_HEATS_OF_VAPORIZATION = sorted(
    [
        MolarHeatOfVaporization(compound="acetic acid", dh_vap_kj_per_mol=37.16),
        MolarHeatOfVaporization(compound="ethyl acetate", dh_vap_kj_per_mol=32.30),
        MolarHeatOfVaporization(compound="diethyl ether", dh_vap_kj_per_mol=26.55),
        MolarHeatOfVaporization(compound="dichloromethane", dh_vap_kj_per_mol=27.95),
        MolarHeatOfVaporization(compound="acetone", dh_vap_kj_per_mol=29.12),
        MolarHeatOfVaporization(compound="ethanol", dh_vap_kj_per_mol=39.14),
        MolarHeatOfVaporization(compound="methanol", dh_vap_kj_per_mol=32.28),
        MolarHeatOfVaporization(compound="isopropanol", dh_vap_kj_per_mol=40.04),
        MolarHeatOfVaporization(compound="water", dh_vap_kj_per_mol=40.65),
        MolarHeatOfVaporization(compound="n-hexane", dh_vap_kj_per_mol=30.65),
        MolarHeatOfVaporization(compound="toluene", dh_vap_kj_per_mol=33.23),
        MolarHeatOfVaporization(compound="benzene", dh_vap_kj_per_mol=30.75),
        MolarHeatOfVaporization(compound="chloroform", dh_vap_kj_per_mol=29.37),
    ],
    key=lambda item: item.compound,
)
