"""Stage 1 verification script — closed-fund BVG liability engine.

Run from repo root:
    python examples/stage1_closed_fund.py
"""

from datetime import date

import pandas as pd

from awesome_actus_lib import (
    ClosedFundSimulator,
    Cohort,
    PensionFund,
    PensionPolicy,
)
from awesome_actus_lib.analysis.liquidity import LiquidityAnalysis
from awesome_actus_lib.analysis.value import ValueAnalysis


REQUIRED_COLS = {"time", "type", "payoff", "contractId"}


def _expected_agh(start_agh: float, gross_salary: float, start_age: int,
                  end_age: int, policy: PensionPolicy) -> float:
    """Independent re-implementation of the AGH recurrence for cross-check."""
    insured = policy.insured_salary(gross_salary)
    agh = start_agh
    for age in range(start_age, end_age):
        agh = agh * (1 + policy.applied_interest_rate) + policy.savings_rate(age) * insured
    return agh


def test_single_active_cohort() -> None:
    policy = PensionPolicy()
    fund = PensionFund(policy=policy, start_date=date(2025, 1, 1))
    fund.add_cohort(Cohort(
        cohort_id="COHORT_1995",
        birth_year=1995,
        headcount=100,
        gross_salary=80_000.0,
        accrued_savings=50_000.0,
    ))

    cf = ClosedFundSimulator(fund).run(horizon_years=36)
    df = cf.events_df

    assert REQUIRED_COLS.issubset(df.columns), f"Missing columns: {REQUIRED_COLS - set(df.columns)}"

    retirement_rows = df[df["type"] == "RETIREMENT_CONV"]
    assert len(retirement_rows) == 1, f"Expected exactly 1 retirement, got {len(retirement_rows)}"

    actual_agh = retirement_rows.iloc[0]["agh_per_capita_at_conversion"]
    expected_agh = _expected_agh(50_000.0, 80_000.0, 30, 65, policy)
    rel_err = abs(actual_agh - expected_agh) / expected_agh
    assert rel_err < 1e-6, f"AGH recurrence mismatch: actual={actual_agh}, expected={expected_agh}"
    print(f"  [single active] AGH@65 per capita = {actual_agh:,.2f} (match)")

    annual_pension = retirement_rows.iloc[0]["annual_pension_per_capita"]
    expected_pension = actual_agh * policy.conversion_rate
    assert abs(annual_pension - expected_pension) < 1e-6
    print(f"  [single active] annual pension per capita = {annual_pension:,.2f}")


def test_single_retired_cohort() -> None:
    policy = PensionPolicy()
    fund = PensionFund(policy=policy, start_date=date(2025, 1, 1))
    fund.add_cohort(Cohort(
        cohort_id="COHORT_1960",
        birth_year=1960,
        headcount=50,
        gross_salary=0.0,
        accrued_savings=500_000.0,
    ))

    horizon = 30
    cf = ClosedFundSimulator(fund).run(horizon_years=horizon)
    df = cf.events_df

    pension_rows = df[df["type"] == "PENSION_PAYMENT"]
    assert len(pension_rows) == horizon, f"Expected {horizon} pension events, got {len(pension_rows)}"

    expected_annual = 500_000.0 * policy.conversion_rate
    expected_total = -expected_annual * 50 * horizon
    actual_total = pension_rows["payoff"].sum()
    rel_err = abs(actual_total - expected_total) / abs(expected_total)
    assert rel_err < 1e-6, f"Pension total mismatch: actual={actual_total}, expected={expected_total}"
    print(f"  [single retired] total pension outflow = {actual_total:,.2f} (expected {expected_total:,.2f})")


def test_schema_compat_with_aal_analyses() -> None:
    policy = PensionPolicy()
    fund = PensionFund(policy=policy, start_date=date(2025, 1, 1))
    fund.add_cohort(Cohort("COHORT_1990", 1990, 200, 90_000.0, 80_000.0))
    fund.add_cohort(Cohort("COHORT_1970", 1970, 150, 110_000.0, 350_000.0))
    fund.add_cohort(Cohort("COHORT_1955", 1955, 80, 0.0, 600_000.0))

    cf = ClosedFundSimulator(fund).run(horizon_years=40)

    liq = LiquidityAnalysis(cf, freq="YE").results
    assert len(liq) > 0 and "netLiquidity" in liq.columns
    print(f"  [schema] LiquidityAnalysis returned {len(liq)} yearly buckets")

    val = ValueAnalysis(cf, as_of_date="2025-01-01", flat_rate=0.02)
    assert val.npv is not None
    print(f"  [schema] ValueAnalysis NPV (flat 2%) = {val.npv:,.2f}")


def main() -> None:
    print("Stage 1 closed-fund verification")
    print("-" * 60)
    print("Test 1: single active cohort, AGH recurrence")
    test_single_active_cohort()
    print()
    print("Test 2: single retired cohort, total outflow")
    test_single_retired_cohort()
    print()
    print("Test 3: schema compat with AAL analyses")
    test_schema_compat_with_aal_analyses()
    print()
    print("All Stage 1 checks passed.")


if __name__ == "__main__":
    main()
