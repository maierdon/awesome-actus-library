"""
thesis_alm_example_extended.py
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple

from awesome_actus_lib import (
    PAM, ANN, Portfolio,
    YieldCurve, PublicActusService,
    ValueAnalysis, ReferenceIndex
)

from stochastic_rates import (
    CurveCalibrator,
    create_model,
    available_models,
    simulation_to_reference_index
)

# =============================================================================
# CONFIGURATION
# =============================================================================
OUTPUT_DIR = "thesis_plots"
SAVE_PLOTS = True
SEED = 42
N_SCENARIOS = 500

if SAVE_PLOTS and not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# =============================================================================
# 1. PORTFOLIO DEFINITION
# =============================================================================
print("=" * 70)
print("EXTENDED CASE STUDY: Deterministic vs Stochastic Risk Analysis")
print("=" * 70)

print("\n[1] Portfolio Definition")
print("-" * 40)

ptf = Portfolio([
    PAM(
        contractID="ASSET_FLOATER_01",
        statusDate="2024-12-31T00:00:00",
        contractDealDate="2024-12-31T00:00:00",
        currency="CHF",
        notionalPrincipal=10_000_000,
        initialExchangeDate="2025-01-01T00:00:00",
        maturityDate="2035-01-01T00:00:00",
        nominalInterestRate=0.0,
        dayCountConvention="30E360",
        contractRole="RPA",
        cycleAnchorDateOfRateReset="2025-01-01T00:00:00",
        cycleOfRateReset="P1YL0",
        marketObjectCodeOfRateReset="IR_SCENARIO",
        rateSpread=0.0080,
        cycleAnchorDateOfInterestPayment="2026-01-01T00:00:00",
        cycleOfInterestPayment="P1YL0",
        counterpartyID="Bank-01",
        creatorID="PensionFund-01"
    ),
    ANN(
        contractID="LIAB_ANNUITY_01",
        statusDate="2025-01-01T00:00:00",
        contractDealDate="2025-01-01T00:00:00",
        currency="CHF",
        notionalPrincipal=8_000_000,
        initialExchangeDate="2025-01-02T00:00:00",
        maturityDate="2035-01-01T00:00:00",
        nominalInterestRate=0.015,
        dayCountConvention="30E360",
        contractRole="RPL",
        cycleAnchorDateOfInterestPayment="2025-02-01T00:00:00",
        cycleOfInterestPayment="P1ML0",
        cycleAnchorDateOfPrincipalRedemption="2025-02-01T00:00:00",
        cycleOfPrincipalRedemption="P1ML0",
        counterpartyID="Bank-01",
        creatorID="PensionFund-01"
    )
])

print(f"  Asset:     CHF 10,000,000 floating-rate bond (PAM)")
print(f"  Liability: CHF 8,000,000 annuity (ANN)")

service = PublicActusService()

# =============================================================================
# 2. MARKET DATA
# =============================================================================
print("\n[2] Market Data & Calibration")
print("-" * 40)

BASE_DATE = "2025-01-01"
MARKET_CODE = "IR_SCENARIO"

# Base curve
curve_tenors = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
curve_rates_base = [0.020, 0.022, 0.024, 0.025, 0.026, 0.027, 0.028, 0.0285, 0.029, 0.030]
r0 = 0.02

yield_curve_base = YieldCurve(
    marketObjectCode="DISCOUNT_CURVE",
    referenceDate=BASE_DATE,
    tenors=["1Y", "2Y", "3Y", "4Y", "5Y", "6Y", "7Y", "8Y", "9Y", "10Y"],
    rates=curve_rates_base
)

calib = CurveCalibrator.from_market(
    times=np.array(curve_tenors, dtype=float),
    spot_rates=np.array(curve_rates_base, dtype=float)
)

print(f"  Base curve: 2.0% (1Y) to 3.0% (10Y)")

# Helper function for NPV calculation
def calc_npv(portfolio, risk_factors) -> float:
    """Calculate portfolio NPV given risk factors."""
    events = service.generateEvents(portfolio, riskFactors=risk_factors)
    val = ValueAnalysis(events, discount_curve_code="DISCOUNT_CURVE")
    return float(val.npv)

def create_reference_index(rates: List[float], shift_bp: float = 0) -> ReferenceIndex:
    """Create a ReferenceIndex with optional parallel shift."""
    _base_dt = pd.to_datetime(BASE_DATE)
    shifted_rates = [r + shift_bp / 10000 for r in rates]

    base_years = [0] + curve_tenors
    base_dates = [(_base_dt + pd.DateOffset(years=y)).strftime("%Y-%m-%d") for y in base_years]
    base_values = [r0 + shift_bp / 10000] + shifted_rates

    return ReferenceIndex(
        marketObjectCode=MARKET_CODE,
        source=pd.DataFrame({"date": base_dates, "value": base_values})
    )

# =============================================================================
# 3. DETERMINISTIC BENCHMARK (Parallel Shifts)
# =============================================================================
print("\n[3] Deterministic Benchmark: Parallel Shift Analysis")
print("-" * 40)

# Base NPV
rf_base = create_reference_index(curve_rates_base, shift_bp=0)
npv_base = calc_npv(ptf, [rf_base, yield_curve_base])
print(f"  Base NPV: {npv_base:,.0f} CHF")

# Parallel shifts
shifts_bp = [-200, -100, -50, 0, +50, +100, +200]
deterministic_results = {}

print("\n  Parallel Shift Analysis:")
print("  " + "-" * 50)
print(f"  {'Shift (bp)':<12} {'NPV (CHF)':<18} {'Change vs Base':<15}")
print("  " + "-" * 50)

for shift in shifts_bp:
    rf_shifted = create_reference_index(curve_rates_base, shift_bp=shift)

    # Also shift discount curve for consistency
    shifted_discount_rates = [r + shift / 10000 for r in curve_rates_base]
    yc_shifted = YieldCurve(
        marketObjectCode="DISCOUNT_CURVE",
        referenceDate=BASE_DATE,
        tenors=["1Y", "2Y", "3Y", "4Y", "5Y", "6Y", "7Y", "8Y", "9Y", "10Y"],
        rates=shifted_discount_rates
    )

    npv = calc_npv(ptf, [rf_shifted, yc_shifted])
    deterministic_results[shift] = npv
    change = npv - npv_base
    print(f"  {shift:+4d} bp       {npv:>15,.0f}    {change:>+15,.0f}")

print("  " + "-" * 50)

# Calculate deterministic range
det_min = min(deterministic_results.values())
det_max = max(deterministic_results.values())
det_range = det_max - det_min
print(f"\n  Deterministic Range (±200bp): {det_range:,.0f} CHF")
print(f"  Min NPV (-200bp): {det_min:,.0f} CHF")
print(f"  Max NPV (+200bp): {det_max:,.0f} CHF")

# =============================================================================
# 4. STOCHASTIC ANALYSIS (Hull-White)
# =============================================================================
print("\n[4] Stochastic Analysis: Hull-White Model")
print("-" * 40)

# Model parameters
sigma = 0.01
a = 0.15
T_horizon = 10

print(f"  Model: Hull-White (a={a}, σ={sigma})")
print(f"  Scenarios: {N_SCENARIOS}")
print(f"  Horizon: {T_horizon} years")
print(f"  Seed: {SEED}")

# Create and simulate
hw_model = create_model("hull_white", r0=r0, a=a, sigma=sigma, calibrator=calib)
rng = np.random.default_rng(SEED)
sim_hw = hw_model.simulate(T=float(T_horizon), M=T_horizon * 12, I=N_SCENARIOS, rng=rng)

# Convert to ACTUS and calculate NPVs
print(f"\n  Calculating {N_SCENARIOS} scenario NPVs...")
npv_stochastic = []

for i in range(N_SCENARIOS):
    if (i + 1) % 100 == 0:
        print(f"    Progress: {i+1}/{N_SCENARIOS}")

    rf = simulation_to_reference_index(sim_hw, base_date=BASE_DATE,
                                        market_code=MARKET_CODE, path=i, freq="M")
    npv = calc_npv(ptf, [rf, yield_curve_base])
    npv_stochastic.append(npv)

npv_stochastic = np.array(npv_stochastic)

# Statistics
mean_npv = np.mean(npv_stochastic)
std_npv = np.std(npv_stochastic, ddof=1)
p1 = np.percentile(npv_stochastic, 1)
p5 = np.percentile(npv_stochastic, 5)
p95 = np.percentile(npv_stochastic, 95)
p99 = np.percentile(npv_stochastic, 99)

# VaR/ES (loss relative to base)
losses = npv_base - npv_stochastic
var_95 = np.percentile(losses, 95)
var_99 = np.percentile(losses, 99)
es_95 = np.mean(losses[losses >= var_95])
es_99 = np.mean(losses[losses >= var_99])

print(f"\n  Stochastic Results (Hull-White):")
print(f"  " + "-" * 40)
print(f"  Mean NPV:        {mean_npv:>15,.0f} CHF")
print(f"  Std Dev:         {std_npv:>15,.0f} CHF")
print(f"  1st Percentile:  {p1:>15,.0f} CHF")
print(f"  5th Percentile:  {p5:>15,.0f} CHF")
print(f"  95th Percentile: {p95:>15,.0f} CHF")
print(f"  99th Percentile: {p99:>15,.0f} CHF")
print(f"  " + "-" * 40)
print(f"  VaR 95%:         {var_95:>15,.0f} CHF")
print(f"  VaR 99%:         {var_99:>15,.0f} CHF")
print(f"  ES 95%:          {es_95:>15,.0f} CHF")
print(f"  ES 99%:          {es_99:>15,.0f} CHF")

stoch_range = p99 - p1
print(f"\n  Stochastic Range (1%-99%): {stoch_range:,.0f} CHF")

# =============================================================================
# 5. MODEL COMPARISON (All 4 Models)
# =============================================================================
print("\n[5] Model Comparison: All 4 Short-Rate Models")
print("-" * 40)

model_configs = {
    'Vasicek': {'name': 'vasicek', 'params': {'r0': r0, 'a': 0.15, 'b': 0.025, 'sigma': 0.012}},
    'CIR': {'name': 'cir', 'params': {'r0': max(r0, 0.001), 'a': 0.15, 'b': 0.025, 'sigma': 0.03}},
    'Ho-Lee': {'name': 'ho_lee', 'params': {'r0': r0, 'sigma': 0.01, 'calibrator': calib}},
    'Hull-White': {'name': 'hull_white', 'params': {'r0': r0, 'a': 0.15, 'sigma': 0.01, 'calibrator': calib}},
}

model_results = {}
n_comparison = 200  # Fewer scenarios for comparison (speed)

for model_label, config in model_configs.items():
    print(f"  Processing {model_label}...")

    model = create_model(config['name'], **config['params'])
    rng = np.random.default_rng(SEED)
    sim = model.simulate(T=float(T_horizon), M=T_horizon * 12, I=n_comparison, rng=rng)

    npvs = []
    for i in range(n_comparison):
        rf = simulation_to_reference_index(sim, base_date=BASE_DATE,
                                           market_code=MARKET_CODE, path=i, freq="M")
        npv = calc_npv(ptf, [rf, yield_curve_base])
        npvs.append(npv)

    npvs = np.array(npvs)
    losses = npv_base - npvs

    model_results[model_label] = {
        'npvs': npvs,
        'mean': np.mean(npvs),
        'std': np.std(npvs, ddof=1),
        'p5': np.percentile(npvs, 5),
        'p95': np.percentile(npvs, 95),
        'var_95': np.percentile(losses, 95),
        'es_95': np.mean(losses[losses >= np.percentile(losses, 95)]),
    }

# Print comparison table
print("\n  Model Comparison Table:")
print("  " + "-" * 75)
print(f"  {'Model':<12} {'Mean NPV':>14} {'Std Dev':>12} {'VaR 95%':>12} {'ES 95%':>12} {'Range':>12}")
print("  " + "-" * 75)
for label, res in model_results.items():
    range_val = res['p95'] - res['p5']
    print(f"  {label:<12} {res['mean']:>14,.0f} {res['std']:>12,.0f} {res['var_95']:>12,.0f} {res['es_95']:>12,.0f} {range_val:>12,.0f}")
print("  " + "-" * 75)

# =============================================================================
# 6. COMPARISON SUMMARY
# =============================================================================
print("\n[6] Key Comparison: Deterministic vs Stochastic")
print("-" * 40)

print(f"""
  DETERMINISTIC (Parallel Shifts ±200bp):
    Range:        {det_range:>12,.0f} CHF
    Scenarios:    {len(shifts_bp):>12} discrete shifts
    Information:  Point estimates only
    
  STOCHASTIC (Hull-White, {N_SCENARIOS} scenarios):
    Range (1-99%): {stoch_range:>12,.0f} CHF
    VaR 95%:       {var_95:>12,.0f} CHF
    ES 95%:        {es_95:>12,.0f} CHF
    Information:  Full distribution + tail risk
    
  KEY INSIGHT:
    The stochastic approach captures path-dependent effects and 
    provides tail risk measures (VaR, ES) that are not available
    from simple parallel shift analysis.
""")

# =============================================================================
# FIGURE 7.4: DETERMINISTIC VS STOCHASTIC COMPARISON
# =============================================================================
print("\n--- Generating Figure 7.4: Deterministic vs Stochastic ---")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Left: Deterministic parallel shifts
ax1 = axes[0]
shifts = list(deterministic_results.keys())
npvs_det = [deterministic_results[s] / 1e6 for s in shifts]
colors = ['red' if s < 0 else 'green' if s > 0 else 'gray' for s in shifts]

bars = ax1.bar(range(len(shifts)), npvs_det, color=colors, alpha=0.7, edgecolor='black')
ax1.axhline(npv_base / 1e6, color='blue', linestyle='--', linewidth=2, label='Base NPV')
ax1.set_xticks(range(len(shifts)))
ax1.set_xticklabels([f'{s:+d}bp' for s in shifts])
ax1.set_xlabel('Parallel Shift')
ax1.set_ylabel('NPV (Million CHF)')
ax1.set_title('Deterministic: Parallel Shift Scenarios')
ax1.legend()
ax1.grid(True, alpha=0.3, axis='y')

# Right: Stochastic distribution
ax2 = axes[1]
ax2.hist(npv_stochastic / 1e6, bins=30, color='steelblue', alpha=0.7,
         edgecolor='black', density=True, label='Stochastic NPVs')
ax2.axvline(npv_base / 1e6, color='blue', linestyle='--', linewidth=2, label='Base NPV')
ax2.axvline(p5 / 1e6, color='red', linestyle=':', linewidth=2, label=f'5th Pctl')
ax2.axvline(p95 / 1e6, color='green', linestyle=':', linewidth=2, label=f'95th Pctl')
ax2.set_xlabel('NPV (Million CHF)')
ax2.set_ylabel('Density')
ax2.set_title(f'Stochastic: Hull-White ({N_SCENARIOS} scenarios)')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
if SAVE_PLOTS:
    plt.savefig(os.path.join(OUTPUT_DIR, 'deterministic_vs_stochastic.png'), dpi=300, bbox_inches='tight')
    print(f"  Saved: {OUTPUT_DIR}/deterministic_vs_stochastic.png")
plt.show()

# =============================================================================
# FIGURE 7.5: MODEL COMPARISON (4 Models)
# =============================================================================
print("\n--- Generating Figure 7.5: Model Comparison ---")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

colors = {'Vasicek': 'blue', 'CIR': 'green', 'Ho-Lee': 'purple', 'Hull-White': 'red'}

for idx, (label, res) in enumerate(model_results.items()):
    ax = axes[idx]
    color = colors[label]

    ax.hist(res['npvs'] / 1e6, bins=25, color=color, alpha=0.7, edgecolor='black')
    ax.axvline(npv_base / 1e6, color='black', linestyle='--', linewidth=2, label='Base NPV')
    ax.axvline(res['mean'] / 1e6, color=color, linestyle='-', linewidth=2, label='Mean')
    ax.axvline(res['p5'] / 1e6, color='darkred', linestyle=':', linewidth=1.5, label='5th Pctl')

    # Stats box
    stats_text = f"Mean: {res['mean']/1e6:.2f}M\nStd: {res['std']/1e3:.0f}k\nVaR95: {res['var_95']/1e3:.0f}k"
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, verticalalignment='top',
            fontsize=9, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    ax.set_xlabel('NPV (Million CHF)')
    ax.set_ylabel('Frequency')
    ax.set_title(f'{label} Model')
    ax.legend(loc='upper right', fontsize=8)
    ax.grid(True, alpha=0.3, axis='y')

plt.suptitle('Model Comparison: NPV Distributions Across All Models', fontsize=14, fontweight='bold')
plt.tight_layout()
if SAVE_PLOTS:
    plt.savefig(os.path.join(OUTPUT_DIR, 'model_comparison_npv.png'), dpi=300, bbox_inches='tight')
    print(f"  Saved: {OUTPUT_DIR}/model_comparison_npv.png")
plt.show()

# =============================================================================
# FIGURE 7.6: RISK METRICS COMPARISON
# =============================================================================
print("\n--- Generating Figure 7.6: Risk Metrics Comparison ---")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

models = list(model_results.keys())
x = np.arange(len(models))
width = 0.35

# Left: VaR comparison
ax1 = axes[0]
var_values = [model_results[m]['var_95'] / 1000 for m in models]
es_values = [model_results[m]['es_95'] / 1000 for m in models]

bars1 = ax1.bar(x - width/2, var_values, width, label='VaR 95%', color='orange', edgecolor='black')
bars2 = ax1.bar(x + width/2, es_values, width, label='ES 95%', color='darkred', edgecolor='black')

ax1.set_xlabel('Model')
ax1.set_ylabel('Risk Measure (thousand CHF)')
ax1.set_title('Tail Risk Comparison: VaR and ES')
ax1.set_xticks(x)
ax1.set_xticklabels(models)
ax1.legend()
ax1.grid(True, alpha=0.3, axis='y')

# Right: Standard deviation comparison
ax2 = axes[1]
std_values = [model_results[m]['std'] / 1000 for m in models]
bar_colors = [colors[m] for m in models]

ax2.bar(models, std_values, color=bar_colors, alpha=0.7, edgecolor='black')
ax2.set_xlabel('Model')
ax2.set_ylabel('Standard Deviation (thousand CHF)')
ax2.set_title('Volatility Comparison: NPV Standard Deviation')
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
if SAVE_PLOTS:
    plt.savefig(os.path.join(OUTPUT_DIR, 'risk_metrics_comparison.png'), dpi=300, bbox_inches='tight')
    print(f"  Saved: {OUTPUT_DIR}/risk_metrics_comparison.png")
plt.show()

# =============================================================================
# LATEX TABLE OUTPUT
# =============================================================================
print("\n" + "=" * 70)
print("LATEX TABLES FOR THESIS")
print("=" * 70)

# Table 7.1: Deterministic Results
print("\n% TABLE 7.1: Deterministic Parallel Shift Analysis")
print("\\begin{table}[htbp]")
print("    \\centering")
print("    \\caption{Deterministic scenario analysis: Portfolio NPV under parallel yield curve shifts.}")
print("    \\label{tab:deterministic-shifts}")
print("    \\begin{tabular}{@{}r r r@{}}")
print("        \\toprule")
print("        \\textbf{Shift (bp)} & \\textbf{NPV (CHF)} & \\textbf{Change vs Base} \\\\")
print("        \\midrule")
for shift in shifts_bp:
    npv = deterministic_results[shift]
    change = npv - npv_base
    print(f"        {shift:+4d} & {npv:,.0f} & {change:+,.0f} \\\\")
print("        \\bottomrule")
print("    \\end{tabular}")
print("\\end{table}")

# Table 7.2: Stochastic Results
print("\n% TABLE 7.2: Stochastic Analysis Results")
print("\\begin{table}[htbp]")
print("    \\centering")
print("    \\caption{Stochastic scenario analysis: Portfolio risk metrics under Hull--White simulation")
print(f"             ($I={N_SCENARIOS}$, $T=10$y, seed=42).}}")
print("    \\label{tab:stochastic-results}")
print("    \\begin{tabular}{@{}l r@{}}")
print("        \\toprule")
print("        \\textbf{Metric} & \\textbf{Value (CHF)} \\\\")
print("        \\midrule")
print(f"        Deterministic NPV (Base) & {npv_base:,.0f} \\\\")
print(f"        Scenario Mean NPV & {mean_npv:,.0f} \\\\")
print(f"        Standard Deviation & {std_npv:,.0f} \\\\")
print("        \\midrule")
print(f"        5th Percentile & {p5:,.0f} \\\\")
print(f"        95th Percentile & {p95:,.0f} \\\\")
print("        \\midrule")
print(f"        VaR 95\\% & {var_95:,.0f} \\\\")
print(f"        VaR 99\\% & {var_99:,.0f} \\\\")
print(f"        ES 95\\% & {es_95:,.0f} \\\\")
print(f"        ES 99\\% & {es_99:,.0f} \\\\")
print("        \\bottomrule")
print("    \\end{tabular}")
print("\\end{table}")

# Table 7.3: Model Comparison
print("\n% TABLE 7.3: Model Comparison")
print("\\begin{table}[htbp]")
print("    \\centering")
print(f"    \\caption{{Model comparison: Risk metrics across all four short-rate models ($I={n_comparison}$, $T=10$y).}}")
print("    \\label{tab:model-comparison}")
print("    \\begin{tabular}{@{}l r r r r@{}}")
print("        \\toprule")
print("        \\textbf{Model} & \\textbf{Mean NPV} & \\textbf{Std Dev} & \\textbf{VaR 95\\%} & \\textbf{ES 95\\%} \\\\")
print("        \\midrule")
for label, res in model_results.items():
    print(f"        {label} & {res['mean']:,.0f} & {res['std']:,.0f} & {res['var_95']:,.0f} & {res['es_95']:,.0f} \\\\")
print("        \\bottomrule")
print("    \\end{tabular}")
print("\\end{table}")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("CASE STUDY COMPLETED")
print("=" * 70)
print(f"\nPlots saved to: {OUTPUT_DIR}/")
print("  - deterministic_vs_stochastic.png (Figure 7.4)")
print("  - model_comparison_npv.png (Figure 7.5)")
print("  - risk_metrics_comparison.png (Figure 7.6)")
print("\nCopy the LaTeX tables above into your thesis Chapter 7.")