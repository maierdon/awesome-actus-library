import os

import pandas as pd

from awesome_actus_lib.models.contractModel import ContractModel


class Portfolio:
    """
    A portfolio of one or more ACTUS contracts.

    This class can be initialized with either:
    - A list of ContractModel instances (e.g., [pam1, ann1, pam2])
    - A string path to a CSV file containing contract definitions

    Attributes:
        contracts (list): A list of ContractModel instances
        contract_df (pd.DataFrame): Tabular representation of the portfolio

    Examples:
        >>> portfolio = Portfolio([pam1, ann1])
        >>> portfolio = Portfolio("contracts.csv")
    """

    def __init__(self, data):
        if isinstance(data, str):
            self._init_from_csv(data)
        elif isinstance(data, list) and all(isinstance(item, ContractModel) for item in data):
            self._init_from_contracts(data)
        else:
            raise TypeError("Portfolio expects a CSV path (str) or a list of ContractModel instances.")

    def _init_from_contracts(self, contracts: list):
        self.contracts = contracts
        self.contract_df = pd.DataFrame([c.to_dict() for c in contracts])

    def _init_from_csv(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Portfolio CSV file not found: {path}")

        df = pd.read_csv(path)
        contracts = []

        for _, row in df.iterrows():
            term_dict = row.dropna().to_dict()
            ct = term_dict.get("contractType")
            if not ct:
                raise ValueError("Missing 'contractType' in one of the rows.")

            contract_class = globals().get(ct)
            if not contract_class:
                raise ValueError(f"Unknown contract type class: '{ct}'")

            # Basic instantiation: assumes flat term dict matches __init__ params
            try:
                contract = contract_class(**term_dict)
            except Exception as e:
                raise ValueError(f"Error creating contract '{ct}': {e}")
            contracts.append(contract)

        self.contracts = contracts
        self.contract_df = df

    def to_dict(self):
        return [contract.to_dict() for contract in self.contracts]

    def write_to_file(self, path: str):
        self.contract_df.to_csv(path, index=False)

    def __len__(self):
        return len(self.contracts)

    def __str__(self):
        return f"Portfolio with {len(self.contracts)} contracts."

    def __repr__(self):
        return f"<Portfolio({len(self.contracts)} contracts)>"
