from datetime import datetime
from typing import Optional, Union

from .contract_terms_generated import *
from .contractModel import ContractModel


class UMP(ContractModel):
    """ACTUS Contract Type: UMP

    Description:
    Principal paid in and out at any point in time without prefixed schedule. Interest calculated on outstanding and capitalized periodically. Needs link to a behavioral function describing expected flows.

    Real-world Instrument Examples (but not limited to):
    Saving products of all kind, current accounts. In some countries even variable rate mortgages can be represented with this CT.

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
    - Group 1
        * Drivers: feeRate
        * Required if triggered: feeBasis
        * Optional: cycleAnchorDateOfFee, cycleOfFee, feeAccrued
    - Group 6
        * Drivers: terminationDate
        * Required if triggered: priceAtTerminationDate
        * Optional: None
    - Group 9
        * Drivers: cycleAnchorDateOfRateReset, cycleOfRateReset
        * Required if triggered: rateSpread, marketObjectCodeOfRateReset
        * Optional: None

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
    - maximumPenaltyFreeDisbursement
    - nonPerformingDate
    - prepaymentPeriod
    - seniority
    - settlementCurrency
    - xDayNotice

    Note:
    - 'contractType' is auto-set to "UMP" during initialization.
    """

    REQUIRED_TERMS = ['contractDealDate', 'contractID', 'contractRole', 'counterpartyID', 'creatorID', 'currency', 'dayCountConvention', 'initialExchangeDate', 'nominalInterestRate', 'notionalPrincipal', 'statusDate']

    CONDITIONAL_GROUPS = {
    "1": {"drivers": ['feeRate'], "required": ['feeBasis'], "optional": ['cycleAnchorDateOfFee', 'cycleOfFee', 'feeAccrued']},
    "6": {"drivers": ['terminationDate'], "required": ['priceAtTerminationDate'], "optional": []},
    "9": {"drivers": ['cycleAnchorDateOfRateReset', 'cycleOfRateReset'], "required": ['rateSpread', 'marketObjectCodeOfRateReset'], "optional": []}
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
        gracePeriod: Optional[str] = None,
        marketObjectCodeOfRateReset: Optional[str] = None,
        maximumPenaltyFreeDisbursement: Optional[float] = None,
        nonPerformingDate: Optional[Union[datetime, str]] = None,
        prepaymentPeriod: Optional[str] = None,
        priceAtTerminationDate: Optional[float] = None,
        rateSpread: Optional[float] = None,
        seniority: Optional[str] = None,
        settlementCurrency: Optional[str] = None,
        terminationDate: Optional[Union[datetime, str]] = None,
        xDayNotice: Optional[str] = None,
        **other_terms):
        terms = {}
        builder = self.TermBuilder(terms)
        term_names = ['contractDealDate', 'contractID', 'contractRole', 'counterpartyID', 'creatorID', 'currency', 'dayCountConvention', 'initialExchangeDate', 'nominalInterestRate', 'notionalPrincipal', 'statusDate', 'accruedInterest', 'businessDayConvention', 'calendar', 'contractPerformance', 'cycleAnchorDateOfFee', 'cycleAnchorDateOfInterestPayment', 'cycleAnchorDateOfRateReset', 'cycleOfFee', 'cycleOfInterestPayment', 'cycleOfRateReset', 'delinquencyPeriod', 'delinquencyRate', 'endOfMonthConvention', 'feeAccrued', 'feeBasis', 'feeRate', 'gracePeriod', 'marketObjectCodeOfRateReset', 'maximumPenaltyFreeDisbursement', 'nonPerformingDate', 'prepaymentPeriod', 'priceAtTerminationDate', 'rateSpread', 'seniority', 'settlementCurrency', 'terminationDate', 'xDayNotice']
        for name in term_names:
            builder.add(name, locals()[name])

        for term_name, value in other_terms.items():
            pascal_case = term_name[0].upper() + term_name[1:]
            term_class = globals().get(pascal_case)
            if term_class:
                terms[term_name] = term_class(value)
            else:
                terms[term_name] = UserDefinedTerm(termName=term_name, value=value)

        terms["contractType"] = ContractType("UMP")

        super().__init__(terms_dict=terms)
        self.check_time_consistency_rules()
        self.validate_terms()

    def validate_terms(self):

        # Validate Group 1
        if self.terms.get("feeRate") is not None:
            missing = [t for t in ["feeBasis"] if self.terms.get(t) is None]
            if missing:
                raise ValueError(f"Group 1: Missing required terms: {', '.join(missing)}")

        # Validate Group 6
        if self.terms.get("terminationDate") is not None:
            missing = [t for t in ["priceAtTerminationDate"] if self.terms.get(t) is None]
            if missing:
                raise ValueError(f"Group 6: Missing required terms: {', '.join(missing)}")

        # Validate Group 9
        if self.terms.get("cycleAnchorDateOfRateReset") is not None or self.terms.get("cycleOfRateReset") is not None:
            missing = [t for t in ["rateSpread", "marketObjectCodeOfRateReset"] if self.terms.get(t) is None]
            if missing:
                raise ValueError(f"Group 9: Missing required terms: {', '.join(missing)}")