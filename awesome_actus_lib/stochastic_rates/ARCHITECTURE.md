# Technical Architecture: Stochastic Rates Extension

## 1. Architectural Overview

The `stochastic_rates` module adheres to the **Model-Analysis-Service (MAS)** architecture of the Awesome ACTUS Library (AAL). It provides a unified and scalable framework for simulating interest rates and integrating them into ACTUS contract evaluations.

### 1.1 Layer Mapping

| Layer | Module | Responsibility |
|-------|--------|----------------|
| **Model** | `models/` | Mathematical definitions of short-rate SDEs |
| **Service** | `calibration/`, `factory.py` | Curve fitting, model instantiation |
| **Analysis** | `simulation.py` | Result containers, statistics |
| **Adapter** | `integration.py` | ACTUS-compatible output conversion |

### 1.2 Package Structure

```
stochastic_rates/
├── models/
│   ├── base.py           # ShortRateModel (abstract base class)
│   ├── vasicek.py        # Vasicek: dr = a(b-r)dt + σdW
│   ├── cir.py            # CIR: dr = a(b-r)dt + σ√r dW
│   ├── ho_lee.py         # Ho-Lee: dr = θ(t)dt + σdW
│   └── hull_white.py     # Hull-White: dr = (θ(t)-ar)dt + σdW
├── calibration/
│   ├── curve.py          # CurveCalibrator (spline + extrapolation)
│   └── spline.py         # Natural cubic spline implementation
├── simulation.py         # SimulationResult dataclass
├── integration.py        # ACTUS adapters
├── factory.py            # create_model(), available_models()
└── __init__.py           # Public API exports
```

---

## 2. Design Patterns

### 2.1 Strategy Pattern
The `ShortRateModel` abstract base class defines a common interface for all models. Concrete implementations (Vasicek, CIR, Ho-Lee, Hull-White) are interchangeable strategies.

```python
class ShortRateModel(ABC):
    @abstractmethod
    def _simulate_impl(self, T, M, I, rng) -> SimulationResult:
        """Model-specific simulation logic."""
        pass
    
    def simulate(self, T, M, I, seed=None) -> SimulationResult:
        """Public interface with RNG management."""
        # ... common setup, then delegate to _simulate_impl
```

### 2.2 Factory Pattern
The `create_model()` function provides configuration-driven instantiation:

```python
model = create_model(
    "hull_white",
    r0=0.02,
    a=0.1,
    sigma=0.01,
    calibrator=cal,
    seed=42
)
```

This decouples client code from concrete model classes.

### 2.3 Template Method Pattern
The `simulate()` method in `ShortRateModel` implements common concerns (RNG setup, caching, validation) while delegating model-specific logic to `_simulate_impl()`.

### 2.4 Adapter Pattern
The `integration.py` module adapts raw numerical arrays to ACTUS-compatible structures:

```
SimulationResult (numpy arrays)
        │
        ▼
simulation_to_reference_index()
        │
        ▼
ReferenceIndex (pandas DataFrame with marketObjectCode)
```

---

## 3. Data Flow

### 3.1 Calibration Flow

```
Market Data (tenors, spot_rates)
        │
        ▼
CurveCalibrator.from_market()
        │
        ├── Natural cubic spline fit
        ├── Compute P(0,T), R(0,T), f(0,T)
        └── Flat-forward extrapolation beyond T_max
        │
        ▼
CurveCalibrator instance
        │
        ▼
Model.theta(t) for Ho-Lee / Hull-White
```

### 3.2 Simulation Flow

```
ShortRateModel.simulate(T, M, I)
        │
        ├── Initialize rates[0,:] = r0
        │
        ├── For k = 1 to M:
        │       │
        │       ├── Generate Z ~ N(0,1) for all I paths
        │       └── Apply exact transition (model-specific)
        │
        └── Return SimulationResult
                │
                ├── times: shape (M+1,)
                ├── rates: shape (M+1, I)
                └── Statistics: mean_path, percentiles, terminal_distribution
```

### 3.3 ACTUS Integration Flow

```
SimulationResult
        │
        ▼
simulation_to_reference_index(sim, base_date, market_code, path)
        │
        ├── Extract rates[:, path]
        ├── Convert times to dates
        └── Create TimeSeries DataFrame
        │
        ▼
ReferenceIndex(marketObjectCode, values=TimeSeries)
        │
        ▼
ActusService.generateEvents(contract, riskFactors=[rf])
```

---

## 4. Exact Transition Methods

Unlike simple Euler-Maruyama discretization, this implementation uses **exact transition sampling** where available:

| Model | Transition Distribution | Method |
|-------|------------------------|--------|
| Vasicek | Gaussian (Ornstein-Uhlenbeck) | Exact mean + variance |
| CIR | Non-central chi-squared | `ncx2` sampling |
| Ho-Lee | Gaussian with time-dependent drift | Exact integration |
| Hull-White | Gaussian (OU with θ(t)) | Per-step drift evaluation |

**Benefit**: Eliminates discretization bias, allowing larger time steps without accuracy loss.

---

## 5. Calibration Details

### 5.1 Curve Construction

The `CurveCalibrator` transforms sparse market quotes into a continuous curve:

1. **Input**: `(tenors, spot_rates)` or `(tenors, zcb_prices)`
2. **Interpolation**: Natural cubic spline on spot rates R(0,T)
3. **Derived quantities**:
   - ZCB prices: `P(0,T) = exp(-R(0,T) * T)`
   - Forward rates: `f(0,T) = R(0,T) + T * dR/dT`
   - Forward slope: `df/dT` (for θ(t) calibration)

### 5.2 Drift Calibration (No-Arbitrage Models)

For Ho-Lee and Hull-White, the drift θ(t) is calibrated to match the initial term structure:

**Ho-Lee**:
```
θ(t) = ∂f(0,t)/∂t + σ²t
```

**Hull-White**:
```
θ(t) = ∂f(0,t)/∂t + a·f(0,t) + (σ²/2a)(1 - e^{-2at})
```

### 5.3 Extrapolation

Beyond the last market tenor T_max, two modes are supported:

- **Flat-forward** (default): `f(0,t) = f(0,T_max)` for `t > T_max`
- **Strict**: Raise error if queried beyond T_max

---

## 6. Validation Approach

### 6.1 Analytical Benchmarking

Zero-coupon bond prices have closed-form solutions for affine models. The validation compares:

```
P_analytical(0,T)  vs  P_MC(0,T) = (1/I) Σ exp(-∫r_t dt)
```

Target: Relative error < 0.5% with I=10,000 paths.

### 6.2 Convergence Verification

Monte Carlo estimators converge at O(I^{-1/2}). The `convergence_analysis()` method verifies this rate empirically.

### 6.3 Model Invariants

- **Vasicek/Hull-White**: Gaussian distribution of r(T)
- **CIR**: Non-negativity (r(t) ≥ 0 if Feller condition holds)
- **Ho-Lee/Hull-White**: P_model(0,T) ≈ P_market(0,T)

---

## 7. Extension Points

The architecture supports future extensions:

| Extension | How to Add |
|-----------|------------|
| New model (e.g., G2++) | Subclass `ShortRateModel`, implement `_simulate_impl()` |
| Alternative calibration | Extend `CurveCalibrator` or create new calibrator class |
| Additional risk factors | Extend `integration.py` with new adapter functions |
| GPU acceleration | Replace numpy operations in `_simulate_impl()` with CuPy |

---

## 8. Dependencies

**Runtime**:
- `numpy >= 1.20` (vectorized computation)
- `pandas >= 1.3` (time series for ACTUS integration)

**Development**:
- `pytest` (testing)
- `matplotlib` (visualization in examples)

**No external dependencies** for core simulation (pure NumPy).