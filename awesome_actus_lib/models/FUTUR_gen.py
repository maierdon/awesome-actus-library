from datetime import datetime
from typing import Any, Optional, Union

from .contract_terms_generated import *
from .contractModel import ContractModel


class FUTUR(ContractModel):
    """ACTUS Contract Type: FUTUR

    Description:
    Keeps track of value changes for any basic CT as underlying (PAM, ANN etc. but also FXOUT, STK, COM). Handles margining calls.

    Real-world Instrument Examples (but not limited to):
    Standard interest rate, FX, stock and commodity futures.

    Required Terms:
    - contractDealDate
    - contractID
    - contractRole
    - contractStructure
    - contractType
    - counterpartyID
    - creatorID
    - currency
    - futuresPrice
    - maturityDate
    - priceAtPurchaseDate
    - purchaseDate
    - statusDate

    Conditional Groups:
    - Group 1
        * Drivers: initialMargin
        * Required if triggered: clearingHouse
        * Optional: maintenanceMarginLowerBound, maintenanceMarginUpperBound, cycleAnchorDateOfMargining, cycleOfMargining, variationMargin
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
    - 'contractType' is auto-set to "FUTUR" during initialization.
    """

    REQUIRED_TERMS = ['contractDealDate', 'contractID', 'contractRole', 'contractStructure', 'counterpartyID', 'creatorID', 'currency', 'futuresPrice', 'maturityDate', 'priceAtPurchaseDate', 'purchaseDate', 'statusDate']

    CONDITIONAL_GROUPS = {
    "1": {"drivers": ['initialMargin'], "required": ['clearingHouse'], "optional": ['maintenanceMarginLowerBound', 'maintenanceMarginUpperBound', 'cycleAnchorDateOfMargining', 'cycleOfMargining', 'variationMargin']},
    "6": {"drivers": ['terminationDate'], "required": ['priceAtTerminationDate'], "optional": []},
    "7": {"drivers": ['exerciseDate'], "required": ['exerciseAmount'], "optional": []}
    }

    def __init__(self,
        contractDealDate: Union[datetime, str],
        contractID: str,
        contractRole: str,
        contractStructure: Any,
        counterpartyID: str,
        creatorID: str,
        currency: str,
        futuresPrice: float,
        maturityDate: Union[datetime, str],
        priceAtPurchaseDate: float,
        purchaseDate: Union[datetime, str],
        statusDate: Union[datetime, str],
        businessDayConvention: Optional[str] = None,
        calendar: Optional[str] = None,
        clearingHouse: Optional[str] = None,
        contractPerformance: Optional[str] = None,
        cycleAnchorDateOfMargining: Optional[Union[datetime, str]] = None,
        cycleOfMargining: Optional[str] = None,
        delinquencyPeriod: Optional[str] = None,
        delinquencyRate: Optional[float] = None,
        deliverySettlement: Optional[str] = None,
        endOfMonthConvention: Optional[str] = None,
        exerciseAmount: Optional[float] = None,
        exerciseDate: Optional[Union[datetime, str]] = None,
        gracePeriod: Optional[str] = None,
        initialMargin: Optional[float] = None,
        maintenanceMarginLowerBound: Optional[float] = None,
        maintenanceMarginUpperBound: Optional[float] = None,
        marketObjectCode: Optional[str] = None,
        marketValueObserved: Optional[float] = None,
        nonPerformingDate: Optional[Union[datetime, str]] = None,
        priceAtTerminationDate: Optional[float] = None,
        seniority: Optional[str] = None,
        settlementCurrency: Optional[str] = None,
        settlementPeriod: Optional[str] = None,
        terminationDate: Optional[Union[datetime, str]] = None,
        variationMargin: Optional[float] = None,
        **other_terms):
        terms = {}
        builder = self.TermBuilder(terms)
        term_names = ['contractDealDate', 'contractID', 'contractRole', 'contractStructure', 'counterpartyID', 'creatorID', 'currency', 'futuresPrice', 'maturityDate', 'priceAtPurchaseDate', 'purchaseDate', 'statusDate', 'businessDayConvention', 'calendar', 'clearingHouse', 'contractPerformance', 'cycleAnchorDateOfMargining', 'cycleOfMargining', 'delinquencyPeriod', 'delinquencyRate', 'deliverySettlement', 'endOfMonthConvention', 'exerciseAmount', 'exerciseDate', 'gracePeriod', 'initialMargin', 'maintenanceMarginLowerBound', 'maintenanceMarginUpperBound', 'marketObjectCode', 'marketValueObserved', 'nonPerformingDate', 'priceAtTerminationDate', 'seniority', 'settlementCurrency', 'settlementPeriod', 'terminationDate', 'variationMargin']
        for name in term_names:
            builder.add(name, locals()[name])

        for term_name, value in other_terms.items():
            pascal_case = term_name[0].upper() + term_name[1:]
            term_class = globals().get(pascal_case)
            if term_class:
                terms[term_name] = term_class(value)
            else:
                terms[term_name] = UserDefinedTerm(termName=term_name, value=value)

        terms["contractType"] = ContractType("FUTUR")

        super().__init__(terms_dict=terms)
        self.check_time_consistency_rules()
        self.validate_terms()

    def validate_terms(self):

        # Validate Group 1
        if self.terms.get("initialMargin") is not None:
            missing = [t for t in ["clearingHouse"] if self.terms.get(t) is None]
            if missing:
                raise ValueError(f"Group 1: Missing required terms: {', '.join(missing)}")

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