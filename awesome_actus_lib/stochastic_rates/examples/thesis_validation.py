"""thesis_validation.py

Generates statistical validation artifacts for the Bachelor Thesis.
1. Model Convergence Analysis (Error vs Samples)
2. Analytical vs Monte Carlo Pricing Validation (Table)
3. Calibration Quality Metrics
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict

# Use correct absolute imports
from stochastic_rates import (
    CurveCalibrator,
    create_model,
    available_models
)

def run_analytics_suite():
    print("=== Thesis Analytics & Validation Suite ===")
    
    # 1. Setup Market Data
    # --------------------
    print("\n[1] Calibrating Base Curve...")
    maturities = np.array([1, 2, 3, 5, 7, 10, 15, 20], dtype=float)
    rates = np.array([0.02, 0.022, 0.024, 0.027, 0.029, 0.032, 0.035, 0.036], dtype=float)
    
    cal = CurveCalibrator.from_market(times=maturities, spot_rates=rates, extrapolation_mode="flat")
    
    # 2. Convergence Analysis (Vasicek)
    # -------------------------------
    print("\n[2] Running Convergence Analysis (Vasicek)...")
    vasicek = create_model("vasicek", r0=0.02, a=0.2, b=0.03, sigma=0.015, seed=42)
    
    # Run a high-res simulation
    with vasicek.no_cache():
        sim = vasicek.simulate(T=5.0, M=60, I=5000)
    
    conv_df = sim.convergence_analysis(target_stat='terminal_mean', path_sizes=[10, 50, 100, 500, 1000, 2000, 5000])
    print(conv_df)
    
    # Plot Convergence
    plt.figure(figsize=(8, 5))
    plt.semilogx(conv_df['n_paths'], conv_df['estimate'], 'o-', label='MC Estimate (Mean)')
    plt.axhline(0.02008, color='red', linestyle='--', alpha=0.5, label='Analytical Mean (Approx)') # Theoretical limit depends on params
    plt.title("Monte Carlo Convergence (Terminal Rate Mean)")
    plt.xlabel("Number of Paths (log scale)")
    plt.ylabel("Estimate")
    plt.grid(True, which="both", ls="-", alpha=0.2)
    plt.legend()
    plt.savefig("thesis_convergence_plot.png")
    print("Saved thesis_convergence_plot.png")

    # 3. Analytical Validation Table
    # ------------------------------
    print("\n[3] Validating ZCB Pricing (Analytical vs MC)...")
    results = []
    
    models = {
        'Vasicek': create_model("vasicek", r0=0.02, a=0.2, b=0.03, sigma=0.015, seed=101),
        'CIR': create_model("cir", r0=0.02, a=0.2, b=0.03, sigma=0.05, seed=101), # Adjusted sigma for Feller
        'Hull-White': create_model("hull_white", r0=0.02, a=0.1, sigma=0.01, calibrator=cal, seed=101),
        'Ho-Lee': create_model("ho_lee", r0=0.02, sigma=0.01, calibrator=cal, seed=101),
    }

    test_horizon = 5.0
    
    for name, model in models.items():
        print(f"  Testing {name}...")
        res = model.validate_against_analytical(T=test_horizon, n_samples=10000)
        res['model'] = name
        results.append(res)
        
    df_res = pd.DataFrame(results)[['model', 'T', 'analytical', 'monte_carlo', 'abs_error', 'rel_error_pct']]
    print("\nValidation Results (T=5.0):")
    print(df_res.to_string(index=False, float_format="%.6f"))
    
    # Save as CSV for LaTeX table generation
    df_res.to_csv("thesis_validation_table.csv", index=False)
    print("Saved thesis_validation_table.csv")

    # 4. Calibration Check (Hull-White)
    # ---------------------------------
    print("\n[4] Zero-Coupon Curve Fit (Hull-White)...")
    hw = models['Hull-White']
    
    check_times = np.linspace(0.5, 20, 20)
    market_prices = cal.zcb_price(check_times)
    model_prices = [hw.zcb_price(0, t) for t in check_times] # Analytical HW price
    
    mse = np.mean((market_prices - model_prices)**2)
    print(f"Hull-White Analytical Fit MSE: {mse:.2e}")
    
    plt.figure(figsize=(8, 5))
    plt.plot(check_times, market_prices, 'k-', linewidth=2, label="Market Input (Spline)")
    plt.plot(check_times, model_prices, 'r--', label="Hull-White Analytical")
    plt.title(f"Calibration Fit (Hull-White) MSE={mse:.2e}")
    plt.xlabel("Maturity T (Years)")
    plt.ylabel("ZCB Price P(0,T)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig("thesis_calibration_plot.png")
    print("Saved thesis_calibration_plot.png")

if __name__ == "__main__":
    run_analytics_suite()
