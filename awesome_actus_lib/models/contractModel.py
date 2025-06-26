from awesome_actus_lib.models.contract_terms_generated import *
from datetime import datetime
from abc import abstractmethod

class ContractModel:
    """
    Abstract base class for all contract types.
    Stores contract terms in a dictionary for fast access and easy serialization.
    """
    def __init__(self, terms_dict: dict):
        self.terms = terms_dict  # keys = termName (str), values = ContractTerm instances

    def get_term(self, term_name: str):
        """
        Retrieve a contract term by its name.
        """
        return self.terms.get(term_name)

    # def to_dict(self):
    #     """
    #     Convert contract terms to a serializable dictionary.
    #     Useful for JSON export.
    #     """
    #     return {
    #         term_name: term.value
    #         for term_name, term in self.terms.items()
    #     }
    def to_dict(self):
        """
        Convert contract terms to a JSON-serializable dictionary.
        - Primitives are converted to strings.
        - Lists and dicts are preserved as-is.
        """
        def stringify(value):
            if isinstance(value, (int, float, bool)):
                return str(value)
            return value  # leave str, list, dict, or None as-is

        return {
            term_name: stringify(term.value)
            for term_name, term in self.terms.items()
            if term.value is not None
        }


    def __repr__(self):
        return f"<{self.__class__.__name__} with terms: {list(self.terms.keys())}>"
    
    @abstractmethod
    def validate_terms(self):
        """
        Base placeholder method — override in subclasses.
        """
        pass

    def check_time_consistency_rules(self):
        def get_date(term):
            value = self.terms.get(term)
            if value and isinstance(value.value, str):
                try:
                    return datetime.fromisoformat(value.value.replace("Z", ""))
                except Exception:
                    pass
            return None

        t = {k: get_date(k) for k in self.terms}

        # Rule 1: CDD <= IED <= XX <= OPXED <= MD <= AMD <= STD
        rule1_chain = [
            ("contractDealDate", "initialExchangeDate"),
            *[(a, b) for a in ["initialExchangeDate"] for b in ["capitalizationEndDate", "cycleAnchorDateOfPrincipalRedemption", "terminationDate", "cycleAnchorDateOfRateReset", "cycleAnchorDateOfScalingIndex", "cycleAnchorDateOfOptionality"] if a in t and b in t],
            ("optionExerciseEndDate", "maturityDate"),
            ("maturityDate", "amortizationDate"),
            # ("amortizationDate", "settlementDate")  removed it was interpreted as statusDate when it should be settlementDate however no reference to a settlementDate found in ACTUS spec
            # ACTUS spec refers to STD as SettlementDays Sometimes it is called SettlementPeriod... very strange therefore ignore for now
        ]
        self._check_order(rule1_chain, "Rule 1")
        # print("I checked rule 1 (inside)")
        # Rule 2: IPANX < MD <= AMD
        self._check_order([("cycleAnchorDateOfInterestPayment", "maturityDate"),
                            ("maturityDate", "amortizationDate")], "Rule 2")

        # Rule 3: CDD <= SD <= XX (where XX are MD, STD, OPXED, TD)
        for xx in ["maturityDate", "optionExerciseEndDate", "terminationDate"]: #"statusDate" removed statusDate here since STD would be settlementDate but that is nonexisting
            if xx in t:
                self._check_order([("contractDealDate", "statusDate"),
                            ("statusDate", xx)], f"Rule 3 (via {xx})")

        # Rule 4: If DVNP defined and DVCL not defined, then DVANX > SD
        if "nextDividendPaymentAmount" in self.terms and "cycleOfDividend" not in self.terms:
            if not (t.get("cycleAnchorDateOfDividend") and t.get("statusDate") and t["cycleAnchorDateOfDividend"] > t["statusDate"]):
                print("⚠️ Rule 4 violated: cycleAnchorDateOfDividend should be > statusDate if nextDividendPaymentAmount is defined and cycleOfDividend is not.")

    def _check_order(self, term_pairs, rule_label):
        for a, b in term_pairs:
            if a in self.terms and b in self.terms:
                da = self.terms[a].value
                db = self.terms[b].value
                try:
                    da = datetime.fromisoformat(da.replace("Z", ""))
                    db = datetime.fromisoformat(db.replace("Z", ""))
                    if da > db:
                        print(f"⚠️ {rule_label} violated: '{a}' ({da}) should be <= '{b}' ({db})")
                except Exception:
                    pass

    class TermBuilder:
        def __init__(self, target_dict):
            self.terms = target_dict

        def add(self, name, value, default=None):
            if value is None and default is None:
                return
            effective_value = value if value is not None else default
            class_name = name[0].upper() + name[1:]
            term_class = globals().get(class_name)
            if term_class is None:
                raise ValueError(f"Unknown term class: {class_name}")
            self.terms[name] = term_class(effective_value)




