from __future__ import annotations
from typing import Optional
import numpy as np
from ..simulation import SimulationResult
from .base import ShortRateModel

class Vasicek(ShortRateModel):
    """Vasicek (1977): dr = a(b-r)dt + sigma dW."""
    name = "vasicek"

    def __init__(self, *, r0: float, a: float, b: float, sigma: float, seed: Optional[int] = None):
        super().__init__(r0=r0, seed=seed)
        if sigma < 0:
            raise ValueError(f"sigma must be non-negative, got {sigma}")
        if a <= 0:
            raise ValueError(f"mean-reversion speed 'a' must be positive, got {a}")
        self.a = float(a)
        self.b = float(b)
        self.sigma = float(sigma)

    def _simulate_impl(self, *, T: float, M: int, I: int, rng: np.random.Generator) -> SimulationResult:
        if M <= 0 or I <= 0:
            raise ValueError("M and I must be positive")
        T = float(T)
        dt = T / float(M)
        times = np.linspace(0.0, T, M + 1)

        rates = np.empty((M + 1, I), dtype=float)
        rates[0, :] = self.r0

        exp_a = np.exp(-self.a * dt)
        mean_coeff = exp_a
        level_coeff = 1.0 - exp_a
        var = (self.sigma ** 2) * (1.0 - np.exp(-2.0 * self.a * dt)) / (2.0 * self.a)
        std = np.sqrt(var)

        for k in range(1, M + 1):
            z = rng.standard_normal(I)
            r_prev = rates[k - 1, :]
            rates[k, :] = r_prev * mean_coeff + self.b * level_coeff + std * z

        return SimulationResult(times=times, rates=rates)

    def zcb_price(self, t: float, T: float, r_t: Optional[float] = None) -> float:
        if r_t is None:
            r_t = self.r0
        t = float(t)
        T = float(T)
        if T < t:
            return 0.0
        tau = T - t
        if tau == 0.0:
            return 1.0

        B = (1.0 - np.exp(-self.a * tau)) / self.a
        A_term = (self.b - (self.sigma ** 2) / (2.0 * self.a ** 2)) * (B - tau) - (self.sigma ** 2) * (B ** 2) / (4.0 * self.a)
        A = np.exp(A_term)
        return float(A * np.exp(-B * float(r_t)))
