from abc import ABC

import pandas as pd


class Analysis(ABC):
    def __init__(self, cf_stream):
        """
        Base class for financial analysis modules.
        Expects a CashFlowStream.
        """
        self.cf_stream = cf_stream
        self.portfolio = cf_stream.portfolio
        self.risk_factors = cf_stream.riskFactors
        self.events_df = cf_stream.events_df.copy()

    # @abstractmethod not needed for now
    def analyze(self):
        """
        Optional analysis method for subclasses that support a direct analysis step.
        ValueAnalysis uses explicit value methods instead.
        """

    def to_dataframe(self) -> pd.DataFrame:
        """
        Return the raw cash flow events.
        """
        return self.events_df.copy()

