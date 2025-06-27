from datetime import datetime
from typing import Optional, Union

from .contract_terms_generated import *
from .contractModel import ContractModel


class SWPPV(ContractModel):
    """ACTUS Contract Type: SWPPV

    Description:
    Plain vanilla swaps where the underlyings are always two identical PAM´s however with one leg fixed and the other variable.

    Real-world Instrument Examples (but not limited to):
    More than 90% of all interest rate swaps follow this simple pattern.

    Required Terms:
    - contractDealDate
    - contractID
    - contractRole
    - contractType
    - counterpartyID
    - creatorID
    - currency
    - dayCountConvention
    - initialExchangeDate
    - marketObjectCodeOfRateReset
    - maturityDate
    - nominalInterestRate
    - nominalInterestRate2
    - notionalPrincipal
    - rateSpread
    - statusDate

    Conditional Groups:
    - Group 2
        * Drivers: cycleAnchorDateOfInterestPayment, cycleOfInterestPayment
        * Required if triggered: None
        * Optional: None
    - Group 5
        * Drivers: purchaseDate
        * Required if triggered: priceAtPurchaseDate
        * Optional: None
    - Group 6
        * Drivers: terminationDate
        * Required if triggered: priceAtTerminationDate
        * Optional: None
    - Group 9
        * Drivers: None
        * Required if triggered: None
        * Optional: cycleAnchorDateOfRateReset, cycleOfRateReset, cyclePointOfRateReset, fixingPeriod, nextResetRate, rateMultiplier

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

    Note:
    - 'contractType' is auto-set to "SWPPV" during initialization.
    """

    REQUIRED_TERMS = ['contractDealDate', 'contractID', 'contractRole', 'counterpartyID', 'creatorID', 'currency', 'dayCountConvention', 'initialExchangeDate', 'marketObjectCodeOfRateReset', 'maturityDate', 'nominalInterestRate', 'nominalInterestRate2', 'notionalPrincipal', 'rateSpread', 'statusDate']

    CONDITIONAL_GROUPS = {
    "2": {"drivers": ['cycleAnchorDateOfInterestPayment', 'cycleOfInterestPayment'], "required": [], "optional": []},
    "5": {"drivers": ['purchaseDate'], "required": ['priceAtPurchaseDate'], "optional": []},
    "6": {"drivers": ['terminationDate'], "required": ['priceAtTerminationDate'], "optional": []},
    "9": {"drivers": [], "required": [], "optional": ['cycleAnchorDateOfRateReset', 'cycleOfRateReset', 'cyclePointOfRateReset', 'fixingPeriod', 'nextResetRate', 'rateMultiplier']}
    }

    def __init__(self,
        contractDealDate: Union[datetime, str],
        contractID: str,
        contractRole: str,
        counterpartyID: str,
        creatorID: str,
        currency: str,
        dayCountConvention: str,
        initialExchangeDate: Union[datetime, str],
        marketObjectCodeOfRateReset: str,
        maturityDate: Union[datetime, str],
        nominalInterestRate: float,
        nominalInterestRate2: float,
        notionalPrincipal: float,
        rateSpread: float,
        statusDate: Union[datetime, str],
        businessDayConvention: Optional[str] = None,
        calendar: Optional[str] = None,
        contractPerformance: Optional[str] = None,
        cycleAnchorDateOfInterestPayment: Optional[Union[datetime, str]] = None,
        cycleAnchorDateOfRateReset: Optional[Union[datetime, str]] = None,
        cycleOfInterestPayment: Optional[str] = None,
        cycleOfRateReset: Optional[str] = None,
        cyclePointOfRateReset: Optional[str] = None,
        delinquencyPeriod: Optional[str] = None,
        delinquencyRate: Optional[float] = None,
        deliverySettlement: Optional[str] = None,
        endOfMonthConvention: Optional[str] = None,
        fixingPeriod: Optional[str] = None,
        gracePeriod: Optional[str] = None,
        marketObjectCode: Optional[str] = None,
        marketValueObserved: Optional[float] = None,
        nextResetRate: Optional[float] = None,
        nonPerformingDate: Optional[Union[datetime, str]] = None,
        priceAtPurchaseDate: Optional[float] = None,
        priceAtTerminationDate: Optional[float] = None,
        purchaseDate: Optional[Union[datetime, str]] = None,
        rateMultiplier: Optional[float] = None,
        seniority: Optional[str] = None,
        settlementCurrency: Optional[str] = None,
        terminationDate: Optional[Union[datetime, str]] = None,
        **other_terms):
        terms = {}
        builder = self.TermBuilder(terms)
        term_names = ['contractDealDate', 'contractID', 'contractRole', 'counterpartyID', 'creatorID', 'currency', 'dayCountConvention', 'initialExchangeDate', 'marketObjectCodeOfRateReset', 'maturityDate', 'nominalInterestRate', 'nominalInterestRate2', 'notionalPrincipal', 'rateSpread', 'statusDate', 'businessDayConvention', 'calendar', 'contractPerformance', 'cycleAnchorDateOfInterestPayment', 'cycleAnchorDateOfRateReset', 'cycleOfInterestPayment', 'cycleOfRateReset', 'cyclePointOfRateReset', 'delinquencyPeriod', 'delinquencyRate', 'deliverySettlement', 'endOfMonthConvention', 'fixingPeriod', 'gracePeriod', 'marketObjectCode', 'marketValueObserved', 'nextResetRate', 'nonPerformingDate', 'priceAtPurchaseDate', 'priceAtTerminationDate', 'purchaseDate', 'rateMultiplier', 'seniority', 'settlementCurrency', 'terminationDate']
        for name in term_names:
            builder.add(name, locals()[name])

        for term_name, value in other_terms.items():
            pascal_case = term_name[0].upper() + term_name[1:]
            term_class = globals().get(pascal_case)
            if term_class:
                terms[term_name] = term_class(value)
            else:
                terms[term_name] = UserDefinedTerm(termName=term_name, value=value)

        terms["contractType"] = ContractType("SWPPV")

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