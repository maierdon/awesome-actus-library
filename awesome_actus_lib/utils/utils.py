from awesome_actus_lib.utils.contract_type_map import ACRONYM_TO_LONGNAME


def get_long_name_for_acronym(acronym: str) -> str:
    try:
        return ACRONYM_TO_LONGNAME[acronym]
    except KeyError:
        raise ValueError(f"Unknown contract type acronym: {acronym}")
