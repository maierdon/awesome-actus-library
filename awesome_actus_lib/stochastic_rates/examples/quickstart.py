"""quickstart.py

Minimal end-to-end example for a third-party user.

What this example demonstrates
------------------------------
1) Build a curve calibrator (needed for no-arbitrage models Ho-Lee / Hull-White)
2) Instantiate exactly ONE short-rate model via the factory
3) Simulate Monte-Carlo short-rate paths
4) Convert one simulated path into an ACTUS-compatible ReferenceIndex (risk factor)
5) Run ONE ACTUS contract simulation using an ACTUS backend (PublicActusService)
6) Compute nominal value and NPV using ValueAnalysis

Requirements
------------
- Network access to an ACTUS engine.
  By default we use the public endpoint (PublicActusService).
  If you run your own engine, set ACTUS_SERVER_URL and we will use ActusService.

Notes
-----
- The ReferenceIndex generated from the short-rate path is used as the rate reset input.
- In this toy quickstart we also re-use it as the discount curve for ValueAnalysis.
  For stricter modelling you would generate a dedicated discount curve (spot rates / DFs)
  from the path and pass it under a different marketObjectCode.
"""

from __future__ import annotations

import os
import sys

# ---------------------------------------------------------------------------
# Path setup: Allow running from examples/ folder without package installation
# ---------------------------------------------------------------------------
try:
    from awesome_actus_lib.stochastic_rates import (
        CurveCalibrator,
        available_models,
        create_model,
        simulation_to_reference_index,
    )
    from awesome_actus_lib import PAM, ActusService, PublicActusService, ValueAnalysis
except ImportError:
    # Development mode: add project root to path
    _script_dir = os.path.dirname(os.path.abspath(__file__))
    _pkg_root = os.path.abspath(os.path.join(_script_dir, "../../../"))
    if _pkg_root not in sys.path:
        sys.path.insert(0, _pkg_root)

    from stochastic_rates import (
        CurveCalibrator,
        available_models,
        create_model,
        simulation_to_reference_index,
    )
    from awesome_actus_lib import PAM, ActusService, PublicActusService, ValueAnalysis


def get_service():
    """Use a custom ACTUS server if provided, else the public endpoint."""
    url = (os.getenv("ACTUS_SERVER_URL") or "").strip()
    return ActusService(serverURL=url) if url else PublicActusService()


def main():
    """Run the quickstart demonstration."""

    print("=" * 60)
    print("Stochastic Rates Extension - Quickstart Example")
    print("=" * 60)

    print("\nAvailable stochastic short-rate models:")
    for model_name in available_models():
        print(f"  - {model_name}")

    # -------------------------------------------------------------------------
    # 1) Market curve input (toy example with continuously-compounded spot rates)
    # -------------------------------------------------------------------------
    print("\n[1] Setting up market curve...")
    tenors_y = [0.25, 0.5, 1, 2, 5, 10]
    spot_rates = [0.006, 0.007, 0.009, 0.011, 0.014, 0.017]

    cal = CurveCalibrator.from_market(times=tenors_y, spot_rates=spot_rates)
    print(f"    Calibrated curve with {len(tenors_y)} tenors")
    print(f"    Short rate r(0) = {spot_rates[0]*100:.2f}%")
    print(f"    Long rate r(10y) = {spot_rates[-1]*100:.2f}%")

    # -------------------------------------------------------------------------
    # 2) Create ONE model (Hull-White: curve-fit + mean reversion)
    # -------------------------------------------------------------------------
    print("\n[2] Creating Hull-White model...")
    model = create_model(
        "hull_white",
        r0=spot_rates[0],
        a=0.10,           # mean reversion speed
        sigma=0.01,       # volatility (1%)
        calibrator=cal,
        seed=42           # for reproducibility
    )
    print(f"    Model: Hull-White")
    print(f"    Parameters: a={model.a}, sigma={model.sigma}")

    # -------------------------------------------------------------------------
    # 3) Simulate Monte Carlo paths
    # -------------------------------------------------------------------------
    print("\n[3] Running Monte Carlo simulation...")
    T_years = 5
    M = 12 * T_years  # monthly grid
    I = 50            # number of scenarios

    sim = model.simulate(T=float(T_years), M=M, I=I)

    print(f"    Horizon: {T_years} years")
    print(f"    Time steps: {M} (monthly)")
    print(f"    Scenarios: {I}")
    print(f"    Terminal rate mean: {sim.terminal_distribution.mean()*100:.3f}%")
    print(f"    Terminal rate std:  {sim.terminal_distribution.std()*100:.3f}%")

    # -------------------------------------------------------------------------
    # 4) Convert ONE path to an ACTUS ReferenceIndex
    # -------------------------------------------------------------------------
    print("\n[4] Converting to ACTUS ReferenceIndex...")
    base_date = "2025-01-01"
    curve_code = "CHF-SARON-3M"  # market object code for contract reference

    rf = simulation_to_reference_index(
        sim,
        base_date=base_date,
        market_code=curve_code,
        path=0,        # select first path (or loop over all)
        freq="M",      # monthly frequency
    )
    print(f"    Market code: {rf.marketObjectCode}")
    print(f"    Time series length: {len(rf.data)} points")

    # -------------------------------------------------------------------------
    # 5) Define ONE simple PAM floating-rate contract
    # -------------------------------------------------------------------------
    print("\n[5] Defining PAM floating-rate contract...")
    pam = PAM(
        contractDealDate=base_date,
        contractID="PAM_ASSET_001",
        contractRole="RPA",
        counterpartyID="CP_001",
        creatorID="ME_001",
        currency="CHF",
        dayCountConvention="A_360",
        statusDate=base_date,
        initialExchangeDate=base_date,
        maturityDate="2030-01-01",
        notionalPrincipal=1_000_000,
        nominalInterestRate=0.0,  # floater: use reset index + spread
        marketObjectCodeOfRateReset=curve_code,
        cycleAnchorDateOfRateReset=base_date,
        cycleOfRateReset="P3ML0",
        rateSpread=0.0020,  # +20bp spread
        cycleAnchorDateOfInterestPayment=base_date,
        cycleOfInterestPayment="P3ML0",
    )
    print(f"    Contract ID: {pam.contractID}")
    print(f"    Notional: CHF {pam.notionalPrincipal:,.0f}")
    print(f"    Maturity: {pam.maturityDate}")
    print(f"    Rate spread: {pam.rateSpread*10000:.0f} bp")

    # -------------------------------------------------------------------------
    # 6) Run ACTUS engine
    # -------------------------------------------------------------------------
    print("\n[6] Generating cash flows via ACTUS engine...")
    service = get_service()
    cf = service.generateEvents(pam, riskFactors=[rf])
    print(f"    Generated {len(cf)} cash flow events")

    # -------------------------------------------------------------------------
    # 7) Present Value calculation using ValueAnalysis
    # -------------------------------------------------------------------------
    print("\n[7] Computing present value...")
    va = ValueAnalysis(cf_stream=cf, as_of_date=base_date, discount_curve_code=curve_code)

    print("\n" + "=" * 60)
    print("ValueAnalysis Summary")
    print("=" * 60)
    print(va.summarize())

    print("\n[Done] Quickstart completed successfully!")
    print("       For full ALM analysis, see: thesis_alm_example.py")


if __name__ == "__main__":
    main()