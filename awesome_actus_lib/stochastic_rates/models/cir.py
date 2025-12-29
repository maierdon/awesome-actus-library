from __future__ import annotations
from typing import Optional
import warnings
import numpy as np
from ..simulation import SimulationResult
from .base import ShortRateModel

class CIR(ShortRateModel):
    """Cox–Ingersoll–Ross (1985): dr = a(b-r)dt + sigma*sqrt(r) dW."""
    name = "cir"

    def __init__(self, *, r0: float, a: float, b: float, sigma: float, seed: Optional[int] = None):
        super().__init__(r0=r0, seed=seed)
        if sigma < 0:
            raise ValueError(f"sigma must be non-negative, got {sigma}")
        if a <= 0:
            raise ValueError(f"mean-reversion speed 'a' must be positive, got {a}")
        if b < 0:
            raise ValueError(f"long-term mean 'b' must be non-negative for CIR, got {b}")
        if r0 < 0:
            raise ValueError(f"initial rate 'r0' must be non-negative for CIR, got {r0}")
        self.a = float(a)
        self.b = float(b)
        self.sigma = float(sigma)

        feller_lhs = 2.0 * self.a * self.b
        feller_rhs = self.sigma ** 2
        if feller_lhs < feller_rhs:
            warnings.warn(
                f"CIR Feller condition violated: 2ab={feller_lhs:.6f} < σ²={feller_rhs:.6f}. "
                f"Rates may touch zero during simulation.",
                UserWarning,
                stacklevel=2,
            )

    def _simulate_impl(self, *, T: float, M: int, I: int, rng: np.random.Generator) -> SimulationResult:
        if M <= 0 or I <= 0:
            raise ValueError("M and I must be positive")
        T = float(T)
        dt = T / float(M)
        times = np.linspace(0.0, T, M + 1)

        rates = np.empty((M + 1, I), dtype=float)
        rates[0, :] = max(self.r0, 0.0)

        exp_a = np.exp(-self.a * dt)
        c = (self.sigma ** 2) * (1.0 - exp_a) / (4.0 * self.a)
        d = 4.0 * self.a * self.b / (self.sigma ** 2)

        for k in range(1, M + 1):
            r_prev = np.maximum(rates[k - 1, :], 0.0)
            lam = (4.0 * self.a * exp_a * r_prev) / ((self.sigma ** 2) * (1.0 - exp_a))
            x = rng.noncentral_chisquare(df=d, nonc=lam, size=I)
            rates[k, :] = c * x

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

        gamma = np.sqrt(self.a ** 2 + 2.0 * (self.sigma ** 2))
        denom = (gamma + self.a) * (np.exp(gamma * tau) - 1.0) + 2.0 * gamma
        B = (2.0 * (np.exp(gamma * tau) - 1.0)) / denom
        A = ((2.0 * gamma * np.exp((self.a + gamma) * tau / 2.0)) / denom) ** (2.0 * self.a * self.b / (self.sigma ** 2))
        return float(A * np.exp(-B * float(max(r_t, 0.0))))
