# Stochastic Interest Rate Models for AAL

**Extension module for the Awesome ACTUS Library (AAL)**

---

## What is this?

This module provides **stochastic short-rate models** for generating Monte Carlo interest-rate scenarios. The simulated scenarios can be converted into ACTUS-compatible risk factors (`ReferenceIndex`) for forward-looking portfolio valuation and risk analysis.

### Why is this relevant?

Standard ACTUS workflows use **deterministic** yield curves, which show only point estimates. For Asset-Liability Management (ALM) and risk analysis, you need to understand how portfolio values behave under **many possible future interest-rate paths**. This extension bridges that gap by:

1. Calibrating to today's market curve
2. Simulating realistic future scenarios
3. Converting simulations to ACTUS-native formats
4. Enabling distributional risk metrics (VaR, ES, NPV distributions)

For detailed information on the internal design (MAS architecture, Design Patterns), see [ARCHITECTURE.md](ARCHITECTURE.md).

---

## Supported Models

| Model | Type | Mean Reversion | Rate Floor | Use Case |
|-------|------|----------------|------------|----------|
| **Vasicek** | Equilibrium | Yes | No (Gaussian) | Simple validation, negative rates OK |
| **CIR** | Equilibrium | Yes | Yes (chi-squared) | Non-negative rates required |
| **Ho-Lee** | No-arbitrage | No | No (Gaussian) | Curve-fitting, short horizon |
| **Hull-White** | No-arbitrage | Yes | No (Gaussian) | ALM/long-horizon, recommended |

---

## Quick Start

```python
import numpy as np
from stochastic_rates import (
    CurveCalibrator,
    create_model,
    simulation_to_reference_index
)

# 1. Market curve input
tenors = [1, 2, 5, 10]  # years
rates = [0.02, 0.022, 0.025, 0.028]  # spot rates
cal = CurveCalibrator.from_market(tenors, spot_rates=rates)

# 2. Create model (Hull-White: curve-fit + mean reversion)
model = create_model(
    "hull_white",
    r0=rates[0],
    a=0.10,           # mean reversion speed
    sigma=0.01,       # volatility
    calibrator=cal,
    seed=42           # for reproducibility
)

# 3. Simulate 1000 paths over 10 years
sim = model.simulate(T=10.0, M=120, I=1000)

# 4. Convert to ACTUS ReferenceIndex
rf = simulation_to_reference_index(
    sim,
    base_date="2025-01-01",
    market_code="YC_CHF",
    path=0  # or loop over all paths
)

# 5. Use with ACTUS contracts
# rf can now be passed to service.generateEvents(contract, riskFactors=[rf])
```

---

## Module Structure

```
stochastic_rates/
├── __init__.py          # Public API exports
├── factory.py           # create_model(), available_models()
├── simulation.py        # SimulationResult container
├── integration.py       # ACTUS adapter functions
├── models/
│   ├── base.py          # ShortRateModel (abstract)
│   ├── vasicek.py       # Vasicek model
│   ├── cir.py           # Cox-Ingersoll-Ross model
│   ├── ho_lee.py        # Ho-Lee model
│   └── hull_white.py    # Hull-White model
├── calibration/
│   ├── curve.py         # CurveCalibrator
│   └── spline.py        # Cubic spline interpolation
├── examples/
│   ├── quickstart.py    # Minimal end-to-end example
│   ├── generate_thesis_plots.py  # Validation tables and plots
│   └── thesis_alm_example.py     # Full ALM workflow
├── tests/
│   ├── test_models.py
│   ├── test_calibration.py
│   └── test_integration.py
└── docs/
    ├── ARCHITECTURE.md
    └── *.puml           # UML diagrams
```

---

## Key Functions

### Factory
```python
from stochastic_rates import create_model, available_models

available_models()  # ['vasicek', 'cir', 'ho_lee', 'hull_white']
model = create_model("hull_white", r0=0.02, a=0.1, sigma=0.01, calibrator=cal, seed=42)
```

### Simulation
```python
sim = model.simulate(T=10.0, M=120, I=1000)
sim.mean_path()              # Mean across paths
sim.percentile_path(95)      # 95th percentile
sim.terminal_distribution()  # r(T) distribution
```

### Validation
```python
result = model.validate_against_analytical(T=5.0, n_samples=10000)
# Returns: {'analytical': 0.873716, 'monte_carlo': 0.874984, 'rel_error_pct': 0.15}
```

### ACTUS Integration
```python
from stochastic_rates import (
    simulation_to_reference_index, 
    simulation_to_scenarios
)

# Single path -> ReferenceIndex
rf = simulation_to_reference_index(sim, base_date="2025-01-01", market_code="YC_CHF", path=0)

# All paths -> ScenarioSet
scenarios = simulation_to_scenarios(sim, base_date="2025-01-01", market_code="YC_CHF")
```

---

## Data Input

The `CurveCalibrator` expects **pre-processed input arrays** (tenors and spot rates or ZCB prices). 

```python
# From manually extracted data
tenors = [1, 2, 5, 10]           # years
spot_rates = [0.02, 0.022, 0.025, 0.028]  # continuously compounded
cal = CurveCalibrator.from_market(tenors, spot_rates=spot_rates)

# Alternative: from ZCB prices
zcb_prices = [0.98, 0.956, 0.88, 0.75]
cal = CurveCalibrator.from_market(tenors, zcb_prices=zcb_prices)
```

**Note:** Integration with raw market data feeds (e.g., SNB XML exports, Bloomberg terminals) requires a separate preprocessing step to extract the relevant time series. This is intentionally left to the user to maintain flexibility across data providers.

---

## End-to-End Workflow

```
Market Curve --> CurveCalibrator --> ShortRateModel --> simulate()
                                                            |
                                                            v
                                                    SimulationResult
                                                            |
                                                            v
                                      simulation_to_reference_index()
                                                            |
                                                            v
                                          ACTUS ReferenceIndex
                                                            |
                                                            v
                              ACTUS Engine (generateEvents)
                                                            |
                                                            v
                                        Cash Flows --> ValueAnalysis
                                                            |
                                                            v
                                          NPV Distribution, VaR, ES
```

---

## Examples

| Script | Purpose |
|--------|---------|
| `examples/quickstart.py` | Minimal example for third-party users |
| `examples/generate_thesis_plots.py` | Generate validation tables and plots |
| `examples/thesis_alm_example.py` | Full ALM workflow with VaR calculation |

Run quickstart:
```bash
cd awesome_actus_lib/stochastic_rates/examples
python quickstart.py
```

---

## Tests

```bash
cd /path/to/AAL
pip install pytest
python -m pytest awesome_actus_lib/stochastic_rates/tests/ -v
```

---

## References

- Hull, J.C. (2022). *Options, Futures, and Other Derivatives*, 11th ed. Technical Note 31.
- Vasicek, O. (1977). "An equilibrium characterization of the term structure."
- Cox, Ingersoll, Ross (1985). "A theory of the term structure of interest rates."
- Ho, T.S.Y. & Lee, S.B. (1986). "Term structure movements and pricing interest rate contingent claims."
- Hull, J. & White, A. (1990). "Pricing interest-rate-derivative securities."
- Glasserman, P. (2004). *Monte Carlo Methods in Financial Engineering*.

---

## Author

**Project Thesis**: Enhancing Financial Analytics in Python and ACTUS  
**Author**: Amritjot Ghodra  
**Supervisors**: Prof. Dr. Henriette Elise Breymann, Dr. Christian Badertscher  
**Institution**: ZHAW School of Engineering  
**Date**: December 2025