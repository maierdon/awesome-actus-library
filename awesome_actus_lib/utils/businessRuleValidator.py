import math

from awesome_actus_lib.utils.actus_applicability_rules_grouped import \
    APPLICABILITY_RULES
from awesome_actus_lib.utils.utils import get_long_name_for_acronym


class BusinessRuleValidator:
    def __init__(self):
        self.rules = APPLICABILITY_RULES

    def validate_dict(self, contract_data: dict) -> list[str]:
        """
        Validates a raw contract dictionary (e.g., from CSV, Excel, API).
        Ensures the contractType exists and checks business rules from applicability.
        """
        errors = []

        acronym = contract_data.get("contractType")
        if not acronym:
            return ["Missing 'contractType' (e.g., 'PAM', 'ANN') in input."]

        try:
            contract_type_key = get_long_name_for_acronym(acronym)
        except ValueError as e:
            return [str(e)]

        if contract_type_key not in self.rules:
            return [f"Unsupported contract type: {contract_type_key}"]

        ct_rules = self.rules[contract_type_key]

        # 1. Mandatory standalone terms
        for term in ct_rules["mandatory"]:
            if self._is_empty(contract_data.get(term)):
                errors.append(f"[{term}] is mandatory for CT={acronym} but not set.")

        # 2. Conditional groups
        for group_id, group in ct_rules["conditional_groups"].items():
            drivers_set = [t for t in group["drivers"] if not self._is_empty(contract_data.get(t))]

            if drivers_set:
                for term in group["required"]:
                    if self._is_empty(contract_data.get(term)):
                        errors.append(
                            f"[{term}] is required in group {group_id} when driver(s) {drivers_set} are set."
                        )
            else:
                for term in group["required"] + group["optional"]:
                    if not self._is_empty(contract_data.get(term)):
                        errors.append(
                            f"[{term}] should not be set in group {group_id} because no driver is set."
                        )

        return errors

    def _is_empty(self, value):
        return (
            value is None or 
            value == "" or 
            (isinstance(value, list) and len(value) == 0 ) or
            (isinstance(value, float) and math.isnan(value))
        )
