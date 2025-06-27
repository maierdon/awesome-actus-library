from datetime import datetime
from typing import Any, Optional, Union

from .contract_terms_generated import *
from .contractModel import ContractModel


class SWAPS(ContractModel):
    """ACTUS Contract Type: SWAPS

    Description:
    Exchange of two basic CT´s (PAM, ANN etc.). Normally one is fixed, the other variable. However all variants possible including different currencies for cross currency swaps, basic swaps or even different principal exchange programs.

    Real-world Instrument Examples (but not limited to):
    All kind of swaps. The variety is defined by the underlying CT´s which often are PAM and ANN in all its flavors. With each new basic CT the variety rises.

    Required Terms:
    - contractDealDate
    - contractID
    - contractRole
    - contractStructure
    - contractType
    - counterpartyID
    - creatorID
    - currency
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

    Standalone Optional Terms:
    - contractPerformance
    - delinquencyPeriod
    - delinquencyRate
    - deliverySettlement
    - gracePeriod
    - marketObjectCode
    - marketValueObserved
    - nonPerformingDate
    - seniority
    - settlementCurrency

    Note:
    - 'contractType' is auto-set to "SWAPS" during initialization.
    """

    REQUIRED_TERMS = ['contractDealDate', 'contractID', 'contractRole', 'contractStructure', 'counterpartyID', 'creatorID', 'currency', 'statusDate']

    CONDITIONAL_GROUPS = {
    "5": {"drivers": ['purchaseDate'], "required": ['priceAtPurchaseDate'], "optional": []},
    "6": {"drivers": ['terminationDate'], "required": ['priceAtTerminationDate'], "optional": []}
    }

    def __init__(self,
        contractDealDate: Union[datetime, str],
        contractID: str,
        contractRole: str,
        contractStructure: Any,
        counterpartyID: str,
        creatorID: str,
        currency: str,
        statusDate: Union[datetime, str],
        contractPerformance: Optional[str] = None,
        delinquencyPeriod: Optional[str] = None,
        delinquencyRate: Optional[float] = None,
        deliverySettlement: Optional[str] = None,
        gracePeriod: Optional[str] = None,
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
        term_names = ['contractDealDate', 'contractID', 'contractRole', 'contractStructure', 'counterpartyID', 'creatorID', 'currency', 'statusDate', 'contractPerformance', 'delinquencyPeriod', 'delinquencyRate', 'deliverySettlement', 'gracePeriod', 'marketObjectCode', 'marketValueObserved', 'nonPerformingDate', 'priceAtPurchaseDate', 'priceAtTerminationDate', 'purchaseDate', 'seniority', 'settlementCurrency', 'terminationDate']
        for name in term_names:
            builder.add(name, locals()[name])

        for term_name, value in other_terms.items():
            pascal_case = term_name[0].upper() + term_name[1:]
            term_class = globals().get(pascal_case)
            if term_class:
                terms[term_name] = term_class(value)
            else:
                terms[term_name] = UserDefinedTerm(termName=term_name, value=value)

        terms["contractType"] = ContractType("SWAPS")

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