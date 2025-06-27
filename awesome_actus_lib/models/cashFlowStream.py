import pandas as pd

from .contractPlot import contractPlot
from .portfolioPlot import portfolioPlot


class CashFlowStream:
    """
    Represents the result of a contract simulation (cash flow generation).

    Attributes:
        portfolio (Portfolio): The portfolio that was simulated
        riskFactors (list or None): Risk factor data used in the simulation
        events_df (pd.DataFrame): Flattened DataFrame of all events
    """

    def __init__(self, portfolio, riskFactors, raw_response: list):
        self.portfolio = portfolio
        self.riskFactors = riskFactors
        self.events_df = self._parse_events(raw_response)

    def _parse_events(self, response):
        """
        Recursively flattens the response and returns a DataFrame with all events from parent and nested contracts.
        """
        def collect_all_events(contract_node):
            collected = []
            contract_id = contract_node.get("contractID")
            for event in contract_node.get("events", []):
                event_copy = dict(event)
                event_copy["contractId"] = contract_id
                collected.append(event_copy)
            for child in contract_node.get("children", []):
                collected.extend(collect_all_events(child))
            return collected

        all_events = []
        #print(f"[DEBUG] Raw Response from generateEvents: {response}")
        for contract_result in response:
            all_events.extend(collect_all_events(contract_result))

        return pd.DataFrame(all_events)


    def __str__(self):
        return f"<CashFlowStream with {len(self.events_df)} events for {len(self.portfolio)} contracts>"

    def __repr__(self):
        return self.__str__()

    def show(self, max_rows: int = 10, full: bool = False):
        """
        Displays the event DataFrame. Shows a preview by default.

        Args:
            max_rows (int): Number of rows to show if full=False.
            full (bool): If True, shows the entire DataFrame.
        """
        pd.set_option("display.max_columns", None)

        if self.events_df.empty:
            print("No events available.")
        elif full:
            print(self.events_df.to_string(index=False))
        else:
            print(self.events_df.head(max_rows).to_string(index=False))


    def plot(self, title=None, y1_label="Notional/Principal", y2_label="Interest Payments", return_fig=False):
        """
        Plots either a single contract (if only one contractId) or delegates to portfolio-level visualization.
        """
        if self.events_df.empty:
            print("No events to plot.")
            return

        unique_contracts = self.events_df["contractId"].unique()

        if len(unique_contracts) == 1:
            return contractPlot(
                df=self.events_df,
                contract_type=self.portfolio.contracts[0].terms.get("contractType",None).value,  # Assuming portfolio is list-like
                title=title or f"Events for {unique_contracts[0]}",
                y1_label=y1_label,
                y2_label=y2_label, 
                return_fig=return_fig
            )
        else:
            return portfolioPlot(
                events_df=self.events_df,
                title=title or "Aggregated Portfolio Events",
                y1_label=y1_label,
                return_fig=return_fig,
            )