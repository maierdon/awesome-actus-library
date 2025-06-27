from datetime import datetime
from typing import Any, Optional, Union

from .contract_terms_generated import *
from .contractModel import ContractModel


class CEG(ContractModel):
    """ACTUS Contract Type: CEG

    Description:
    Guarantee creates a relationship between a guarantor, an obligee and a debtor, moving the exposure from the debtor to the guarantor.

    Real-world Instrument Examples (but not limited to):
    Personal guarantee. Government guarantee. Underlyings of CDO´s.

    Required Terms:
    - contractDealDate
    - contractID
    - contractRole
    - contractStructure
    - contractType
    - counterpartyID
    - creatorID
    - currency
    - guaranteedExposure
    - statusDate

    Conditional Groups:
    - Group 1
        * Drivers: feeRate
        * Required if triggered: feeBasis
        * Optional: cycleAnchorDateOfFee, cycleOfFee, feeAccrued
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
    - coverageOfCreditEnhancement
    - creditEventTypeCovered
    - delinquencyPeriod
    - delinquencyRate
    - endOfMonthConvention
    - gracePeriod
    - maturityDate
    - nonPerformingDate
    - notionalPrincipal
    - settlementCurrency
    - settlementPeriod

    Note:
    - 'contractType' is auto-set to "CEG" during initialization.
    """

    REQUIRED_TERMS = ['contractDealDate', 'contractID', 'contractRole', 'contractStructure', 'counterpartyID', 'creatorID', 'currency', 'guaranteedExposure', 'statusDate']

    CONDITIONAL_GROUPS = {
    "1": {"drivers": ['feeRate'], "required": ['feeBasis'], "optional": ['cycleAnchorDateOfFee', 'cycleOfFee', 'feeAccrued']},
    "5": {"drivers": ['purchaseDate'], "required": ['priceAtPurchaseDate'], "optional": []},
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
        guaranteedExposure: str,
        statusDate: Union[datetime, str],
        businessDayConvention: Optional[str] = None,
        calendar: Optional[str] = None,
        contractPerformance: Optional[str] = None,
        coverageOfCreditEnhancement: Optional[float] = None,
        creditEventTypeCovered: Optional[Any] = None,
        cycleAnchorDateOfFee: Optional[Union[datetime, str]] = None,
        cycleOfFee: Optional[str] = None,
        delinquencyPeriod: Optional[str] = None,
        delinquencyRate: Optional[float] = None,
        endOfMonthConvention: Optional[str] = None,
        exerciseAmount: Optional[float] = None,
        exerciseDate: Optional[Union[datetime, str]] = None,
        feeAccrued: Optional[float] = None,
        feeBasis: Optional[str] = None,
        feeRate: Optional[float] = None,
        gracePeriod: Optional[str] = None,
        maturityDate: Optional[Union[datetime, str]] = None,
        nonPerformingDate: Optional[Union[datetime, str]] = None,
        notionalPrincipal: Optional[float] = None,
        priceAtPurchaseDate: Optional[float] = None,
        priceAtTerminationDate: Optional[float] = None,
        purchaseDate: Optional[Union[datetime, str]] = None,
        settlementCurrency: Optional[str] = None,
        settlementPeriod: Optional[str] = None,
        terminationDate: Optional[Union[datetime, str]] = None,
        **other_terms):
        terms = {}
        builder = self.TermBuilder(terms)
        term_names = ['contractDealDate', 'contractID', 'contractRole', 'contractStructure', 'counterpartyID', 'creatorID', 'currency', 'guaranteedExposure', 'statusDate', 'businessDayConvention', 'calendar', 'contractPerformance', 'coverageOfCreditEnhancement', 'creditEventTypeCovered', 'cycleAnchorDateOfFee', 'cycleOfFee', 'delinquencyPeriod', 'delinquencyRate', 'endOfMonthConvention', 'exerciseAmount', 'exerciseDate', 'feeAccrued', 'feeBasis', 'feeRate', 'gracePeriod', 'maturityDate', 'nonPerformingDate', 'notionalPrincipal', 'priceAtPurchaseDate', 'priceAtTerminationDate', 'purchaseDate', 'settlementCurrency', 'settlementPeriod', 'terminationDate']
        for name in term_names:
            builder.add(name, locals()[name])

        for term_name, value in other_terms.items():
            pascal_case = term_name[0].upper() + term_name[1:]
            term_class = globals().get(pascal_case)
            if term_class:
                terms[term_name] = term_class(value)
            else:
                terms[term_name] = UserDefinedTerm(termName=term_name, value=value)

        terms["contractType"] = ContractType("CEG")

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
        if self.terms.get("exerciseDate") is not None:
            missing = [t for t in ["exerciseAmount"] if self.terms.get(t) is None]
            if missing:
                raise ValueError(f"Group 7: Missing required terms: {', '.join(missing)}")