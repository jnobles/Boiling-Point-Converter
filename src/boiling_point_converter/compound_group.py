from dataclasses import dataclass


@dataclass(frozen=True)
class CompoundGroup:
    label: str
    dH_vap_kj_per_mole: float
