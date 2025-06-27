from datetime import datetime
from typing import Optional, Union

from .contract_terms_generated import *
from .contractModel import ContractModel


class STK(ContractModel):
    """ACTUS Contract Type: STK

    Description:
    Any instrument which is bought at a certain amount (market price normally) and then follows an index.

    Real-world Instrument Examples (but not limited to):
    All straight stocks.

    Required Terms:
    - contractDealDate
    - contractID
    - contractRole
    - contractType
    - counterpartyID
    - creatorID
    - currency
    - notionalPrincipal
    - priceAtPurchaseDate
    - purchaseDate
    - quantity
    - statusDate

    Conditional Groups:
    - Group 1
        * Drivers: cycleOfDividend, nextDividendPaymentAmount
        * Required if triggered: cycleAnchorDateOfDividend
        * Optional: exDividendDate
    - Group 6
        * Drivers: terminationDate
        * Required if triggered: priceAtTerminationDate
        * Optional: None

    Standalone Optional Terms:
    - businessDayConvention
    - calendar
    - contractPerformance
    - endOfMonthConvention
    - marketObjectCode
    - marketValueObserved
    - nonPerformingDate
    - seniority
    - settlementCurrency

    Note:
    - 'contractType' is auto-set to "STK" during initialization.
    """

    REQUIRED_TERMS = ['contractDealDate', 'contractID', 'contractRole', 'counterpartyID', 'creatorID', 'currency', 'notionalPrincipal', 'priceAtPurchaseDate', 'purchaseDate', 'quantity', 'statusDate']

    CONDITIONAL_GROUPS = {
    "1": {"drivers": ['cycleOfDividend', 'nextDividendPaymentAmount'], "required": ['cycleAnchorDateOfDividend'], "optional": ['exDividendDate']},
    "6": {"drivers": ['terminationDate'], "required": ['priceAtTerminationDate'], "optional": []}
    }

    def __init__(self,
        contractDealDate: Union[datetime, str],
        contractID: str,
        contractRole: str,
        counterpartyID: str,
        creatorID: str,
        currency: str,
        notionalPrincipal: float,
        priceAtPurchaseDate: float,
        purchaseDate: Union[datetime, str],
        quantity: float,
        statusDate: Union[datetime, str],
        businessDayConvention: Optional[str] = None,
        calendar: Optional[str] = None,
        contractPerformance: Optional[str] = None,
        cycleAnchorDateOfDividend: Optional[Union[datetime, str]] = None,
        cycleOfDividend: Optional[str] = None,
        endOfMonthConvention: Optional[str] = None,
        exDividendDate: Optional[Union[datetime, str]] = None,
        marketObjectCode: Optional[str] = None,
        marketValueObserved: Optional[float] = None,
        nextDividendPaymentAmount: Optional[float] = None,
        nonPerformingDate: Optional[Union[datetime, str]] = None,
        priceAtTerminationDate: Optional[float] = None,
        seniority: Optional[str] = None,
        settlementCurrency: Optional[str] = None,
        terminationDate: Optional[Union[datetime, str]] = None,
        **other_terms):
        terms = {}
        builder = self.TermBuilder(terms)
        term_names = ['contractDealDate', 'contractID', 'contractRole', 'counterpartyID', 'creatorID', 'currency', 'notionalPrincipal', 'priceAtPurchaseDate', 'purchaseDate', 'quantity', 'statusDate', 'businessDayConvention', 'calendar', 'contractPerformance', 'cycleAnchorDateOfDividend', 'cycleOfDividend', 'endOfMonthConvention', 'exDividendDate', 'marketObjectCode', 'marketValueObserved', 'nextDividendPaymentAmount', 'nonPerformingDate', 'priceAtTerminationDate', 'seniority', 'settlementCurrency', 'terminationDate']
        for name in term_names:
            builder.add(name, locals()[name])

        for term_name, value in other_terms.items():
            pascal_case = term_name[0].upper() + term_name[1:]
            term_class = globals().get(pascal_case)
            if term_class:
                terms[term_name] = term_class(value)
            else:
                terms[term_name] = UserDefinedTerm(termName=term_name, value=value)

        terms["contractType"] = ContractType("STK")

        super().__init__(terms_dict=terms)
        self.check_time_consistency_rules()
        self.validate_terms()

    def validate_terms(self):

        # Validate Group 1
        if self.terms.get("cycleOfDividend") is not None or self.terms.get("nextDividendPaymentAmount") is not None:
            missing = [t for t in ["cycleAnchorDateOfDividend"] if self.terms.get(t) is None]
            if missing:
                raise ValueError(f"Group 1: Missing required terms: {', '.join(missing)}")

        # Validate Group 6
        if self.terms.get("terminationDate") is not None:
            missing = [t for t in ["priceAtTerminationDate"] if self.terms.get(t) is None]
            if missing:
                raise ValueError(f"Group 6: Missing required terms: {', '.join(missing)}")