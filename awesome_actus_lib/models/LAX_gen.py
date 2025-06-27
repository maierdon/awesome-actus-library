from datetime import datetime
from typing import Any, Optional, Union

from .contract_terms_generated import *
from .contractModel import ContractModel


class LAX(ContractModel):
    """ACTUS Contract Type: LAX

    Description:
    Exotic version of LAM. However step ups with respect to (i) Principal, (ii) Interest rates are possible. Highly flexible to match totally irregular principal payments. Principal can also be paid out in steps.

    Real-world Instrument Examples (but not limited to):
    A special version of this kind are teaser rate loans and mortgages.

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
    - nominalInterestRate
    - notionalPrincipal
    - statusDate

    Conditional Groups:
    - Group 8
        * Drivers: prepaymentEffect
        * Required if triggered: None
        * Optional: prepaymentPeriod, optionExerciseEndDate, cycleAnchorDateOfOptionality, cycleOfOptionality, penaltyType, penaltyRate
    - Group 1
        * Drivers: feeRate
        * Required if triggered: feeBasis
        * Optional: cycleAnchorDateOfFee, cycleOfFee, feeAccrued
    - Group 2
        * Drivers: arrayCycleAnchorDateOfInterestPayment, arrayCycleOfInterestPayment
        * Required if triggered: None
        * Optional: cyclePointOfInterestPayment
    - Group 3
        * Drivers: interestCalculationBase
        * Required if triggered: interestCalculationBaseAmount
        * Optional: cycleAnchorDateOfInterestCalculationBase, cycleOfInterestCalculationBase
    - Group 4
        * Drivers: arrayCycleAnchorDateOfPrincipalRedemption, arrayCycleOfPrincipalRedemption, arrayNextPrincipalRedemptionPayment, arrayIncreaseDecrease
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
    - Group 7
        * Drivers: scalingEffect
        * Required if triggered: marketObjectCodeOfScalingIndex, scalingIndexAtContractDealDate, notionalScalingMultiplier, interestScalingMultiplier
        * Optional: cycleAnchorDateOfScalingIndex, cycleOfScalingIndex
    - Group 9
        * Drivers: arrayCycleAnchorDateOfRateReset
        * Required if triggered: arrayRate, arrayFixedVariable, marketObjectCodeOfRateReset
        * Optional: arrayCycleOfRateReset, lifeCap, lifeFloor, periodCap, periodFloor, cyclePointOfRateReset, fixingPeriod, nextResetRate, rateMultiplier

    Standalone Optional Terms:
    - accruedInterest
    - businessDayConvention
    - calendar
    - capitalizationEndDate
    - contractPerformance
    - delinquencyPeriod
    - delinquencyRate
    - endOfMonthConvention
    - gracePeriod
    - marketObjectCode
    - marketValueObserved
    - maturityDate
    - nonPerformingDate
    - premiumDiscountAtIED
    - seniority
    - settlementCurrency

    Note:
    - 'contractType' is auto-set to "LAX" during initialization.
    """

    REQUIRED_TERMS = ['contractDealDate', 'contractID', 'contractRole', 'counterpartyID', 'creatorID', 'currency', 'dayCountConvention', 'initialExchangeDate', 'nominalInterestRate', 'notionalPrincipal', 'statusDate']

    CONDITIONAL_GROUPS = {
    "8": {"drivers": ['prepaymentEffect'], "required": [], "optional": ['prepaymentPeriod', 'optionExerciseEndDate', 'cycleAnchorDateOfOptionality', 'cycleOfOptionality', 'penaltyType', 'penaltyRate']},
    "1": {"drivers": ['feeRate'], "required": ['feeBasis'], "optional": ['cycleAnchorDateOfFee', 'cycleOfFee', 'feeAccrued']},
    "2": {"drivers": ['arrayCycleAnchorDateOfInterestPayment', 'arrayCycleOfInterestPayment'], "required": [], "optional": ['cyclePointOfInterestPayment']},
    "3": {"drivers": ['interestCalculationBase'], "required": ['interestCalculationBaseAmount'], "optional": ['cycleAnchorDateOfInterestCalculationBase', 'cycleOfInterestCalculationBase']},
    "4": {"drivers": ['arrayCycleAnchorDateOfPrincipalRedemption', 'arrayCycleOfPrincipalRedemption', 'arrayNextPrincipalRedemptionPayment', 'arrayIncreaseDecrease'], "required": [], "optional": []},
    "5": {"drivers": ['purchaseDate'], "required": ['priceAtPurchaseDate'], "optional": []},
    "6": {"drivers": ['terminationDate'], "required": ['priceAtTerminationDate'], "optional": []},
    "7": {"drivers": ['scalingEffect'], "required": ['marketObjectCodeOfScalingIndex', 'scalingIndexAtContractDealDate', 'notionalScalingMultiplier', 'interestScalingMultiplier'], "optional": ['cycleAnchorDateOfScalingIndex', 'cycleOfScalingIndex']},
    "9": {"drivers": ['arrayCycleAnchorDateOfRateReset'], "required": ['arrayRate', 'arrayFixedVariable', 'marketObjectCodeOfRateReset'], "optional": ['arrayCycleOfRateReset', 'lifeCap', 'lifeFloor', 'periodCap', 'periodFloor', 'cyclePointOfRateReset', 'fixingPeriod', 'nextResetRate', 'rateMultiplier']}
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
        nominalInterestRate: float,
        notionalPrincipal: float,
        statusDate: Union[datetime, str],
        accruedInterest: Optional[float] = None,
        arrayCycleAnchorDateOfInterestPayment: Optional[Any] = None,
        arrayCycleAnchorDateOfPrincipalRedemption: Optional[Any] = None,
        arrayCycleAnchorDateOfRateReset: Optional[Any] = None,
        arrayCycleOfInterestPayment: Optional[Any] = None,
        arrayCycleOfPrincipalRedemption: Optional[Any] = None,
        arrayCycleOfRateReset: Optional[Any] = None,
        arrayFixedVariable: Optional[Any] = None,
        arrayIncreaseDecrease: Optional[Any] = None,
        arrayNextPrincipalRedemptionPayment: Optional[Any] = None,
        arrayRate: Optional[Any] = None,
        businessDayConvention: Optional[str] = None,
        calendar: Optional[str] = None,
        capitalizationEndDate: Optional[Union[datetime, str]] = None,
        contractPerformance: Optional[str] = None,
        cycleAnchorDateOfFee: Optional[Union[datetime, str]] = None,
        cycleAnchorDateOfInterestCalculationBase: Optional[Union[datetime, str]] = None,
        cycleAnchorDateOfOptionality: Optional[Union[datetime, str]] = None,
        cycleAnchorDateOfScalingIndex: Optional[Union[datetime, str]] = None,
        cycleOfFee: Optional[str] = None,
        cycleOfInterestCalculationBase: Optional[str] = None,
        cycleOfOptionality: Optional[str] = None,
        cycleOfScalingIndex: Optional[str] = None,
        cyclePointOfInterestPayment: Optional[str] = None,
        cyclePointOfRateReset: Optional[str] = None,
        delinquencyPeriod: Optional[str] = None,
        delinquencyRate: Optional[float] = None,
        endOfMonthConvention: Optional[str] = None,
        feeAccrued: Optional[float] = None,
        feeBasis: Optional[str] = None,
        feeRate: Optional[float] = None,
        fixingPeriod: Optional[str] = None,
        gracePeriod: Optional[str] = None,
        interestCalculationBase: Optional[str] = None,
        interestCalculationBaseAmount: Optional[float] = None,
        interestScalingMultiplier: Optional[float] = None,
        lifeCap: Optional[float] = None,
        lifeFloor: Optional[float] = None,
        marketObjectCode: Optional[str] = None,
        marketObjectCodeOfRateReset: Optional[str] = None,
        marketObjectCodeOfScalingIndex: Optional[str] = None,
        marketValueObserved: Optional[float] = None,
        maturityDate: Optional[Union[datetime, str]] = None,
        nextResetRate: Optional[float] = None,
        nonPerformingDate: Optional[Union[datetime, str]] = None,
        notionalScalingMultiplier: Optional[float] = None,
        optionExerciseEndDate: Optional[Union[datetime, str]] = None,
        penaltyRate: Optional[float] = None,
        penaltyType: Optional[str] = None,
        periodCap: Optional[float] = None,
        periodFloor: Optional[float] = None,
        premiumDiscountAtIED: Optional[float] = None,
        prepaymentEffect: Optional[str] = None,
        prepaymentPeriod: Optional[str] = None,
        priceAtPurchaseDate: Optional[float] = None,
        priceAtTerminationDate: Optional[float] = None,
        purchaseDate: Optional[Union[datetime, str]] = None,
        rateMultiplier: Optional[float] = None,
        scalingEffect: Optional[str] = None,
        scalingIndexAtContractDealDate: Optional[float] = None,
        seniority: Optional[str] = None,
        settlementCurrency: Optional[str] = None,
        terminationDate: Optional[Union[datetime, str]] = None,
        **other_terms):
        terms = {}
        builder = self.TermBuilder(terms)
        term_names = ['contractDealDate', 'contractID', 'contractRole', 'counterpartyID', 'creatorID', 'currency', 'dayCountConvention', 'initialExchangeDate', 'nominalInterestRate', 'notionalPrincipal', 'statusDate', 'accruedInterest', 'arrayCycleAnchorDateOfInterestPayment', 'arrayCycleAnchorDateOfPrincipalRedemption', 'arrayCycleAnchorDateOfRateReset', 'arrayCycleOfInterestPayment', 'arrayCycleOfPrincipalRedemption', 'arrayCycleOfRateReset', 'arrayFixedVariable', 'arrayIncreaseDecrease', 'arrayNextPrincipalRedemptionPayment', 'arrayRate', 'businessDayConvention', 'calendar', 'capitalizationEndDate', 'contractPerformance', 'cycleAnchorDateOfFee', 'cycleAnchorDateOfInterestCalculationBase', 'cycleAnchorDateOfOptionality', 'cycleAnchorDateOfScalingIndex', 'cycleOfFee', 'cycleOfInterestCalculationBase', 'cycleOfOptionality', 'cycleOfScalingIndex', 'cyclePointOfInterestPayment', 'cyclePointOfRateReset', 'delinquencyPeriod', 'delinquencyRate', 'endOfMonthConvention', 'feeAccrued', 'feeBasis', 'feeRate', 'fixingPeriod', 'gracePeriod', 'interestCalculationBase', 'interestCalculationBaseAmount', 'interestScalingMultiplier', 'lifeCap', 'lifeFloor', 'marketObjectCode', 'marketObjectCodeOfRateReset', 'marketObjectCodeOfScalingIndex', 'marketValueObserved', 'maturityDate', 'nextResetRate', 'nonPerformingDate', 'notionalScalingMultiplier', 'optionExerciseEndDate', 'penaltyRate', 'penaltyType', 'periodCap', 'periodFloor', 'premiumDiscountAtIED', 'prepaymentEffect', 'prepaymentPeriod', 'priceAtPurchaseDate', 'priceAtTerminationDate', 'purchaseDate', 'rateMultiplier', 'scalingEffect', 'scalingIndexAtContractDealDate', 'seniority', 'settlementCurrency', 'terminationDate']
        for name in term_names:
            builder.add(name, locals()[name])

        for term_name, value in other_terms.items():
            pascal_case = term_name[0].upper() + term_name[1:]
            term_class = globals().get(pascal_case)
            if term_class:
                terms[term_name] = term_class(value)
            else:
                terms[term_name] = UserDefinedTerm(termName=term_name, value=value)

        terms["contractType"] = ContractType("LAX")

        super().__init__(terms_dict=terms)
        self.check_time_consistency_rules()
        self.validate_terms()

    def validate_terms(self):

        # Validate Group 1
        if self.terms.get("feeRate") is not None:
            missing = [t for t in ["feeBasis"] if self.terms.get(t) is None]
            if missing:
                raise ValueError(f"Group 1: Missing required terms: {', '.join(missing)}")

        # Validate Group 3
        if self.terms.get("interestCalculationBase") is not None:
            missing = [t for t in ["interestCalculationBaseAmount"] if self.terms.get(t) is None]
            if missing:
                raise ValueError(f"Group 3: Missing required terms: {', '.join(missing)}")

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
        if self.terms.get("scalingEffect") is not None:
            missing = [t for t in ["marketObjectCodeOfScalingIndex", "scalingIndexAtContractDealDate", "notionalScalingMultiplier", "interestScalingMultiplier"] if self.terms.get(t) is None]
            if missing:
                raise ValueError(f"Group 7: Missing required terms: {', '.join(missing)}")

        # Validate Group 9
        if self.terms.get("arrayCycleAnchorDateOfRateReset") is not None:
            missing = [t for t in ["arrayRate", "arrayFixedVariable", "marketObjectCodeOfRateReset"] if self.terms.get(t) is None]
            if missing:
                raise ValueError(f"Group 9: Missing required terms: {', '.join(missing)}")