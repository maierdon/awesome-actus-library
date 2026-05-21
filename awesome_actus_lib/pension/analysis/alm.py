from typing import List, Optional, Union

import pandas as pd

from ...analysis.liquidity import LiquidityAnalysis
from ...analysis.value import ValueAnalysis
from ...models.cashFlowStream import CashFlowStream
from ...models.RiskFactor import ReferenceIndex, YieldCurve

DiscountSource = Union[ReferenceIndex, YieldCurve, List[Union[ReferenceIndex, YieldCurve]]]


class ALMAnalysis:
    """Joint analysis of asset and liability cashflows.

    Liability cashflows are produced by ClosedFundSimulator. Assets come
    from a normal AAL ActusService.generateEvents() call. Both must share
    a consistent valuation context (same discount source).
    """

    def __init__(
        self,
        assets_cf: CashFlowStream,
        liabilities_cf: CashFlowStream,
        discount_source: Optional[DiscountSource] = None,
        flat_rate: Optional[float] = None,
        discount_curve_code: Optional[str] = None,
    ):
        self.assets_cf = assets_cf
        self.liabilities_cf = liabilities_cf
        self.discount_source = discount_source
        self.flat_rate = flat_rate
        self.discount_curve_code = discount_curve_code

    def net_liquidity(self, freq: str = "YE") -> pd.DataFrame:
        a = LiquidityAnalysis(self.assets_cf, freq=freq).results
        l = LiquidityAnalysis(self.liabilities_cf, freq=freq).results
        joined = a.join(l, how="outer", lsuffix="_assets", rsuffix="_liabilities").fillna(0.0)
        joined["net"] = joined["netLiquidity_assets"] + joined["netLiquidity_liabilities"]
        return joined

    def _value(self, cf: CashFlowStream, as_of: pd.Timestamp) -> float:
        original_rf = cf.riskFactors
        if self.discount_source is not None:
            cf.riskFactors = self.discount_source
        try:
            va = ValueAnalysis(
                cf,
                as_of_date=as_of,
                flat_rate=self.flat_rate,
                discount_curve_code=self.discount_curve_code,
            )
            return va.npv
        finally:
            cf.riskFactors = original_rf

    def funding_ratio(self, as_of) -> float:
        as_of_ts = pd.to_datetime(as_of)
        npv_assets = self._value(self.assets_cf, as_of_ts)
        npv_liab = self._value(self.liabilities_cf, as_of_ts)
        if npv_liab is None or npv_liab == 0:
            raise ValueError("Liability NPV is zero or None; cannot compute funding ratio.")
        # Liabilities net cashflow is negative when obligations dominate.
        # Funding ratio = assets / |obligations|.
        return npv_assets / abs(npv_liab)

    def deckungsgrad_path(self, dates) -> pd.Series:
        return pd.Series(
            {pd.to_datetime(d): self.funding_ratio(d) for d in dates},
            name="funding_ratio",
        )
