from datetime import datetime
from typing import Union

from .contract_terms_generated import *
from .contractModel import ContractModel


class CSH(ContractModel):
    """ACTUS Contract Type: CSH

    Description:
    Cash or cash equivalent position

    Real-world Instrument Examples (but not limited to):
    Cash, deposits at central bank.

    Required Terms:
    - contractID
    - contractRole
    - contractType
    - creatorID
    - currency
    - notionalPrincipal
    - statusDate

    Conditional Groups:


    Note:
    - 'contractType' is auto-set to "CSH" during initialization.
    """

    REQUIRED_TERMS = ['contractID', 'contractRole', 'creatorID', 'currency', 'notionalPrincipal', 'statusDate']

    CONDITIONAL_GROUPS = {

    }

    def __init__(self,
        contractID: str,
        contractRole: str,
        creatorID: str,
        currency: str,
        notionalPrincipal: float,
        statusDate: Union[datetime, str],
        **other_terms):
        terms = {}
        builder = self.TermBuilder(terms)
        term_names = ['contractID', 'contractRole', 'creatorID', 'currency', 'notionalPrincipal', 'statusDate']
        for name in term_names:
            builder.add(name, locals()[name])

        for term_name, value in other_terms.items():
            pascal_case = term_name[0].upper() + term_name[1:]
            term_class = globals().get(pascal_case)
            if term_class:
                terms[term_name] = term_class(value)
            else:
                terms[term_name] = UserDefinedTerm(termName=term_name, value=value)

        terms["contractType"] = ContractType("CSH")

        super().__init__(terms_dict=terms)
        self.check_time_consistency_rules()
        self.validate_terms()

    def validate_terms(self):
        pass