import numpy as np
import pandas as pd
from awesome_actus_lib import PAM, ReferenceIndex, PublicActusService, LiquidityAnalysis, ValueAnalysis, IncomeAnalysis
np.random.seed(42) # for reproducability 

contract = PAM(
    contractID="pam01",
    statusDate="2025-12-30T00:00:00",
    contractDealDate="2025-12-28T00:00:00",
    currency="USD",
    notionalPrincipal=1000,
    initialExchangeDate="2026-01-01T00:00:00",
    maturityDate="2030-01-01T00:00:00",
    nominalInterestRate=0.1,
    cycleAnchorDateOfInterestPayment="2026-01-01T00:00:00",
    cycleOfInterestPayment="P1YL0",
    dayCountConvention="30E360",
    endOfMonthConvention="SD",
    premiumDiscountAtIED=0,
    contractRole="RPA",
    creatorID="Creator-01",
    counterpartyID="Counterparty-01",
    marketObjectCodeOfRateReset="UST5Y",
    rateSpread=0, 
    cycleOfRateReset="P1YL0",
    cycleAnchorDateOfRateReset="2026-01-01T00:00:00",
)


index_data = pd.DataFrame({
    "date": pd.date_range(start="2023-01-01", end="2030-12-31", periods=20).strftime("%Y-%m-%d"),
    "value": np.random.uniform(0.01, 0.015, size=20).round(4)
})
ust5y = ReferenceIndex(marketObjectCode="UST5Y", source=index_data, base=1.0)

service = PublicActusService()
event_stream = service.generateEvents(portfolio=contract, riskFactors=[ust5y])
print(event_stream.events_df)


val = ValueAnalysis(event_stream, as_of_date="2026-01-01", discount_curve_code="UST5Y")
print(val.summarize())