from datetime import datetime
from typing import Optional, Union

from .contract_terms_generated import *
from .contractModel import ContractModel


class CLM(ContractModel):
    """ACTUS Contract Type: CLM

    Description:
    Loans that are rolled over as long as they are not called. Once called it has to be paid back after the stipulated notice period.

    Real-world Instrument Examples (but not limited to):
    Interbank loans with call features.

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
    - xDayNotice

    Conditional Groups:
    - Group 1
        * Drivers: feeRate
        * Required if triggered: feeBasis
        * Optional: cycleAnchorDateOfFee, cycleOfFee, feeAccrued
    - Group 9
        * Drivers: cycleAnchorDateOfRateReset, cycleOfRateReset
        * Required if triggered: rateSpread, marketObjectCodeOfRateReset
        * Optional: fixingPeriod, nextResetRate, rateMultiplier

    Standalone Optional Terms:
    - accruedInterest
    - businessDayConvention
    - calendar
    - contractPerformance
    - cycleAnchorDateOfInterestPayment
    - cycleOfInterestPayment
    - delinquencyPeriod
    - delinquencyRate
    - endOfMonthConvention
    - gracePeriod
    - maturityDate
    - nonPerformingDate
    - prepaymentPeriod
    - seniority
    - settlementCurrency

    Note:
    - 'contractType' is auto-set to "CLM" during initialization.
    """

    REQUIRED_TERMS = ['contractDealDate', 'contractID', 'contractRole', 'counterpartyID', 'creatorID', 'currency', 'dayCountConvention', 'initialExchangeDate', 'nominalInterestRate', 'notionalPrincipal', 'statusDate', 'xDayNotice']

    CONDITIONAL_GROUPS = {
    "1": {"drivers": ['feeRate'], "required": ['feeBasis'], "optional": ['cycleAnchorDateOfFee', 'cycleOfFee', 'feeAccrued']},
    "9": {"drivers": ['cycleAnchorDateOfRateReset', 'cycleOfRateReset'], "required": ['rateSpread', 'marketObjectCodeOfRateReset'], "optional": ['fixingPeriod', 'nextResetRate', 'rateMultiplier']}
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
        xDayNotice: str,
        accruedInterest: Optional[float] = None,
        businessDayConvention: Optional[str] = None,
        calendar: Optional[str] = None,
        contractPerformance: Optional[str] = None,
        cycleAnchorDateOfFee: Optional[Union[datetime, str]] = None,
        cycleAnchorDateOfInterestPayment: Optional[Union[datetime, str]] = None,
        cycleAnchorDateOfRateReset: Optional[Union[datetime, str]] = None,
        cycleOfFee: Optional[str] = None,
        cycleOfInterestPayment: Optional[str] = None,
        cycleOfRateReset: Optional[str] = None,
        delinquencyPeriod: Optional[str] = None,
        delinquencyRate: Optional[float] = None,
        endOfMonthConvention: Optional[str] = None,
        feeAccrued: Optional[float] = None,
        feeBasis: Optional[str] = None,
        feeRate: Optional[float] = None,
        fixingPeriod: Optional[str] = None,
        gracePeriod: Optional[str] = None,
        marketObjectCodeOfRateReset: Optional[str] = None,
        maturityDate: Optional[Union[datetime, str]] = None,
        nextResetRate: Optional[float] = None,
        nonPerformingDate: Optional[Union[datetime, str]] = None,
        prepaymentPeriod: Optional[str] = None,
        rateMultiplier: Optional[float] = None,
        rateSpread: Optional[float] = None,
        seniority: Optional[str] = None,
        settlementCurrency: Optional[str] = None,
        **other_terms):
        terms = {}
        builder = self.TermBuilder(terms)
        term_names = ['contractDealDate', 'contractID', 'contractRole', 'counterpartyID', 'creatorID', 'currency', 'dayCountConvention', 'initialExchangeDate', 'nominalInterestRate', 'notionalPrincipal', 'statusDate', 'xDayNotice', 'accruedInterest', 'businessDayConvention', 'calendar', 'contractPerformance', 'cycleAnchorDateOfFee', 'cycleAnchorDateOfInterestPayment', 'cycleAnchorDateOfRateReset', 'cycleOfFee', 'cycleOfInterestPayment', 'cycleOfRateReset', 'delinquencyPeriod', 'delinquencyRate', 'endOfMonthConvention', 'feeAccrued', 'feeBasis', 'feeRate', 'fixingPeriod', 'gracePeriod', 'marketObjectCodeOfRateReset', 'maturityDate', 'nextResetRate', 'nonPerformingDate', 'prepaymentPeriod', 'rateMultiplier', 'rateSpread', 'seniority', 'settlementCurrency']
        for name in term_names:
            builder.add(name, locals()[name])

        for term_name, value in other_terms.items():
            pascal_case = term_name[0].upper() + term_name[1:]
            term_class = globals().get(pascal_case)
            if term_class:
                terms[term_name] = term_class(value)
            else:
                terms[term_name] = UserDefinedTerm(termName=term_name, value=value)

        terms["contractType"] = ContractType("CLM")

        super().__init__(terms_dict=terms)
        self.check_time_consistency_rules()
        self.validate_terms()

    def validate_terms(self):

        # Validate Group 1
        if self.terms.get("feeRate") is not None:
            missing = [t for t in ["feeBasis"] if self.terms.get(t) is None]
            if missing:
                raise ValueError(f"Group 1: Missing required terms: {', '.join(missing)}")

        # Validate Group 9
        if self.terms.get("cycleAnchorDateOfRateReset") is not None or self.terms.get("cycleOfRateReset") is not None:
            missing = [t for t in ["rateSpread", "marketObjectCodeOfRateReset"] if self.terms.get(t) is None]
            if missing:
                raise ValueError(f"Group 9: Missing required terms: {', '.join(missing)}")