from __future__ import annotations
from typing import Optional
import numpy as np
from ..simulation import SimulationResult
from ..calibration.curve import CurveCalibrator
from .base import ShortRateModel

class HullWhite(ShortRateModel):
    """Hull–White 1-factor (1990): dr = (theta(t) - a r)dt + sigma dW."""
    name = "hull_white"

    def __init__(self, *, r0: float, a: float, sigma: float, calibrator: CurveCalibrator, seed: Optional[int] = None):
        super().__init__(r0=r0, seed=seed)
        if sigma < 0:
            raise ValueError(f"sigma must be non-negative, got {sigma}")
        if a <= 0:
            raise ValueError(f"mean-reversion speed 'a' must be positive, got {a}")
        if calibrator is None:
            raise ValueError("Hull-White requires a CurveCalibrator for no-arbitrage fitting")
        self.a = float(a)
        self.sigma = float(sigma)
        self.cal = calibrator

    def theta(self, t: float) -> float:
        dF = self.cal.forward_rate_slope(t)
        F = self.cal.forward_rate(t)
        convex = (self.sigma ** 2) / (2.0 * self.a) * (1.0 - np.exp(-2.0 * self.a * t))
        return float(dF + self.a * F + convex)

    def _simulate_impl(self, *, T: float, M: int, I: int, rng: np.random.Generator) -> SimulationResult:
        if M <= 0 or I <= 0:
            raise ValueError("M and I must be positive")
        T = float(T)
        dt = T / float(M)
        times = np.linspace(0.0, T, M + 1)

        rates = np.empty((M + 1, I), dtype=float)
        rates[0, :] = self.r0

        exp_a = np.exp(-self.a * dt)
        std = self.sigma * np.sqrt((1.0 - np.exp(-2.0 * self.a * dt)) / (2.0 * self.a))
        theta_coeff = (1.0 - exp_a) / self.a

        for k in range(1, M + 1):
            t_prev = times[k - 1]
            z = rng.standard_normal(I)
            th = self.theta(t_prev)
            rates[k, :] = rates[k - 1, :] * exp_a + th * theta_coeff + std * z

        return SimulationResult(times=times, rates=rates)

    def zcb_price(self, t: float, T: float, r_t: Optional[float] = None) -> float:
        if r_t is None:
            r_t = self.r0
        t = float(t)
        T = float(T)
        if T < t:
            return 0.0
        if t == 0.0:
            return float(self.cal.zcb_price(T))
        tau = T - t
        if tau == 0.0:
            return 1.0

        B = (1.0 - np.exp(-self.a * tau)) / self.a
        P_0_T = self.cal.zcb_price(T)
        P_0_t = self.cal.zcb_price(t)
        f_0_t = self.cal.forward_rate(t)

        term_drift = -B * (float(r_t) - f_0_t)
        term_conv = -(self.sigma ** 2) / (4.0 * self.a) * (1.0 - np.exp(-2.0 * self.a * t)) * (B ** 2)
        return float((P_0_T / P_0_t) * np.exp(term_drift + term_conv))
