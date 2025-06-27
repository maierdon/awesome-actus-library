import matplotlib.pyplot as plt
import pandas as pd

from .Analysis import Analysis


class IncomeAnalysis(Analysis):
    def __init__(self, cf_stream, freq="M", start=None, end=None):
        super().__init__(cf_stream)
        self.results = self.analyze(freq=freq, start=start, end=end)

    def analyze(self, freq: str = "M", start: pd.Timestamp = None, end: pd.Timestamp = None) -> pd.DataFrame:
        df = self.events_df.copy()
        df["time"] = pd.to_datetime(df["time"])
        df["payoff"] = pd.to_numeric(df["payoff"], errors="coerce").fillna(0)

        if start is None:
            start = df["time"].min()
        if end is None:
            end = df["time"].max()

        df = df[(df["time"] >= start) & (df["time"] <= end)]
        df = df[df["type"].isin({"IP", "FP"})]
        df = df.set_index("time")

        if freq == "2Q":
            df["year"] = df.index.year
            df["half"] = (df.index.month > 6).astype(int) + 1
            result = df.groupby(["year", "half"])["payoff"].sum()
            result.index = [f"{'1st' if h==1 else '2nd'} Half {y}" for (y, h) in result.index]
        else:
            result = df["payoff"].resample(freq).sum()
            if freq == "M":
                result.index = result.index.strftime("%B %Y")
            elif freq == "Q":
                result.index = [f"Q{d.quarter} {d.year}" for d in result.index]
            elif freq == "Y":
                result.index = result.index.strftime("%Y")

        return result.to_frame(name="netIncome")
    
    def plot(self, title="Income over Time", figsize=(10, 4), return_fig=False):
        fig, ax = plt.subplots(figsize=figsize)
        self.results.plot(kind="bar", title=title, legend=False, ax=ax)
        ax.set_ylabel("Amount")
        ax.set_xlabel("Time Bucket")
        ax.grid(True, axis="y", linestyle="--", alpha=0.6)
        plt.tight_layout()
        
        if return_fig:
            return fig
        else:
            plt.show()