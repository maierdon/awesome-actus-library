"""
generate_thesis_plots.py
"""

from __future__ import annotations

import os
import sys
import time
import argparse
from dataclasses import dataclass
from typing import Iterable, Optional, Sequence, Tuple, Dict, Any

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.patches as mpatches
import pandas as pd
try:
    from scipy import stats
except Exception:
    stats = None

# AAL imports
ACTUS_AVAILABLE = False

try:
    from awesome_actus_lib import (
        PAM, ANN, ActusService, PublicActusService, ValueAnalysis,
    )
    from awesome_actus_lib.stochastic_rates import (
        CurveCalibrator, create_model, simulation_to_reference_index,
    )
    ACTUS_AVAILABLE = True
except ImportError:
    pass

if not ACTUS_AVAILABLE:
    try:
        _script_dir = os.path.dirname(os.path.abspath(__file__))
        _pkg_root = os.path.abspath(os.path.join(_script_dir, "../../../"))
        if _pkg_root not in sys.path:
            sys.path.insert(0, _pkg_root)
        for mod in list(sys.modules.keys()):
            if mod.startswith("awesome_actus_lib"):
                del sys.modules[mod]
        from awesome_actus_lib.stochastic_rates import (
            CurveCalibrator, create_model, simulation_to_reference_index,
        )
        print(f" Using local package from {_pkg_root}")
    except ImportError as e:
        print(f" Warning: Could not import stochastic_rates modules: {e}")
        CurveCalibrator = None
        create_model = None


# =============================================================================
# CONFIGURATION & STYLING
# =============================================================================
try:
    plt.style.use('seaborn-v0_8-whitegrid')
except OSError:
    try:
        plt.style.use('seaborn-whitegrid')
    except OSError:
        plt.style.use('ggplot')

plt.rcParams.update({
    'figure.figsize': (12, 7),
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 13,
    'axes.titleweight': 'bold',
    'legend.fontsize': 9,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'figure.dpi': 100,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})

SAVE_PLOTS = False
OUTPUT_DIR = "thesis_plots"


def configure_output(save: bool = False, save_only: bool = False):
    """Configure whether to save/display plots."""
    global SAVE_PLOTS
    SAVE_PLOTS = save or save_only
    if SAVE_PLOTS and not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"✓ Created output directory: {OUTPUT_DIR}/")
    plt.ioff()


def show_and_save(fig, filename: str):
    """Helper to show and/or save a figure."""
    if SAVE_PLOTS:
        filepath = os.path.join(OUTPUT_DIR, filename)
        fig.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"  ✓ Saved: {filepath}")
    if not plt.isinteractive():
        plt.show()
    else:
        plt.show(block=True)


# =============================================================================
# HELPERS
# =============================================================================
def make_toy_curve() -> Tuple[np.ndarray, np.ndarray]:
    """Create CHF-like spot curve."""
    tenors_y = np.array([0.25, 0.5, 1, 2, 5, 10, 20, 30], dtype=float)
    spot = np.array([0.006, 0.007, 0.009, 0.011, 0.014, 0.017, 0.020, 0.021], dtype=float)
    return tenors_y, spot


def print_section_header(title: str, chapter: str = ""):
    """Print formatted section header."""
    print("\n" + "="*80)
    if chapter:
        print(f"{chapter} | {title}")
    else:
        print(title)
    print("="*80)


def _rng(seed: int, tag: str = "") -> np.random.Generator:
    """Deterministic RNG."""
    if tag:
        child = np.random.SeedSequence([int(seed), abs(hash(tag)) % (2**32)])
        return np.random.default_rng(child)
    return np.random.default_rng(int(seed))


def _zcb_price_call(model, t: float, T: float, r_t: Optional[float] = None) -> float:
    """Call model.zcb_price with various signatures."""
    f = getattr(model, "zcb_price", None)
    if f is None:
        raise AttributeError("Model has no zcb_price method.")
    tries = [
        lambda: f(t, T, r_t),
        lambda: f(t=t, T=T, r_t=r_t),
        lambda: f(t, T),
    ]
    for call in tries:
        try:
            return float(call())
        except TypeError:
            continue
    if t == 0.0 and r_t is None:
        cal = getattr(model, "calibrator", None) or getattr(model, "cal", None)
        if cal is not None and hasattr(cal, "zcb_price"):
            return float(cal.zcb_price(float(T)))
    raise TypeError("Could not call zcb_price with supported signatures.")


def _zero_yield_from_zcb(P: float, tau: float) -> float:
    """Continuously-compounded zero yield."""
    tau = float(tau)
    if tau <= 0.0:
        return np.nan
    return float(-np.log(float(P)) / tau)


def zcb_mc_estimate_from_sim(sim, T: float) -> Tuple[float, float]:
    """Estimate ZCB price via Monte Carlo from simulation result."""
    dt = sim.horizon / sim.n_steps
    D = np.exp(-np.sum(sim.rates[:-1, :], axis=0) * dt)
    return float(np.mean(D)), float(np.std(D, ddof=1) / np.sqrt(sim.n_paths))


def zcb_reference_price(model, T: float, calibrator=None) -> float:
    """Get analytical ZCB price."""
    T = float(T)
    if calibrator is not None and hasattr(calibrator, "zcb_price"):
        try:
            return float(calibrator.zcb_price(T))
        except TypeError:
            pass
    if not hasattr(model, "zcb_price"):
        raise AttributeError("Model has no zcb_price method.")
    f = model.zcb_price
    tries = [lambda: f(T), lambda: f(T=T), lambda: f(0.0, T), lambda: f(t=0.0, T=T)]
    for call in tries:
        try:
            return float(call())
        except TypeError:
            continue
    raise TypeError("Could not call zcb_price with any known signature.")


# =============================================================================
# CHAPTER 2: Theoretical Foundation
# =============================================================================
def plot_vasicek_vs_cir_comparison():
    """
    VASICEK VS CIR COMPARISON
    Output: vasicek_vs_cir.png
    LaTeX: Chapter 2, Figure 2.1
    """
    print_section_header("Vasicek vs CIR Comparison", "Chapter 2")

    tenors_y, spot = make_toy_curve()

    vasicek = create_model("vasicek", r0=float(spot[0]), a=0.15, b=0.025, sigma=0.012)
    cir = create_model("cir", r0=max(float(spot[0]), 0.001), a=0.15, b=0.025, sigma=0.02)

    rng = np.random.default_rng(42)
    sim_v = vasicek.simulate(T=10.0, M=120, I=50, rng=rng)
    sim_c = cir.simulate(T=10.0, M=120, I=50, rng=rng)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    for i in range(min(20, sim_v.n_paths)):
        axes[0].plot(sim_v.times, sim_v.rates[:, i], linewidth=0.8, alpha=0.6)
    axes[0].axhline(0, color='red', linestyle='--', linewidth=2)
    axes[0].set_title("Vasicek Model (can produce negative rates)")
    axes[0].set_xlabel("Time (years)")
    axes[0].set_ylabel("Short rate r(t)")
    axes[0].grid(True, alpha=0.3)

    for i in range(min(20, sim_c.n_paths)):
        axes[1].plot(sim_c.times, sim_c.rates[:, i], linewidth=0.8, alpha=0.6)
    axes[1].axhline(0, color='red', linestyle='--', linewidth=2)
    axes[1].set_title("CIR Model (non-negative rates)")
    axes[1].set_xlabel("Time (years)")
    axes[1].set_ylabel("Short rate r(t)")
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    show_and_save(fig, 'vasicek_vs_cir.png')


def plot_all_models_comparison():
    """
    ALL 4 MODELS COMPARISON
    Output: all_models_comparison.png
    LaTeX: Chapter 2, Figure 2.2
    """
    print_section_header("All Models Comparison", "Chapter 2")

    tenors_y, spot = make_toy_curve()
    cal = CurveCalibrator.from_market(tenors_y, spot_rates=spot)

    models = {
        'Vasicek': {'model': create_model("vasicek", r0=spot[0], a=0.15, b=0.025, sigma=0.012), 'color': 'blue'},
        'CIR': {'model': create_model("cir", r0=max(spot[0], 0.001), a=0.15, b=0.025, sigma=0.02), 'color': 'green'},
        'Ho-Lee': {'model': create_model("ho_lee", r0=spot[0], sigma=0.01, calibrator=cal), 'color': 'purple'},
        'Hull-White': {'model': create_model("hull_white", r0=spot[0], a=0.1, sigma=0.01, calibrator=cal), 'color': 'red'}
    }

    rng = np.random.default_rng(42)
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    for idx, (name, config) in enumerate(models.items()):
        model = config['model']
        color = config['color']
        sim = model.simulate(T=10.0, M=120, I=1000, rng=rng)

        for i in range(min(30, sim.n_paths)):
            axes[idx].plot(sim.times, sim.rates[:, i] * 100, alpha=0.1, linewidth=0.5, color=color)

        mean_rate = np.mean(sim.rates, axis=1) * 100
        axes[idx].plot(sim.times, mean_rate, 'k-', linewidth=2, label='Mean')

        terminal_rates = sim.rates[-1, :] * 100
        stats_text = f'Mean: {np.mean(terminal_rates):.2f}%\nStd: {np.std(terminal_rates):.2f}%'
        if name in ['Vasicek', 'Hull-White']:
            neg_prob = np.mean(terminal_rates < 0)
            stats_text += f'\nP(neg): {neg_prob:.1%}'

        axes[idx].text(0.02, 0.98, stats_text, transform=axes[idx].transAxes,
                       verticalalignment='top', fontsize=9,
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

        axes[idx].set_title(f'{name} Model', fontweight='bold')
        axes[idx].set_xlabel('Time (years)')
        axes[idx].set_ylabel('Rate (%)')
        axes[idx].legend(loc='upper right')
        axes[idx].grid(True, alpha=0.3)

    plt.suptitle('Comparison of All Implemented Short-Rate Models', fontsize=16, fontweight='bold')
    plt.tight_layout()
    show_and_save(fig, 'all_models_comparison.png')


# =============================================================================
# CHAPTER 5: Implementation - Curve Calibration
# =============================================================================
def plot_curve_calibration(tenors_y: np.ndarray, spot: np.ndarray, grid_max: float = 35.0):
    """
    CURVE CALIBRATION
    Output: curve_calibration.png
    LaTeX: Chapter 5, Figure 5.1
    """
    print_section_header("Curve Calibration", "Chapter 5")

    cal = CurveCalibrator.from_market(tenors_y, spot_rates=spot)

    t = np.linspace(0.01, grid_max, 800)
    R = np.array([cal.spot_rate(float(tt)) for tt in t])
    F = np.array([cal.forward_rate(float(tt)) for tt in t])
    P = np.array([cal.zcb_price(float(tt)) for tt in t])

    fig = plt.figure(figsize=(16, 5))
    gs = GridSpec(1, 3, figure=fig, wspace=0.3)

    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(t, R * 100, 'b-', linewidth=2, label='Calibrated R(0,t)')
    ax1.scatter(tenors_y, spot * 100, s=80, c='red', zorder=5, label='Market Input', edgecolors='black')
    ax1.axvline(tenors_y[-1], color='gray', linestyle='--', alpha=0.5, label=f'Last Tenor ({tenors_y[-1]:.0f}y)')
    ax1.set_xlabel('Maturity (years)')
    ax1.set_ylabel('Spot Rate (%)')
    ax1.set_title('Spot Rate Curve R(0,t)')
    ax1.legend(loc='best')
    ax1.grid(True, alpha=0.3)

    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(t, F * 100, 'g-', linewidth=2, label='Forward F(0,t)')
    ax2.axvline(tenors_y[-1], color='gray', linestyle='--', alpha=0.5)
    ax2.set_xlabel('Maturity (years)')
    ax2.set_ylabel('Forward Rate (%)')
    ax2.set_title('Instantaneous Forward Rate F(0,t)')
    ax2.legend(loc='best')
    ax2.grid(True, alpha=0.3)

    ax3 = fig.add_subplot(gs[0, 2])
    ax3.plot(t, P, 'purple', linewidth=2, label='Discount P(0,t)')
    ax3.axvline(tenors_y[-1], color='gray', linestyle='--', alpha=0.5)
    ax3.set_xlabel('Maturity (years)')
    ax3.set_ylabel('Discount Factor')
    ax3.set_title('Zero-Coupon Bond Prices P(0,t)')
    ax3.legend(loc='best')
    ax3.grid(True, alpha=0.3)

    show_and_save(fig, 'curve_calibration.png')
    return cal


def plot_theta_drift(calibrator, T: float = 10.0):
    """
    THETA DRIFT COMPARISON
    Output: theta_drift.png
    LaTeX: Chapter 5, Figure 5.2
    """
    print_section_header("Theta Drift Comparison", "Chapter 5")

    tenors_y, spot = make_toy_curve()

    ho_lee = create_model("ho_lee", r0=spot[0], sigma=0.01, calibrator=calibrator)
    hull_white = create_model("hull_white", r0=spot[0], a=0.1, sigma=0.01, calibrator=calibrator)

    t = np.linspace(0.01, T, 240)
    th_holee = np.array([float(ho_lee.theta(float(tt))) for tt in t])
    th_hw = np.array([float(hull_white.theta(float(tt))) for tt in t])

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    axes[0].plot(t, th_holee, 'purple', linewidth=2)
    axes[0].axhline(0, color='gray', linestyle='--', alpha=0.5)
    axes[0].fill_between(t, 0, th_holee, alpha=0.2, color='purple')
    axes[0].set_xlabel('Time t (years)')
    axes[0].set_ylabel('θ(t)')
    axes[0].set_title('Ho-Lee: θ(t) = ∂f(0,t)/∂t + σ²t')
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(t, th_hw, 'red', linewidth=2)
    axes[1].axhline(0, color='gray', linestyle='--', alpha=0.5)
    axes[1].fill_between(t, 0, th_hw, alpha=0.2, color='red')
    axes[1].set_xlabel('Time t (years)')
    axes[1].set_ylabel('θ(t)')
    axes[1].set_title('Hull-White: θ(t) = ∂f/∂t + af(0,t) + σ²(1-e^{-2at})/(2a)')
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    show_and_save(fig, 'theta_drift.png')


# =============================================================================
# CHAPTER 6: Validation
# =============================================================================
def table_zcb_benchmark(model, maturities: Sequence[float], M_per_year: int = 12,
                        I: int = 50_000, seed: int = 42):
    """
    ZCB VALIDATION TABLE AND PLOT
    Output: zcb_validation.png
    LaTeX: Chapter 6, Table 6.1 + Figure 6.1
    """
    print_section_header("ZCB Pricing Validation", "Chapter 6")
    print(f"  Running with I={I:,} scenarios per maturity...")

    rng = np.random.default_rng(seed)
    rows = []

    for T in maturities:
        M = int(M_per_year * T)
        sim = model.simulate(T=float(T), M=M, I=I, rng=rng)
        P_hat, SE = zcb_mc_estimate_from_sim(sim, T=float(T))
        P_ana = zcb_reference_price(model, float(T), calibrator=getattr(model, "calibrator", None))
        abs_err = P_hat - P_ana
        rel_err = abs_err / P_ana
        rows.append((T, P_ana, P_hat, abs_err, rel_err, SE))

    print("\n" + "─"*90)
    print("TABLE 6.1 – Analytical vs. Simulated ZCB Prices")
    print("─"*90)
    print(f"{'Maturity':<10} {'P_ana':<12} {'P_MC':<12} {'Abs Error':<13} {'Rel Error':<12} {'SE':<10}")
    print("─"*90)
    for T, P_ana, P_hat, abs_err, rel_err, SE in rows:
        print(f"{T:>4.0f}y      {P_ana:.8f}  {P_hat:.8f}  {abs_err:+.3e}  {rel_err:+.3e}  {SE:.3e}")
    print("─"*90 + "\n")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    mats = [r[0] for r in rows]
    P_anas = [r[1] for r in rows]
    P_hats = [r[2] for r in rows]
    SEs = [r[5] for r in rows]
    rel_errs = [r[4] * 100 for r in rows]

    ax1.plot(mats, P_anas, 'r-', linewidth=2, marker='o', markersize=8, label='Analytical P(0,T)')
    ax1.errorbar(mats, P_hats, yerr=[2*se for se in SEs], fmt='bo', markersize=8, capsize=5, label='MC Estimate ±2SE')
    ax1.set_xlabel('Maturity T (years)')
    ax1.set_ylabel('ZCB Price P(0,T)')
    ax1.set_title('ZCB Price Validation')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.bar(mats, rel_errs, color='coral', alpha=0.7, edgecolor='black')
    ax2.axhline(0, color='black', linewidth=1)
    ax2.set_xlabel('Maturity T (years)')
    ax2.set_ylabel('Relative Error (%)')
    ax2.set_title('Relative Pricing Error')
    ax2.grid(True, alpha=0.3, axis='y')

    show_and_save(fig, 'zcb_validation.png')
    return rows


def plot_convergence():
    """
    CONVERGENCE ANALYSIS
    Output: convergence.png
    LaTeX: Chapter 6, Figure 6.2
    """
    print_section_header("Monte Carlo Convergence", "Chapter 6")

    tenors_y, spot = make_toy_curve()
    cal = CurveCalibrator.from_market(tenors_y, spot_rates=spot)

    models = {
        'Vasicek': create_model("vasicek", r0=spot[0], a=0.15, b=0.025, sigma=0.012),
        'CIR': create_model("cir", r0=max(spot[0], 0.001), a=0.15, b=0.025, sigma=0.02),
        'Ho-Lee': create_model("ho_lee", r0=spot[0], sigma=0.01, calibrator=cal),
        'Hull-White': create_model("hull_white", r0=spot[0], a=0.1, sigma=0.01, calibrator=cal),
    }

    I_list = [1000, 2000, 5000, 10000, 20000, 50000]
    T = 10.0
    M = 120
    seed = 42

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    for idx, (name, model) in enumerate(models.items()):
        errors = []
        for I in I_list:
            rng = np.random.default_rng(seed)
            sim = model.simulate(T=T, M=M, I=I, rng=rng)
            P_hat, _ = zcb_mc_estimate_from_sim(sim, T=T)
            try:
                P_ana = model.zcb_price(T)
            except:
                try:
                    P_ana = model.zcb_price(0.0, T)
                except:
                    P_ana = cal.zcb_price(T) if hasattr(cal, 'zcb_price') else None
            if P_ana is not None:
                rel_error = abs(P_hat - P_ana) / P_ana
                errors.append(rel_error)
            else:
                errors.append(np.nan)

        axes[idx].plot(I_list, errors, 'o-', linewidth=2)
        axes[idx].set_xscale('log')
        axes[idx].set_yscale('log')
        axes[idx].set_title(f"{name} Convergence")
        axes[idx].set_xlabel("Number of scenarios (I)")
        axes[idx].set_ylabel("Relative Error")
        axes[idx].grid(True, alpha=0.3)

        ref = errors[0] * np.sqrt(I_list[0]) / np.sqrt(I_list)
        axes[idx].plot(I_list, ref, 'r--', alpha=0.7, label='O(I^{-1/2})')
        axes[idx].legend()

    plt.suptitle("Monte Carlo Convergence for All Models (ZCB Pricing Error)", fontsize=14, fontweight='bold')
    plt.tight_layout()
    show_and_save(fig, 'convergence.png')


def plot_runtime_scaling(model, T: float = 10.0, M_per_year: int = 12,
                         I_list: Sequence[int] = (1_000, 10_000, 50_000),
                         repeats: int = 3, seed: int = 42):
    """
    RUNTIME SCALING
    Output: runtime.png
    LaTeX: Chapter 6, Figure 6.3
    """
    print_section_header("Runtime Scaling", "Chapter 6")

    M = int(M_per_year * T)
    results = []

    print(f"  Benchmarking simulation runtime (T={T}, M={M}, repeats={repeats})...")

    for I in I_list:
        times = []
        for rep in range(repeats):
            rng = np.random.default_rng(seed)
            t0 = time.perf_counter()
            _ = model.simulate(T=float(T), M=M, I=int(I), rng=rng)
            t1 = time.perf_counter()
            times.append(t1 - t0)
        mean_t = float(np.mean(times))
        std_t = float(np.std(times, ddof=1)) if repeats > 1 else 0.0
        results.append((int(I), mean_t, std_t))
        print(f"    I={I:>6,}: {mean_t:.4f}s (±{std_t:.4f}s)")

    print("\n" + "─"*60)
    print("TABLE 6.2 – Runtime Scaling")
    print("─"*60)
    print(f"{'Scenarios':<15} {'Mean Time (s)':<15} {'Std Dev (s)':<15}")
    print("─"*60)
    for I, mu, sd in results:
        print(f"{I:<15,} {mu:<15.4f} {sd:<15.4f}")
    print("─"*60 + "\n")

    fig, ax = plt.subplots(figsize=(10, 6))
    I_vals = [r[0] for r in results]
    times_vals = [r[1] for r in results]
    stds = [r[2] for r in results]

    ax.errorbar(I_vals, times_vals, yerr=stds, fmt='bo-', linewidth=2, markersize=10, capsize=5)
    ax.set_xlabel('Number of Scenarios (I)')
    ax.set_ylabel('Runtime (seconds)')
    ax.set_title('Simulation Runtime Scaling')
    ax.grid(True, alpha=0.3)

    if len(I_vals) > 1:
        slope = (times_vals[-1] - times_vals[0]) / (I_vals[-1] - I_vals[0])
        linear_ref = [times_vals[0] + slope * (I - I_vals[0]) for I in I_vals]
        ax.plot(I_vals, linear_ref, 'r--', alpha=0.5, linewidth=1.5, label='Linear Reference')
        ax.legend()

    show_and_save(fig, 'runtime.png')


# =============================================================================
# CHAPTER 8: Discussion
# =============================================================================
def plot_one_factor_limitation():
    """
    ONE-FACTOR LIMITATION
    Output: one_factor_limitation.png
    LaTeX: Chapter 8, Figure 8.1
    """
    print_section_header("One-Factor Limitation", "Chapter 8")

    tenors_y, spot = make_toy_curve()
    cal = CurveCalibrator.from_market(tenors_y, spot_rates=spot)

    model = create_model("hull_white", r0=float(spot[0]), a=0.10, sigma=0.01, calibrator=cal)

    rng = _rng(42, tag="one_factor_sim")
    sim = model.simulate(T=10.0, M=120, I=1, rng=rng)

    t_grid = sim.times
    r_path = sim.rates[:, 0]

    taus = [1.0, 5.0, 10.0]
    y = {tau: [] for tau in taus}

    for t, r_t in zip(t_grid, r_path):
        t = float(t)
        r_t = float(r_t)
        for tau in taus:
            T = t + tau
            P = _zcb_price_call(model, t, T, r_t=r_t)
            y[tau].append(_zero_yield_from_zcb(P, tau) * 100.0)

    y_mat = np.vstack([y[tau] for tau in taus])
    corr = np.corrcoef(y_mat)

    fig, ax = plt.subplots(figsize=(10, 6))
    for tau in taus:
        ax.plot(t_grid, y[tau], linewidth=2, label=f"τ={tau:g}y zero yield")

    ax.set_title("One-Factor Limitation: Strong Co-Movement Across Maturities")
    ax.set_xlabel("Time t (years)")
    ax.set_ylabel("Zero yield y(t,t+τ) (%)")
    ax.grid(True, alpha=0.3)
    ax.legend()

    txt = f"Correlation(yields)\n1y–5y: {corr[0,1]:.3f}\n1y–10y: {corr[0,2]:.3f}\n5y–10y: {corr[1,2]:.3f}"
    ax.text(0.02, 0.98, txt, transform=ax.transAxes, va="top", ha="left", fontsize=9,
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8))

    plt.tight_layout()
    show_and_save(fig, "one_factor_limitation.png")


def plot_parameter_sensitivity():
    """
    PARAMETER SENSITIVITY
    Output: parameter_sensitivity.png
    LaTeX: Chapter 8, Figure 8.2
    """
    print_section_header("Parameter Sensitivity", "Chapter 8")

    tenors_y, spot = make_toy_curve()
    cal = CurveCalibrator.from_market(tenors_y, spot_rates=spot)

    param_sets = [
        {'a': 0.05, 'sigma': 0.005, 'label': 'Low MR, Low Vol'},
        {'a': 0.05, 'sigma': 0.02, 'label': 'Low MR, High Vol'},
        {'a': 0.20, 'sigma': 0.005, 'label': 'High MR, Low Vol'},
        {'a': 0.20, 'sigma': 0.02, 'label': 'High MR, High Vol'},
    ]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    for idx, params in enumerate(param_sets):
        model = create_model("hull_white", r0=float(spot[0]), a=params['a'],
                            sigma=params['sigma'], calibrator=cal)
        rng = np.random.default_rng(42)
        sim = model.simulate(T=10.0, M=120, I=2000, rng=rng)

        terminal_rates = sim.rates[-1, :] * 100

        axes[idx].hist(terminal_rates, bins=40, alpha=0.7, edgecolor='black')
        axes[idx].axvline(np.mean(terminal_rates), color='red', linestyle='--',
                         label=f'Mean: {np.mean(terminal_rates):.2f}%')
        axes[idx].set_xlabel('Terminal Rate (%)')
        axes[idx].set_ylabel('Frequency')
        axes[idx].set_title(f"a={params['a']}, σ={params['sigma']}")
        axes[idx].legend()
        axes[idx].grid(True, alpha=0.3, axis='y')

    plt.suptitle('Parameter Sensitivity: Impact on Terminal Rate Distribution', fontsize=14, fontweight='bold')
    plt.tight_layout()
    show_and_save(fig, 'parameter_sensitivity.png')


def plot_model_npv_comparison():
    """
    MODEL NPV COMPARISON
    Output: model_comparison.png
    LaTeX: Chapter 8, Figure 8.3
    """
    print_section_header("Model NPV Comparison", "Chapter 8")

    tenors_y, spot = make_toy_curve()
    cal = CurveCalibrator.from_market(tenors_y, spot_rates=spot)

    models = {
        'Vasicek': create_model("vasicek", r0=spot[0], a=0.15, b=0.025, sigma=0.012),
        'CIR': create_model("cir", r0=max(spot[0], 0.001), a=0.15, b=0.025, sigma=0.02),
        'Ho-Lee': create_model("ho_lee", r0=spot[0], sigma=0.01, calibrator=cal),
        'Hull-White': create_model("hull_white", r0=spot[0], a=0.1, sigma=0.01, calibrator=cal),
    }

    colors = {'Vasicek': 'blue', 'CIR': 'green', 'Ho-Lee': 'purple', 'Hull-White': 'red'}

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    for idx, (name, model) in enumerate(models.items()):
        rng = np.random.default_rng(42)
        sim = model.simulate(T=10.0, M=120, I=1000, rng=rng)

        # Synthetic NPVs
        avg_rates = np.mean(sim.rates, axis=0)
        base_npv = 500_000
        interest_sensitivity = -10_000_000
        surplus = base_npv + interest_sensitivity * (avg_rates - np.mean(avg_rates))
        surplus += rng.normal(0, 30_000, size=surplus.shape)

        mean_npv = np.mean(surplus)
        std_npv = np.std(surplus)
        pctl_5 = np.percentile(surplus, 5)
        var_95 = mean_npv - pctl_5

        axes[idx].hist(surplus / 1000, bins=35, alpha=0.7, color=colors[name], edgecolor='black')
        axes[idx].axvline(mean_npv / 1000, color='black', linestyle='--', linewidth=2, label='Mean')
        axes[idx].axvline(pctl_5 / 1000, color='darkred', linestyle=':', linewidth=2, label='5th Pctl')

        stats_text = f'Mean: {mean_npv/1000:.0f}k\nStd: {std_npv/1000:.0f}k\nVaR95: {var_95/1000:.0f}k'
        axes[idx].text(0.02, 0.98, stats_text, transform=axes[idx].transAxes,
                       verticalalignment='top', fontsize=9,
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

        axes[idx].set_xlabel('NPV (thousands CHF)')
        axes[idx].set_ylabel('Frequency')
        axes[idx].set_title(f'{name} Model')
        axes[idx].grid(True, alpha=0.3, axis='y')

    plt.suptitle('Model Selection Impact: NPV Distributions Across All Models', fontsize=14, fontweight='bold')
    plt.tight_layout()
    show_and_save(fig, 'model_comparison.png')


# =============================================================================
# TABLES
# =============================================================================
def generate_model_comparison_table():
    """Generate model comparison table for Appendix."""
    data = {
        'Model': ['Vasicek', 'CIR', 'Ho-Lee', 'Hull-White'],
        'Type': ['Equilibrium', 'Equilibrium', 'No-Arbitrage', 'No-Arbitrage'],
        'SDE': ['dr = a(b-r)dt + σdW', 'dr = a(b-r)dt + σ√r dW',
                'dr = θ(t)dt + σdW', 'dr = (θ(t)-ar)dt + σdW'],
        'Negative Rates': ['Possible', 'No (Feller)', 'Possible', 'Possible'],
        'Mean Reversion': ['Yes', 'Yes', 'No', 'Yes'],
        'Curve Fit': ['No', 'No', 'Yes', 'Yes'],
    }
    df = pd.DataFrame(data)

    print("\n" + "="*80)
    print("MODEL COMPARISON TABLE (for Appendix)")
    print("="*80)
    print(df.to_markdown())

    print("\nLaTeX version:")
    print(df.to_latex(index=False, caption="Comparison of implemented short-rate models",
                      label="tab:model_comparison"))
    return df


# =============================================================================
# MAIN
# =============================================================================
def main(args):
    """Main execution function."""
    print("\n" + "="*80)
    print("THESIS PLOTS GENERATOR")
    print("="*80)
    print(f"Mode: {'SAVE + DISPLAY' if args.save else 'DISPLAY ONLY' if not args.save_only else 'SAVE ONLY'}")
    print("\nNOTE: Chapter 7 plots are generated by thesis_alm_example_extended.py")

    configure_output(save=args.save, save_only=args.save_only)

    try:
        tenors_y, spot = make_toy_curve()

        # Chapter 2: Theoretical Foundation
        print_section_header("CHAPTER 2: Theoretical Foundation")
        plot_vasicek_vs_cir_comparison()
        plot_all_models_comparison()

        # Chapter 5: Implementation
        print_section_header("CHAPTER 5: Implementation")
        cal = plot_curve_calibration(tenors_y, spot, grid_max=30.0)
        plot_theta_drift(cal, T=10.0)

        # Chapter 6: Validation
        print_section_header("CHAPTER 6: Validation")
        model_hw = create_model("hull_white", r0=float(spot[0]), a=0.10, sigma=0.01, calibrator=cal)
        table_zcb_benchmark(model_hw, maturities=[1, 5, 10, 20, 30],
                           I=20_000 if not args.quick else 5000)
        plot_convergence()
        plot_runtime_scaling(model_hw, T=10.0,
                            I_list=(1000, 5000, 10000, 20000) if not args.quick else (1000, 2000))

        # Chapter 8: Discussion
        print_section_header("CHAPTER 8: Discussion")
        plot_one_factor_limitation()
        plot_parameter_sensitivity()
        plot_model_npv_comparison()

        # Tables
        print_section_header("TABLES")
        generate_model_comparison_table()

        print("\n" + "="*60)
        print(" ALL PLOTS GENERATED SUCCESSFULLY")
        print("="*60)

        if SAVE_PLOTS:
            print(f"\n Plots saved to: {OUTPUT_DIR}/")
            files = sorted([f for f in os.listdir(OUTPUT_DIR) if f.endswith('.png')])
            for i, fname in enumerate(files, 1):
                print(f"  {i:2d}. {fname}")

        if not args.save_only:
            print("\nPress Enter to close all plots...")
            input()
            plt.close('all')

    except Exception as e:
        print(f"\n ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate thesis plots")
    parser.add_argument('--save', action='store_true', help='Save plots as PNG')
    parser.add_argument('--save-only', action='store_true', help='Save without display')
    parser.add_argument('--quick', action='store_true', help='Use fewer scenarios')

    args = parser.parse_args()

    try:
        main(args)
    except KeyboardInterrupt:
        print("\n️  Interrupted")
        sys.exit(1)