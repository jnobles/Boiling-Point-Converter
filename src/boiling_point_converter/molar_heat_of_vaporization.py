from dataclasses import dataclass, field


@dataclass(frozen=True, order=True)
class MolarHeatOfVaporization:
    compound: str
    dH: float = field(compare=False)


DH_VAP_TABLE = [
    MolarHeatOfVaporization(compound="acetic acid", dH=37.16),
    MolarHeatOfVaporization(compound="ethyl acetate", dH=32.30),
    MolarHeatOfVaporization(compound="diethyl ether", dH=26.55),
    MolarHeatOfVaporization(compound="dichloromethane", dH=27.95),
    MolarHeatOfVaporization(compound="acetone", dH=29.12),
    MolarHeatOfVaporization(compound="ethanol", dH=39.14),
    MolarHeatOfVaporization(compound="methanol", dH=32.28),
    MolarHeatOfVaporization(compound="isopropanol", dH=40.04),
    MolarHeatOfVaporization(compound="water", dH=40.65),
    MolarHeatOfVaporization(compound="n-hexane", dH=30.65),
    MolarHeatOfVaporization(compound="toluene", dH=33.23),
    MolarHeatOfVaporization(compound="benzene", dH=30.75),
    MolarHeatOfVaporization(compound="chloroform", dH=29.37),
]

DH_VAP_TABLE = sorted(DH_VAP_TABLE)
