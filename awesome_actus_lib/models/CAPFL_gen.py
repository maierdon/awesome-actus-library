from datetime import datetime
from typing import Any, Optional, Union

from .contract_terms_generated import *
from .contractModel import ContractModel


class CAPFL(ContractModel):
    """ACTUS Contract Type: CAPFL

    Description:
    Interest rate option expressed in a maximum or minimum interest rate.

    Real-world Instrument Examples (but not limited to):
    Caps and Floor options.

    Required Terms:
    - contractDealDate
    - contractID
    - contractRole
    - contractStructure
    - contractType
    - counterpartyID
    - creatorID
    - statusDate

    Conditional Groups:
    - Group 5
        * Drivers: purchaseDate
        * Required if triggered: priceAtPurchaseDate
        * Optional: None
    - Group 6
        * Drivers: terminationDate
        * Required if triggered: priceAtTerminationDate
        * Optional: None
    - Group 7
        * Drivers: None
        * Required if triggered: None
        * Optional: lifeCap, lifeFloor

    Standalone Optional Terms:
    - contractPerformance
    - delinquencyPeriod
    - delinquencyRate
    - gracePeriod
    - marketObjectCode
    - marketValueObserved
    - nonPerformingDate
    - seniority
    - settlementCurrency

    Note:
    - 'contractType' is auto-set to "CAPFL" during initialization.
    """

    REQUIRED_TERMS = ['contractDealDate', 'contractID', 'contractRole', 'contractStructure', 'counterpartyID', 'creatorID', 'statusDate']

    CONDITIONAL_GROUPS = {
    "5": {"drivers": ['purchaseDate'], "required": ['priceAtPurchaseDate'], "optional": []},
    "6": {"drivers": ['terminationDate'], "required": ['priceAtTerminationDate'], "optional": []},
    "7": {"drivers": [], "required": [], "optional": ['lifeCap', 'lifeFloor']}
    }

    def __init__(self,
        contractDealDate: Union[datetime, str],
        contractID: str,
        contractRole: str,
        contractStructure: Any,
        counterpartyID: str,
        creatorID: str,
        statusDate: Union[datetime, str],
        contractPerformance: Optional[str] = None,
        delinquencyPeriod: Optional[str] = None,
        delinquencyRate: Optional[float] = None,
        gracePeriod: Optional[str] = None,
        lifeCap: Optional[float] = None,
        lifeFloor: Optional[float] = None,
        marketObjectCode: Optional[str] = None,
        marketValueObserved: Optional[float] = None,
        nonPerformingDate: Optional[Union[datetime, str]] = None,
        priceAtPurchaseDate: Optional[float] = None,
        priceAtTerminationDate: Optional[float] = None,
        purchaseDate: Optional[Union[datetime, str]] = None,
        seniority: Optional[str] = None,
        settlementCurrency: Optional[str] = None,
        terminationDate: Optional[Union[datetime, str]] = None,
        **other_terms):
        terms = {}
        builder = self.TermBuilder(terms)
        term_names = ['contractDealDate', 'contractID', 'contractRole', 'contractStructure', 'counterpartyID', 'creatorID', 'statusDate', 'contractPerformance', 'delinquencyPeriod', 'delinquencyRate', 'gracePeriod', 'lifeCap', 'lifeFloor', 'marketObjectCode', 'marketValueObserved', 'nonPerformingDate', 'priceAtPurchaseDate', 'priceAtTerminationDate', 'purchaseDate', 'seniority', 'settlementCurrency', 'terminationDate']
        for name in term_names:
            builder.add(name, locals()[name])

        for term_name, value in other_terms.items():
            pascal_case = term_name[0].upper() + term_name[1:]
            term_class = globals().get(pascal_case)
            if term_class:
                terms[term_name] = term_class(value)
            else:
                terms[term_name] = UserDefinedTerm(termName=term_name, value=value)

        terms["contractType"] = ContractType("CAPFL")

        super().__init__(terms_dict=terms)
        self.check_time_consistency_rules()
        self.validate_terms()

    def validate_terms(self):

        # Validate Group 5
        if self.terms.get("purchaseDate") is not None:
            missing = [t for t in ["priceAtPurchaseDate"] if self.terms.get(t) is None]
            if missing:
                raise ValueError(f"Group 5: Missing required terms: {', '.join(missing)}")

        # Validate Group 6
        if self.terms.get("terminationDate") is not None:
            missing = [t for t in ["priceAtTerminationDate"] if self.terms.get(t) is None]
            if missing:
                raise ValueError(f"Group 6: Missing required terms: {', '.join(missing)}")