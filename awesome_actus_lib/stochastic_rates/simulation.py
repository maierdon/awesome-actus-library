from __future__ import annotations
import pandas as pd
import warnings
from dataclasses import dataclass
import numpy as np

Array = np.ndarray

@dataclass
class SimulationResult:
    """Container for a simulated short-rate path matrix."""
    times: Array
    rates: Array

    def assert_valid(self) -> None:
        if self.times.ndim != 1:
            raise ValueError("times must be 1D")
        if self.rates.ndim != 2:
            raise ValueError("rates must be 2D")
        if self.rates.shape[0] != self.times.size:
            raise ValueError(f"rates first dim matches times length")
        
        # Check for negative rates (warn only)
        if np.any(self.rates < 0):
            n_neg = np.sum(self.rates < 0)
            pct = 100.0 * n_neg / self.rates.size
            warnings.warn(
                f"Simulation contains {n_neg} negative rates ({pct:.2f}%). "
                f"This is expected for Gaussian models (Vasicek, Hull-White) "
                f"but may be problematic for certain ACTUS contracts.",
                UserWarning,
                stacklevel=2
            )

    @property
    def n_steps(self) -> int:
        return self.times.size - 1

    @property
    def n_paths(self) -> int:
        return self.rates.shape[1]

    @property
    def horizon(self) -> float:
        return float(self.times[-1])

    @property
    def dt(self) -> float:
        return float(self.times[1] - self.times[0]) if self.n_steps > 0 else 0.0

    def mean_path(self) -> Array:
        return np.mean(self.rates, axis=1)

    def std_path(self) -> Array:
        return np.std(self.rates, axis=1)

    def percentile_path(self, q: float) -> Array:
        return np.percentile(self.rates, q, axis=1)

    def terminal_distribution(self) -> Array:
        return self.rates[-1, :]

    def rate_at_time(self, t: float) -> Array:
        idx = np.argmin(np.abs(self.times - t))
        return self.rates[idx, :]

    def statistics(self) -> dict:
        return {
            'n_paths': self.n_paths,
            'n_steps': self.n_steps,
            'horizon': self.horizon,
            'dt': self.dt,
            'initial_rate': float(self.rates[0, 0]),
            'terminal_mean': float(np.mean(self.terminal_distribution())),
            'terminal_std': float(np.std(self.terminal_distribution())),
            'min_rate': float(np.min(self.rates)),
            'max_rate': float(np.max(self.rates)),
        }

    def convergence_analysis(self, target_stat='terminal_mean', path_sizes=[10, 50, 100, 500, 1000]) -> pd.DataFrame:
        """Analyze convergence of Monte Carlo estimators."""
        results = []
        for n in path_sizes:
            if n > self.n_paths:
                continue
            subset = self.rates[:, :n]
            if target_stat == 'terminal_mean':
                val = np.mean(subset[-1, :])
            elif target_stat == 'terminal_std':
                val = np.std(subset[-1, :])
            else:
                raise ValueError(f"Unknown target_stat='{target_stat}'")
            results.append({'n_paths': n, 'estimate': val})
        return pd.DataFrame(results)
