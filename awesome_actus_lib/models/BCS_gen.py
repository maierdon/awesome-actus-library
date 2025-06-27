from datetime import datetime
from typing import Any, Optional, Union

from .contract_terms_generated import *
from .contractModel import ContractModel


class BCS(ContractModel):
    """ACTUS Contract Type: BCS

    Description:
    A boundary controlled switch is a derivative contract with subcontract legs which can be activated (knocked in) or extinguished (knocked out) when the underlying asset price reaches a specified value.  The underlying asset may be a stock, index, or exchange-traded fund. Boundary controlled switch contracts with a single boundary are currently defined.

    Real-world Instrument Examples (but not limited to):
    Knock-in and Knock-out barrier options with a single boundary. Bonus contracts with payout when underlying asset price remains above or below a specified level for specified period.

    Required Terms:
    - boundaryDirection
    - boundaryEffect
    - boundaryLegInitiallyActive
    - boundaryMonitoringAnchorDate
    - boundaryMonitoringCycle
    - boundaryMonitoringEndDate
    - boundaryValue
    - contractDealDate
    - contractID
    - contractRole
    - contractStructure
    - contractType
    - maturityDate
    - priceAtPurchaseDate
    - purchaseDate
    - statusDate

    Conditional Groups:
    - Group 1
        * Drivers: terminationDate
        * Required if triggered: priceAtTerminationDate
        * Optional: None

    Standalone Optional Terms:
    - businessDayConvention
    - calendar
    - deliverySettlement
    - endOfMonthConvention
    - marketObjectCode
    - marketValueObserved
    - settlementPeriod

    Note:
    - 'contractType' is auto-set to "BCS" during initialization.
    """

    REQUIRED_TERMS = ['boundaryDirection', 'boundaryEffect', 'boundaryLegInitiallyActive', 'boundaryMonitoringAnchorDate', 'boundaryMonitoringCycle', 'boundaryMonitoringEndDate', 'boundaryValue', 'contractDealDate', 'contractID', 'contractRole', 'contractStructure', 'maturityDate', 'priceAtPurchaseDate', 'purchaseDate', 'statusDate']

    CONDITIONAL_GROUPS = {
    "1": {"drivers": ['terminationDate'], "required": ['priceAtTerminationDate'], "optional": []}
    }

    def __init__(self,
        boundaryDirection: str,
        boundaryEffect: str,
        boundaryLegInitiallyActive: str,
        boundaryMonitoringAnchorDate: Union[datetime, str],
        boundaryMonitoringCycle: str,
        boundaryMonitoringEndDate: Union[datetime, str],
        boundaryValue: float,
        contractDealDate: Union[datetime, str],
        contractID: str,
        contractRole: str,
        contractStructure: Any,
        maturityDate: Union[datetime, str],
        priceAtPurchaseDate: float,
        purchaseDate: Union[datetime, str],
        statusDate: Union[datetime, str],
        businessDayConvention: Optional[str] = None,
        calendar: Optional[str] = None,
        deliverySettlement: Optional[str] = None,
        endOfMonthConvention: Optional[str] = None,
        marketObjectCode: Optional[str] = None,
        marketValueObserved: Optional[float] = None,
        priceAtTerminationDate: Optional[float] = None,
        settlementPeriod: Optional[str] = None,
        terminationDate: Optional[Union[datetime, str]] = None,
        **other_terms):
        terms = {}
        builder = self.TermBuilder(terms)
        term_names = ['boundaryDirection', 'boundaryEffect', 'boundaryLegInitiallyActive', 'boundaryMonitoringAnchorDate', 'boundaryMonitoringCycle', 'boundaryMonitoringEndDate', 'boundaryValue', 'contractDealDate', 'contractID', 'contractRole', 'contractStructure', 'maturityDate', 'priceAtPurchaseDate', 'purchaseDate', 'statusDate', 'businessDayConvention', 'calendar', 'deliverySettlement', 'endOfMonthConvention', 'marketObjectCode', 'marketValueObserved', 'priceAtTerminationDate', 'settlementPeriod', 'terminationDate']
        for name in term_names:
            builder.add(name, locals()[name])

        for term_name, value in other_terms.items():
            pascal_case = term_name[0].upper() + term_name[1:]
            term_class = globals().get(pascal_case)
            if term_class:
                terms[term_name] = term_class(value)
            else:
                terms[term_name] = UserDefinedTerm(termName=term_name, value=value)

        terms["contractType"] = ContractType("BCS")

        super().__init__(terms_dict=terms)
        self.check_time_consistency_rules()
        self.validate_terms()

    def validate_terms(self):

        # Validate Group 1
        if self.terms.get("terminationDate") is not None:
            missing = [t for t in ["priceAtTerminationDate"] if self.terms.get(t) is None]
            if missing:
                raise ValueError(f"Group 1: Missing required terms: {', '.join(missing)}")