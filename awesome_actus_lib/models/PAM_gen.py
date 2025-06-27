from datetime import datetime
from typing import Optional, Union

from .contract_terms_generated import *
from .contractModel import ContractModel


class PAM(ContractModel):
    """ACTUS Contract Type: PAM

    Description:
    Principal payment fully at Initial Exchange Date (IED) and repaid at Maturity Date (MD). Fixed and variable rates.

    Real-world Instrument Examples (but not limited to):
    All kind of bonds, term deposits, bullet loans and mortgages etc.

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
    - maturityDate
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
        * Drivers: cycleAnchorDateOfInterestPayment, cycleOfInterestPayment
        * Required if triggered: None
        * Optional: cyclePointOfInterestPayment
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
        * Drivers: cycleAnchorDateOfRateReset, cycleOfRateReset
        * Required if triggered: rateSpread, marketObjectCodeOfRateReset
        * Optional: lifeCap, lifeFloor, periodCap, periodFloor, cyclePointOfRateReset, fixingPeriod, nextResetRate, rateMultiplier

    Standalone Optional Terms:
    - accruedInterest
    - businessDayConvention
    - calendar
    - capitalizationEndDate
    - contractPerformance
    - creditLineAmount
    - delinquencyPeriod
    - delinquencyRate
    - endOfMonthConvention
    - gracePeriod
    - marketObjectCode
    - marketValueObserved
    - nonPerformingDate
    - premiumDiscountAtIED
    - seniority
    - settlementCurrency

    Note:
    - 'contractType' is auto-set to "PAM" during initialization.
    """

    REQUIRED_TERMS = ['contractDealDate', 'contractID', 'contractRole', 'counterpartyID', 'creatorID', 'currency', 'dayCountConvention', 'initialExchangeDate', 'maturityDate', 'nominalInterestRate', 'notionalPrincipal', 'statusDate']

    CONDITIONAL_GROUPS = {
    "8": {"drivers": ['prepaymentEffect'], "required": [], "optional": ['prepaymentPeriod', 'optionExerciseEndDate', 'cycleAnchorDateOfOptionality', 'cycleOfOptionality', 'penaltyType', 'penaltyRate']},
    "1": {"drivers": ['feeRate'], "required": ['feeBasis'], "optional": ['cycleAnchorDateOfFee', 'cycleOfFee', 'feeAccrued']},
    "2": {"drivers": ['cycleAnchorDateOfInterestPayment', 'cycleOfInterestPayment'], "required": [], "optional": ['cyclePointOfInterestPayment']},
    "5": {"drivers": ['purchaseDate'], "required": ['priceAtPurchaseDate'], "optional": []},
    "6": {"drivers": ['terminationDate'], "required": ['priceAtTerminationDate'], "optional": []},
    "7": {"drivers": ['scalingEffect'], "required": ['marketObjectCodeOfScalingIndex', 'scalingIndexAtContractDealDate', 'notionalScalingMultiplier', 'interestScalingMultiplier'], "optional": ['cycleAnchorDateOfScalingIndex', 'cycleOfScalingIndex']},
    "9": {"drivers": ['cycleAnchorDateOfRateReset', 'cycleOfRateReset'], "required": ['rateSpread', 'marketObjectCodeOfRateReset'], "optional": ['lifeCap', 'lifeFloor', 'periodCap', 'periodFloor', 'cyclePointOfRateReset', 'fixingPeriod', 'nextResetRate', 'rateMultiplier']}
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
        maturityDate: Union[datetime, str],
        nominalInterestRate: float,
        notionalPrincipal: float,
        statusDate: Union[datetime, str],
        accruedInterest: Optional[float] = None,
        businessDayConvention: Optional[str] = None,
        calendar: Optional[str] = None,
        capitalizationEndDate: Optional[Union[datetime, str]] = None,
        contractPerformance: Optional[str] = None,
        creditLineAmount: Optional[float] = None,
        cycleAnchorDateOfFee: Optional[Union[datetime, str]] = None,
        cycleAnchorDateOfInterestPayment: Optional[Union[datetime, str]] = None,
        cycleAnchorDateOfOptionality: Optional[Union[datetime, str]] = None,
        cycleAnchorDateOfRateReset: Optional[Union[datetime, str]] = None,
        cycleAnchorDateOfScalingIndex: Optional[Union[datetime, str]] = None,
        cycleOfFee: Optional[str] = None,
        cycleOfInterestPayment: Optional[str] = None,
        cycleOfOptionality: Optional[str] = None,
        cycleOfRateReset: Optional[str] = None,
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
        interestScalingMultiplier: Optional[float] = None,
        lifeCap: Optional[float] = None,
        lifeFloor: Optional[float] = None,
        marketObjectCode: Optional[str] = None,
        marketObjectCodeOfRateReset: Optional[str] = None,
        marketObjectCodeOfScalingIndex: Optional[str] = None,
        marketValueObserved: Optional[float] = None,
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
        rateSpread: Optional[float] = None,
        scalingEffect: Optional[str] = None,
        scalingIndexAtContractDealDate: Optional[float] = None,
        seniority: Optional[str] = None,
        settlementCurrency: Optional[str] = None,
        terminationDate: Optional[Union[datetime, str]] = None,
        **other_terms):
        terms = {}
        builder = self.TermBuilder(terms)
        term_names = ['contractDealDate', 'contractID', 'contractRole', 'counterpartyID', 'creatorID', 'currency', 'dayCountConvention', 'initialExchangeDate', 'maturityDate', 'nominalInterestRate', 'notionalPrincipal', 'statusDate', 'accruedInterest', 'businessDayConvention', 'calendar', 'capitalizationEndDate', 'contractPerformance', 'creditLineAmount', 'cycleAnchorDateOfFee', 'cycleAnchorDateOfInterestPayment', 'cycleAnchorDateOfOptionality', 'cycleAnchorDateOfRateReset', 'cycleAnchorDateOfScalingIndex', 'cycleOfFee', 'cycleOfInterestPayment', 'cycleOfOptionality', 'cycleOfRateReset', 'cycleOfScalingIndex', 'cyclePointOfInterestPayment', 'cyclePointOfRateReset', 'delinquencyPeriod', 'delinquencyRate', 'endOfMonthConvention', 'feeAccrued', 'feeBasis', 'feeRate', 'fixingPeriod', 'gracePeriod', 'interestScalingMultiplier', 'lifeCap', 'lifeFloor', 'marketObjectCode', 'marketObjectCodeOfRateReset', 'marketObjectCodeOfScalingIndex', 'marketValueObserved', 'nextResetRate', 'nonPerformingDate', 'notionalScalingMultiplier', 'optionExerciseEndDate', 'penaltyRate', 'penaltyType', 'periodCap', 'periodFloor', 'premiumDiscountAtIED', 'prepaymentEffect', 'prepaymentPeriod', 'priceAtPurchaseDate', 'priceAtTerminationDate', 'purchaseDate', 'rateMultiplier', 'rateSpread', 'scalingEffect', 'scalingIndexAtContractDealDate', 'seniority', 'settlementCurrency', 'terminationDate']
        for name in term_names:
            builder.add(name, locals()[name])

        for term_name, value in other_terms.items():
            pascal_case = term_name[0].upper() + term_name[1:]
            term_class = globals().get(pascal_case)
            if term_class:
                terms[term_name] = term_class(value)
            else:
                terms[term_name] = UserDefinedTerm(termName=term_name, value=value)

        terms["contractType"] = ContractType("PAM")

        super().__init__(terms_dict=terms)
        self.check_time_consistency_rules()
        self.validate_terms()

    def validate_terms(self):

        # Validate Group 1
        if self.terms.get("feeRate") is not None:
            missing = [t for t in ["feeBasis"] if self.terms.get(t) is None]
            if missing:
                raise ValueError(f"Group 1: Missing required terms: {', '.join(missing)}")

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
        if self.terms.get("cycleAnchorDateOfRateReset") is not None or self.terms.get("cycleOfRateReset") is not None:
            missing = [t for t in ["rateSpread", "marketObjectCodeOfRateReset"] if self.terms.get(t) is None]
            if missing:
                raise ValueError(f"Group 9: Missing required terms: {', '.join(missing)}")