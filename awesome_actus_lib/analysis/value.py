import numpy as np
import pandas as pd

from ..models.RiskFactor import ReferenceIndex, YieldCurve
from .Analysis import Analysis


class ValueAnalysis(Analysis):
    """
    Computes nominal value and net present value (NPV) of a portfolio using its cash flows.

    Parameters:
        cf_stream (CashFlowStream): Cash flow stream from a contract simulation.
        as_of_date (datetime or str, optional): Valuation date. Defaults to first event date.
        flat_rate (float, optional): Fallback constant discount rate (e.g. 0.02 for 2%).
        discount_curve_code (str, optional): marketObjectCode of the curve to use if multiple are available.

    Usage:
        - If multiple ReferenceIndex curves are available, specify `discount_curve_code`.
        - If none or one is available, it is auto-used.
        - If no curve or rate is available, NPV will not be computed.
    """

    def __init__(self, cf_stream, as_of_date=None, flat_rate=None, discount_curve_code=None):
        super().__init__(cf_stream)
        self.as_of_date = pd.to_datetime(as_of_date) if as_of_date else pd.to_datetime(self.events_df["time"].min())
        self.flat_rate = flat_rate
        self.discount_curve = self._select_discount_curve(discount_curve_code)

        self.nominal_value = self._compute_nominal_value()
        self.npv = self._compute_discounted_value()
        self.results = pd.DataFrame([{
            "as_of_date": self.as_of_date,
            "nominal_value": self.nominal_value,
            "npv": self.npv
        }])


    def _select_discount_curve(self, curve_code=None):
        """
        Select a discount curve from available risk factors.
        Supports both ReferenceIndex and YieldCurve as valid types.
        """
        valid_types = (ReferenceIndex, YieldCurve)

        # Normalize to list
        if isinstance(self.risk_factors, valid_types):
            curves = [self.risk_factors]
        elif isinstance(self.risk_factors, list):
            curves = [rf for rf in self.risk_factors if isinstance(rf, valid_types)]
        else:
            curves = []

        if curve_code:
            for curve in curves:
                if curve.marketObjectCode == curve_code:
                    return curve
            raise ValueError(f"[ValueAnalysis] No curve found with marketObjectCode='{curve_code}'.")

        if len(curves) == 1:
            print(f"[ValueAnalysis] Using only available discount curve: {curves[0].marketObjectCode}")
            return curves[0]

        elif len(curves) > 1:
            available = ", ".join(c.marketObjectCode for c in curves)
            raise ValueError(
                "[ValueAnalysis] Multiple discount curves found. Please specify one using `discount_curve_code`.\n"
                f"Available: {available}"
            )

        print("[ValueAnalysis] No discount curve available.")
        return None

    def _compute_nominal_value(self):
        df = self.events_df.copy()
        df["time"] = pd.to_datetime(df["time"])
        df = df[df["time"] >= self.as_of_date]
        df["payoff"] = pd.to_numeric(df["payoff"], errors="coerce").fillna(0)
        return df["payoff"].sum()

    def _compute_discounted_value(self):
        df = self.events_df.copy()
        df["time"] = pd.to_datetime(df["time"])
        df = df[df["time"] >= self.as_of_date].copy()
        df["payoff"] = pd.to_numeric(df["payoff"], errors="coerce").fillna(0)

        if df.empty:
            print("[ValueAnalysis] No future payoffs after valuation date. NPV = 0.")
            return 0.0

        # Use discount curve if available
        if self.discount_curve is not None:
            try:
                rate_data = self.discount_curve._data.copy()
                rate_data["date"] = self.discount_curve._validate_and_format_dates("date")
                rate_data = rate_data.set_index("date").sort_index()
                rate_col = None
                for col in rate_data.columns:
                    if col.lower() in ("value", "rate"):
                        rate_col = col
                        break

                if rate_col is None:
                    raise ValueError("Discount curve must have a 'value' or 'rate' column.")

                rate_series = rate_data[rate_col].sort_index()

                df["t"] = (df["time"] - self.as_of_date).dt.days / 365.0
                timestamps = rate_series.index.astype("datetime64[ns]").astype("int64") / 1e9
                df["rate"] = df["time"].apply(
                    lambda t: np.interp(t.timestamp(), timestamps, rate_series.values) / self.discount_curve.base
                )
                df["df"] = np.exp(-df["rate"] * df["t"])
                df["present_value"] = df["payoff"] * df["df"]

                self.details = df[["time", "payoff", "rate", "df", "present_value"]]
                print(f"[ValueAnalysis] Discounting using curve '{self.discount_curve.marketObjectCode}'.")
                return df["present_value"].sum()
            except Exception as e:
                print(f"[ValueAnalysis] Failed to compute discounting from curve: {e}")

        # Fallback to flat rate
        if self.flat_rate is not None:
            print(f"[ValueAnalysis] ℹ️ Using fallback flat rate of {self.flat_rate:.2%} for discounting.")
            df["t"] = (df["time"] - self.as_of_date).dt.days / 365.0
            df["rate"] = self.flat_rate
            df["df"] = np.exp(-self.flat_rate * df["t"])
            df["present_value"] = df["payoff"] * df["df"]

            self.details = df[["time", "payoff", "rate", "df", "present_value"]]
            return df["present_value"].sum()

        # No method available
        print("[ValueAnalysis] Cannot compute NPV: no discount curve or fallback rate provided.")
        print("Please provide a valid `discount_curve_code` or `flat_rate`.")
        return None

    def summarize(self) -> dict:
        return {
            "As of Date": self.as_of_date.strftime("%Y-%m-%d"),
            "Nominal Value (undiscounted)": f"{self.nominal_value:,.2f}",
            "Net Present Value (NPV)": f"{self.npv:,.2f}" if self.npv is not None else "N/A"
        }