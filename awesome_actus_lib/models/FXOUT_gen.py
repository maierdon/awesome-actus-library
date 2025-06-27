from datetime import datetime
from typing import Optional, Union

from .contract_terms_generated import *
from .contractModel import ContractModel


class FXOUT(ContractModel):
    """ACTUS Contract Type: FXOUT

    Description:
    Two parties agree to exchange two fixed cash flows in different currencies at a certain point in time in future.

    Real-world Instrument Examples (but not limited to):
    Any FX-outright transaction at a future date. This is also the underlying of FX-options and FX futures.

    Required Terms:
    - contractDealDate
    - contractID
    - contractRole
    - contractType
    - counterpartyID
    - creatorID
    - currency
    - currency2
    - maturityDate
    - notionalPrincipal
    - notionalPrincipal2
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
        * Drivers: exerciseDate
        * Required if triggered: exerciseAmount
        * Optional: None

    Standalone Optional Terms:
    - businessDayConvention
    - calendar
    - contractPerformance
    - delinquencyPeriod
    - delinquencyRate
    - deliverySettlement
    - endOfMonthConvention
    - gracePeriod
    - marketObjectCode
    - marketValueObserved
    - nonPerformingDate
    - seniority
    - settlementCurrency
    - settlementPeriod

    Note:
    - 'contractType' is auto-set to "FXOUT" during initialization.
    """

    REQUIRED_TERMS = ['contractDealDate', 'contractID', 'contractRole', 'counterpartyID', 'creatorID', 'currency', 'currency2', 'maturityDate', 'notionalPrincipal', 'notionalPrincipal2', 'statusDate']

    CONDITIONAL_GROUPS = {
    "5": {"drivers": ['purchaseDate'], "required": ['priceAtPurchaseDate'], "optional": []},
    "6": {"drivers": ['terminationDate'], "required": ['priceAtTerminationDate'], "optional": []},
    "7": {"drivers": ['exerciseDate'], "required": ['exerciseAmount'], "optional": []}
    }

    def __init__(self,
        contractDealDate: Union[datetime, str],
        contractID: str,
        contractRole: str,
        counterpartyID: str,
        creatorID: str,
        currency: str,
        currency2: str,
        maturityDate: Union[datetime, str],
        notionalPrincipal: float,
        notionalPrincipal2: float,
        statusDate: Union[datetime, str],
        businessDayConvention: Optional[str] = None,
        calendar: Optional[str] = None,
        contractPerformance: Optional[str] = None,
        delinquencyPeriod: Optional[str] = None,
        delinquencyRate: Optional[float] = None,
        deliverySettlement: Optional[str] = None,
        endOfMonthConvention: Optional[str] = None,
        exerciseAmount: Optional[float] = None,
        exerciseDate: Optional[Union[datetime, str]] = None,
        gracePeriod: Optional[str] = None,
        marketObjectCode: Optional[str] = None,
        marketValueObserved: Optional[float] = None,
        nonPerformingDate: Optional[Union[datetime, str]] = None,
        priceAtPurchaseDate: Optional[float] = None,
        priceAtTerminationDate: Optional[float] = None,
        purchaseDate: Optional[Union[datetime, str]] = None,
        seniority: Optional[str] = None,
        settlementCurrency: Optional[str] = None,
        settlementPeriod: Optional[str] = None,
        terminationDate: Optional[Union[datetime, str]] = None,
        **other_terms):
        terms = {}
        builder = self.TermBuilder(terms)
        term_names = ['contractDealDate', 'contractID', 'contractRole', 'counterpartyID', 'creatorID', 'currency', 'currency2', 'maturityDate', 'notionalPrincipal', 'notionalPrincipal2', 'statusDate', 'businessDayConvention', 'calendar', 'contractPerformance', 'delinquencyPeriod', 'delinquencyRate', 'deliverySettlement', 'endOfMonthConvention', 'exerciseAmount', 'exerciseDate', 'gracePeriod', 'marketObjectCode', 'marketValueObserved', 'nonPerformingDate', 'priceAtPurchaseDate', 'priceAtTerminationDate', 'purchaseDate', 'seniority', 'settlementCurrency', 'settlementPeriod', 'terminationDate']
        for name in term_names:
            builder.add(name, locals()[name])

        for term_name, value in other_terms.items():
            pascal_case = term_name[0].upper() + term_name[1:]
            term_class = globals().get(pascal_case)
            if term_class:
                terms[term_name] = term_class(value)
            else:
                terms[term_name] = UserDefinedTerm(termName=term_name, value=value)

        terms["contractType"] = ContractType("FXOUT")

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

        # Validate Group 7
        if self.terms.get("exerciseDate") is not None:
            missing = [t for t in ["exerciseAmount"] if self.terms.get(t) is None]
            if missing:
                raise ValueError(f"Group 7: Missing required terms: {', '.join(missing)}")