from datetime import datetime
from typing import Any, Optional, Union

from .contract_terms_generated import *
from .contractModel import ContractModel


class OPTNS(ContractModel):
    """ACTUS Contract Type: OPTNS

    Description:
    Calculates straight option pay-off for any basic CT as underlying (PAM, ANN etc.) but also SWAPS, FXOUT, STK and COM. Single, periodic and continuous strike is supported.

    Real-world Instrument Examples (but not limited to):
    European, American and Bermudan options with Interest rate, FX and stock futures as underlying instruments.

    Required Terms:
    - contractDealDate
    - contractID
    - contractRole
    - contractStructure
    - contractType
    - counterpartyID
    - creatorID
    - currency
    - maturityDate
    - optionExerciseEndDate
    - optionExerciseType
    - optionStrike1
    - optionType
    - priceAtPurchaseDate
    - purchaseDate
    - statusDate

    Conditional Groups:
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
    - cycleAnchorDateOfOptionality
    - cycleOfOptionality
    - delinquencyPeriod
    - delinquencyRate
    - deliverySettlement
    - endOfMonthConvention
    - gracePeriod
    - marketObjectCode
    - marketValueObserved
    - nonPerformingDate
    - optionStrike2
    - seniority
    - settlementCurrency
    - settlementPeriod

    Note:
    - 'contractType' is auto-set to "OPTNS" during initialization.
    """

    REQUIRED_TERMS = ['contractDealDate', 'contractID', 'contractRole', 'contractStructure', 'counterpartyID', 'creatorID', 'currency', 'maturityDate', 'optionExerciseEndDate', 'optionExerciseType', 'optionStrike1', 'optionType', 'priceAtPurchaseDate', 'purchaseDate', 'statusDate']

    CONDITIONAL_GROUPS = {
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
        maturityDate: Union[datetime, str],
        optionExerciseEndDate: Union[datetime, str],
        optionExerciseType: str,
        optionStrike1: float,
        optionType: str,
        priceAtPurchaseDate: float,
        purchaseDate: Union[datetime, str],
        statusDate: Union[datetime, str],
        businessDayConvention: Optional[str] = None,
        calendar: Optional[str] = None,
        contractPerformance: Optional[str] = None,
        cycleAnchorDateOfOptionality: Optional[Union[datetime, str]] = None,
        cycleOfOptionality: Optional[str] = None,
        delinquencyPeriod: Optional[str] = None,
        delinquencyRate: Optional[float] = None,
        deliverySettlement: Optional[str] = None,
        endOfMonthConvention: Optional[str] = None,
        exerciseAmount: Optional[float] = None,
        exerciseDate: Optional[Union[datetime, str]] = None,
        gracePeriod: Optional[str] = None,
        marketObjectCode: Optional[str] = None,
        marketValueObserved: Optional[float] = None,
        nonPerformingDate: Optional[Union[datetime, str]] = None,
        optionStrike2: Optional[float] = None,
        priceAtTerminationDate: Optional[float] = None,
        seniority: Optional[str] = None,
        settlementCurrency: Optional[str] = None,
        settlementPeriod: Optional[str] = None,
        terminationDate: Optional[Union[datetime, str]] = None,
        **other_terms):
        terms = {}
        builder = self.TermBuilder(terms)
        term_names = ['contractDealDate', 'contractID', 'contractRole', 'contractStructure', 'counterpartyID', 'creatorID', 'currency', 'maturityDate', 'optionExerciseEndDate', 'optionExerciseType', 'optionStrike1', 'optionType', 'priceAtPurchaseDate', 'purchaseDate', 'statusDate', 'businessDayConvention', 'calendar', 'contractPerformance', 'cycleAnchorDateOfOptionality', 'cycleOfOptionality', 'delinquencyPeriod', 'delinquencyRate', 'deliverySettlement', 'endOfMonthConvention', 'exerciseAmount', 'exerciseDate', 'gracePeriod', 'marketObjectCode', 'marketValueObserved', 'nonPerformingDate', 'optionStrike2', 'priceAtTerminationDate', 'seniority', 'settlementCurrency', 'settlementPeriod', 'terminationDate']
        for name in term_names:
            builder.add(name, locals()[name])

        for term_name, value in other_terms.items():
            pascal_case = term_name[0].upper() + term_name[1:]
            term_class = globals().get(pascal_case)
            if term_class:
                terms[term_name] = term_class(value)
            else:
                terms[term_name] = UserDefinedTerm(termName=term_name, value=value)

        terms["contractType"] = ContractType("OPTNS")

        super().__init__(terms_dict=terms)
        self.check_time_consistency_rules()
        self.validate_terms()

    def validate_terms(self):

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