from datetime import datetime
from typing import Any, Optional, Union

from .contract_terms_generated import *
from .contractModel import ContractModel


class CEC(ContractModel):
    """ACTUS Contract Type: CEC

    Description:
    Collateral creates a relationship between a collateral an obligee and a debtor, covering the exposure from the debtor with the collateral.

    Real-world Instrument Examples (but not limited to):
    Mortgages include a collateral contract. Any coverage with financial or physical collateral.

    Required Terms:
    - contractDealDate
    - contractID
    - contractRole
    - contractStructure
    - contractType
    - counterpartyID
    - creatorID
    - guaranteedExposure
    - statusDate

    Conditional Groups:
    - Group 7
        * Drivers: exerciseDate
        * Required if triggered: exerciseAmount
        * Optional: None

    Standalone Optional Terms:
    - businessDayConvention
    - calendar
    - coverageOfCreditEnhancement
    - creditEventTypeCovered
    - endOfMonthConvention
    - settlementPeriod

    Note:
    - 'contractType' is auto-set to "CEC" during initialization.
    """

    REQUIRED_TERMS = ['contractDealDate', 'contractID', 'contractRole', 'contractStructure', 'counterpartyID', 'creatorID', 'guaranteedExposure', 'statusDate']

    CONDITIONAL_GROUPS = {
    "7": {"drivers": ['exerciseDate'], "required": ['exerciseAmount'], "optional": []}
    }

    def __init__(self,
        contractDealDate: Union[datetime, str],
        contractID: str,
        contractRole: str,
        contractStructure: Any,
        counterpartyID: str,
        creatorID: str,
        guaranteedExposure: str,
        statusDate: Union[datetime, str],
        businessDayConvention: Optional[str] = None,
        calendar: Optional[str] = None,
        coverageOfCreditEnhancement: Optional[float] = None,
        creditEventTypeCovered: Optional[Any] = None,
        endOfMonthConvention: Optional[str] = None,
        exerciseAmount: Optional[float] = None,
        exerciseDate: Optional[Union[datetime, str]] = None,
        settlementPeriod: Optional[str] = None,
        **other_terms):
        terms = {}
        builder = self.TermBuilder(terms)
        term_names = ['contractDealDate', 'contractID', 'contractRole', 'contractStructure', 'counterpartyID', 'creatorID', 'guaranteedExposure', 'statusDate', 'businessDayConvention', 'calendar', 'coverageOfCreditEnhancement', 'creditEventTypeCovered', 'endOfMonthConvention', 'exerciseAmount', 'exerciseDate', 'settlementPeriod']
        for name in term_names:
            builder.add(name, locals()[name])

        for term_name, value in other_terms.items():
            pascal_case = term_name[0].upper() + term_name[1:]
            term_class = globals().get(pascal_case)
            if term_class:
                terms[term_name] = term_class(value)
            else:
                terms[term_name] = UserDefinedTerm(termName=term_name, value=value)

        terms["contractType"] = ContractType("CEC")

        super().__init__(terms_dict=terms)
        self.check_time_consistency_rules()
        self.validate_terms()

    def validate_terms(self):

        # Validate Group 7
        if self.terms.get("exerciseDate") is not None:
            missing = [t for t in ["exerciseAmount"] if self.terms.get(t) is None]
            if missing:
                raise ValueError(f"Group 7: Missing required terms: {', '.join(missing)}")