from datetime import datetime
from typing import Optional, Union

from .contract_terms_generated import *
from .contractModel import ContractModel


class COM(ContractModel):
    """ACTUS Contract Type: COM

    Description:
    This is not a financial contract in its propper sense. However it traks movements of commodities such as oil, gas or even houses. Such commodities can serve as underlyings of commodity futures, guarantees or simply asset positions.

    Real-world Instrument Examples (but not limited to):
    Oil, gas, electricity, houses etc.

    Required Terms:
    - contractDealDate
    - contractID
    - contractRole
    - contractType
    - creatorID
    - currency
    - priceAtPurchaseDate
    - purchaseDate
    - quantity
    - statusDate
    - unit

    Conditional Groups:
    - Group 6
        * Drivers: terminationDate
        * Required if triggered: priceAtTerminationDate
        * Optional: None

    Standalone Optional Terms:
    - counterpartyID
    - marketObjectCode
    - marketValueObserved

    Note:
    - 'contractType' is auto-set to "COM" during initialization.
    """

    REQUIRED_TERMS = ['contractDealDate', 'contractID', 'contractRole', 'creatorID', 'currency', 'priceAtPurchaseDate', 'purchaseDate', 'quantity', 'statusDate', 'unit']

    CONDITIONAL_GROUPS = {
    "6": {"drivers": ['terminationDate'], "required": ['priceAtTerminationDate'], "optional": []}
    }

    def __init__(self,
        contractDealDate: Union[datetime, str],
        contractID: str,
        contractRole: str,
        creatorID: str,
        currency: str,
        priceAtPurchaseDate: float,
        purchaseDate: Union[datetime, str],
        quantity: float,
        statusDate: Union[datetime, str],
        unit: str,
        counterpartyID: Optional[str] = None,
        marketObjectCode: Optional[str] = None,
        marketValueObserved: Optional[float] = None,
        priceAtTerminationDate: Optional[float] = None,
        terminationDate: Optional[Union[datetime, str]] = None,
        **other_terms):
        terms = {}
        builder = self.TermBuilder(terms)
        term_names = ['contractDealDate', 'contractID', 'contractRole', 'creatorID', 'currency', 'priceAtPurchaseDate', 'purchaseDate', 'quantity', 'statusDate', 'unit', 'counterpartyID', 'marketObjectCode', 'marketValueObserved', 'priceAtTerminationDate', 'terminationDate']
        for name in term_names:
            builder.add(name, locals()[name])

        for term_name, value in other_terms.items():
            pascal_case = term_name[0].upper() + term_name[1:]
            term_class = globals().get(pascal_case)
            if term_class:
                terms[term_name] = term_class(value)
            else:
                terms[term_name] = UserDefinedTerm(termName=term_name, value=value)

        terms["contractType"] = ContractType("COM")

        super().__init__(terms_dict=terms)
        self.check_time_consistency_rules()
        self.validate_terms()

    def validate_terms(self):

        # Validate Group 6
        if self.terms.get("terminationDate") is not None:
            missing = [t for t in ["priceAtTerminationDate"] if self.terms.get(t) is None]
            if missing:
                raise ValueError(f"Group 6: Missing required terms: {', '.join(missing)}")