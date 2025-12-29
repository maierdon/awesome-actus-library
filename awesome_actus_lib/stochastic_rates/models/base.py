from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, Tuple
import numpy as np

from ..simulation import SimulationResult

Array = np.ndarray

from contextlib import contextmanager

class ShortRateModel(ABC):
    """Abstract base class for one-factor short-rate models."""
    name: str

    def __init__(self, *, r0: float, seed: Optional[int] = None):
        self.r0 = float(r0)
        self.seed = seed
        self._rng = np.random.default_rng(seed) if seed is not None else None
        self._sim: Optional[SimulationResult] = None
        self._cache_enabled: bool = True

    @property
    def simulation(self) -> Optional[SimulationResult]:
        return self._sim

    @contextmanager
    def no_cache(self):
        """Context manager to temporarily disable simulation caching."""
        old_val = self._cache_enabled
        self._cache_enabled = False
        try:
            yield
        finally:
            self._cache_enabled = old_val
            # Optional: Decide if we want to clear cache on exit or just restore flag.
            # User example suggests just restoring flag + clearing sim.
            self._sim = None

    def reset_rng(self) -> None:
        """Resets the internal RNG if a seed was provided."""
        if self.seed is not None:
            self._rng = np.random.default_rng(self.seed)

    def require_simulation(self) -> SimulationResult:
        if self._sim is None:
            raise RuntimeError("No simulation available. Call simulate(...) first.")
        return self._sim

    def simulate(self, *, T: float, M: int, I: int, rng: Optional[np.random.Generator] = None) -> SimulationResult:
        """
        Simulate short-rate paths. 
        Uses the internal RNG if 'rng' is not provided and a seed was set.
        Caches the result unless validation is active or 'no_cache' context is used.
        """
        if rng is None:
            if self._rng is not None:
                rng = self._rng
            else:
                rng = np.random.default_rng()

        sim = self._simulate_impl(T=T, M=M, I=I, rng=rng)
        
        if self._cache_enabled:
            self.set_simulation(sim)
        
        return sim

    @abstractmethod
    def _simulate_impl(self, *, T: float, M: int, I: int, rng: np.random.Generator) -> SimulationResult:
        """Concrete implementation of the simulation step."""
        pass

    @abstractmethod
    def zcb_price(self, t: float, T: float, r_t: Optional[float] = None) -> float:
        pass

    def explain(self) -> str:
        doc = self.__class__.__doc__
        return doc.strip() if doc else ""

    def set_simulation(self, sim: SimulationResult) -> None:
        sim.assert_valid()
        self._sim = sim

    def sample_paths(self, n: int = 10) -> Tuple[Array, Array]:
        sim = self.require_simulation()
        k = min(int(n), sim.n_paths)
        return sim.times.copy(), sim.rates[:, :k].copy()

    def validate_against_analytical(self, T: float, r_t: Optional[float] = None, n_samples: int = 10000) -> dict:
        """
        Compare Monte Carlo ZCB pricing with analytical formula.
        """
        # Analytical Price
        P_analytical = self.zcb_price(t=0, T=T, r_t=r_t)

        # Monte Carlo Price using temporary simulation
        # Use no_cache() to avoid overwriting user's main simulation if they have one
        with self.no_cache():
            # Use sufficient steps for convergence (e.g., monthly)
            steps = int(max(T * 12, 12)) 
            sim = self.simulate(T=T, M=steps, I=n_samples)
            
            # Integral approximation: trapezoidal rule or simple sum
            # Simple Reimann sum: sum(r(t_i) * dt)
            dt = sim.dt
            # Exclude last point for left-Riemann sum or use trapz
            integral_r = np.sum(sim.rates[:-1, :], axis=0) * dt
            P_mc_paths = np.exp(-integral_r)
            P_mc = float(np.mean(P_mc_paths))
            mc_std_error = float(np.std(P_mc_paths) / np.sqrt(n_samples))

        error = abs(P_mc - P_analytical)
        if P_analytical != 0:
            rel_error = error / abs(P_analytical)
        else:
            rel_error = float('inf')

        return {
            'T': T,
            'analytical': P_analytical,
            'monte_carlo': P_mc,
            'mc_std_error': mc_std_error,
            'abs_error': error,
            'rel_error_pct': 100.0 * rel_error
        }

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(r0={self.r0})"
