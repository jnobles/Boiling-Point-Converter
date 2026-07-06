from .compound_group import CompoundGroup

R = 8.3145  # J/(mol K)
K = 273.15

DH_VAP_TABLE = [
    CompoundGroup(
        label="ether, hexanes, carbon disulfide, methylene chloride",
        dH_vap_kj_per_mole=25,
    ),
    CompoundGroup(
        label="acetone, benzene, acetonitrile, bromine, chloroform, cyclohexane, ethyl acetate, triethylamine",  # noqa: E501
        dH_vap_kj_per_mole=30,
    ),
    CompoundGroup(
        label="dioxane, methanol, ethanol, nitric acid, nitromethane, pyridine, phosphorus oxychloride",  # noqa: E501
        dH_vap_kj_per_mole=37,
    ),
    CompoundGroup(
        label="water, butanoles, propaniles, aniline, toluene, bromoform, dimethylformamide",  # noqa: E501
        dH_vap_kj_per_mole=43,
    ),
    CompoundGroup(
        label="DMSO, nitrobenzene, octanoles, sulfuric acid", dH_vap_kj_per_mole=55
    ),
    CompoundGroup(label="mercury, formamide, glycol", dH_vap_kj_per_mole=60),
    CompoundGroup(
        label="high molecular or high boiling compounds", dH_vap_kj_per_mole=70
    ),
]
