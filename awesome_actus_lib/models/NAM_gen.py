from datetime import datetime
from typing import Optional, Union

from .contract_terms_generated import *
from .contractModel import ContractModel


class NAM(ContractModel):
    """ACTUS Contract Type: NAM

    Description:
    Similar as ANN. However when resetting rate, total amount (interest plus principal) stay constant. MD shifts. Only variable rates.

    Real-world Instrument Examples (but not limited to):
    Special class of ARM´s (adjustable rate mortgages), Certain loans.

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
    - nextPrincipalRedemptionPayment
    - nominalInterestRate
    - notionalPrincipal
    - rateSpread
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
    - Group 3
        * Drivers: interestCalculationBase
        * Required if triggered: interestCalculationBaseAmount
        * Optional: cycleAnchorDateOfInterestCalculationBase, cycleOfInterestCalculationBase
    - Group 4
        * Drivers: None
        * Required if triggered: None
        * Optional: cycleAnchorDateOfPrincipalRedemption, cycleOfPrincipalRedemption
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
        * Drivers: None
        * Required if triggered: None
        * Optional: cycleAnchorDateOfRateReset, cycleOfRateReset, lifeCap, lifeFloor, periodCap, periodFloor, fixingPeriod, nextResetRate, rateMultiplier

    Standalone Optional Terms:
    - accruedInterest
    - businessDayConvention
    - calendar
    - capitalizationEndDate
    - contractPerformance
    - creditLineAmount
    - cycleAnchorDateOfInterestPayment
    - cycleOfInterestPayment
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
    - 'contractType' is auto-set to "NAM" during initialization.
    """

    REQUIRED_TERMS = ['contractDealDate', 'contractID', 'contractRole', 'counterpartyID', 'creatorID', 'currency', 'dayCountConvention', 'initialExchangeDate', 'marketObjectCodeOfRateReset', 'nextPrincipalRedemptionPayment', 'nominalInterestRate', 'notionalPrincipal', 'rateSpread', 'statusDate']

    CONDITIONAL_GROUPS = {
    "8": {"drivers": ['prepaymentEffect'], "required": [], "optional": ['prepaymentPeriod', 'optionExerciseEndDate', 'cycleAnchorDateOfOptionality', 'cycleOfOptionality', 'penaltyType', 'penaltyRate']},
    "1": {"drivers": ['feeRate'], "required": ['feeBasis'], "optional": ['cycleAnchorDateOfFee', 'cycleOfFee', 'feeAccrued']},
    "3": {"drivers": ['interestCalculationBase'], "required": ['interestCalculationBaseAmount'], "optional": ['cycleAnchorDateOfInterestCalculationBase', 'cycleOfInterestCalculationBase']},
    "4": {"drivers": [], "required": [], "optional": ['cycleAnchorDateOfPrincipalRedemption', 'cycleOfPrincipalRedemption']},
    "5": {"drivers": ['purchaseDate'], "required": ['priceAtPurchaseDate'], "optional": []},
    "6": {"drivers": ['terminationDate'], "required": ['priceAtTerminationDate'], "optional": []},
    "7": {"drivers": ['scalingEffect'], "required": ['marketObjectCodeOfScalingIndex', 'scalingIndexAtContractDealDate', 'notionalScalingMultiplier', 'interestScalingMultiplier'], "optional": ['cycleAnchorDateOfScalingIndex', 'cycleOfScalingIndex']},
    "9": {"drivers": [], "required": [], "optional": ['cycleAnchorDateOfRateReset', 'cycleOfRateReset', 'lifeCap', 'lifeFloor', 'periodCap', 'periodFloor', 'fixingPeriod', 'nextResetRate', 'rateMultiplier']}
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
        nextPrincipalRedemptionPayment: float,
        nominalInterestRate: float,
        notionalPrincipal: float,
        rateSpread: float,
        statusDate: Union[datetime, str],
        accruedInterest: Optional[float] = None,
        businessDayConvention: Optional[str] = None,
        calendar: Optional[str] = None,
        capitalizationEndDate: Optional[Union[datetime, str]] = None,
        contractPerformance: Optional[str] = None,
        creditLineAmount: Optional[float] = None,
        cycleAnchorDateOfFee: Optional[Union[datetime, str]] = None,
        cycleAnchorDateOfInterestCalculationBase: Optional[Union[datetime, str]] = None,
        cycleAnchorDateOfInterestPayment: Optional[Union[datetime, str]] = None,
        cycleAnchorDateOfOptionality: Optional[Union[datetime, str]] = None,
        cycleAnchorDateOfPrincipalRedemption: Optional[Union[datetime, str]] = None,
        cycleAnchorDateOfRateReset: Optional[Union[datetime, str]] = None,
        cycleAnchorDateOfScalingIndex: Optional[Union[datetime, str]] = None,
        cycleOfFee: Optional[str] = None,
        cycleOfInterestCalculationBase: Optional[str] = None,
        cycleOfInterestPayment: Optional[str] = None,
        cycleOfOptionality: Optional[str] = None,
        cycleOfPrincipalRedemption: Optional[str] = None,
        cycleOfRateReset: Optional[str] = None,
        cycleOfScalingIndex: Optional[str] = None,
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
        term_names = ['contractDealDate', 'contractID', 'contractRole', 'counterpartyID', 'creatorID', 'currency', 'dayCountConvention', 'initialExchangeDate', 'marketObjectCodeOfRateReset', 'nextPrincipalRedemptionPayment', 'nominalInterestRate', 'notionalPrincipal', 'rateSpread', 'statusDate', 'accruedInterest', 'businessDayConvention', 'calendar', 'capitalizationEndDate', 'contractPerformance', 'creditLineAmount', 'cycleAnchorDateOfFee', 'cycleAnchorDateOfInterestCalculationBase', 'cycleAnchorDateOfInterestPayment', 'cycleAnchorDateOfOptionality', 'cycleAnchorDateOfPrincipalRedemption', 'cycleAnchorDateOfRateReset', 'cycleAnchorDateOfScalingIndex', 'cycleOfFee', 'cycleOfInterestCalculationBase', 'cycleOfInterestPayment', 'cycleOfOptionality', 'cycleOfPrincipalRedemption', 'cycleOfRateReset', 'cycleOfScalingIndex', 'delinquencyPeriod', 'delinquencyRate', 'endOfMonthConvention', 'feeAccrued', 'feeBasis', 'feeRate', 'fixingPeriod', 'gracePeriod', 'interestCalculationBase', 'interestCalculationBaseAmount', 'interestScalingMultiplier', 'lifeCap', 'lifeFloor', 'marketObjectCode', 'marketObjectCodeOfScalingIndex', 'marketValueObserved', 'maturityDate', 'nextResetRate', 'nonPerformingDate', 'notionalScalingMultiplier', 'optionExerciseEndDate', 'penaltyRate', 'penaltyType', 'periodCap', 'periodFloor', 'premiumDiscountAtIED', 'prepaymentEffect', 'prepaymentPeriod', 'priceAtPurchaseDate', 'priceAtTerminationDate', 'purchaseDate', 'rateMultiplier', 'scalingEffect', 'scalingIndexAtContractDealDate', 'seniority', 'settlementCurrency', 'terminationDate']
        for name in term_names:
            builder.add(name, locals()[name])

        for term_name, value in other_terms.items():
            pascal_case = term_name[0].upper() + term_name[1:]
            term_class = globals().get(pascal_case)
            if term_class:
                terms[term_name] = term_class(value)
            else:
                terms[term_name] = UserDefinedTerm(termName=term_name, value=value)

        terms["contractType"] = ContractType("NAM")

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