from __future__ import annotations
from typing import Optional
import numpy as np
from ..simulation import SimulationResult
from ..calibration.curve import CurveCalibrator
from .base import ShortRateModel

class HoLee(ShortRateModel):
    """Ho–Lee (1986): dr = theta(t)dt + sigma dW, curve-fit via theta(t)."""
    name = "ho_lee"

    def __init__(self, *, r0: float, sigma: float, calibrator: CurveCalibrator, seed: Optional[int] = None):
        super().__init__(r0=r0, seed=seed)
        if sigma < 0:
            raise ValueError(f"sigma must be non-negative, got {sigma}")
        if calibrator is None:
            raise ValueError("Ho-Lee requires a CurveCalibrator for no-arbitrage fitting")
        self.sigma = float(sigma)
        self.cal = calibrator

    def theta(self, t: float) -> float:
        return float(self.cal.forward_rate_slope(t) + (self.sigma ** 2) * t)

    def _simulate_impl(self, *, T: float, M: int, I: int, rng: np.random.Generator) -> SimulationResult:
        if M <= 0 or I <= 0:
            raise ValueError("M and I must be positive")
        T = float(T)
        dt = T / float(M)
        times = np.linspace(0.0, T, M + 1)

        rates = np.empty((M + 1, I), dtype=float)
        rates[0, :] = self.r0

        sqrt_dt = np.sqrt(dt)
        for k in range(1, M + 1):
            t_prev = times[k - 1]
            z = rng.standard_normal(I)
            drift = self.theta(t_prev) * dt
            rates[k, :] = rates[k - 1, :] + drift + self.sigma * sqrt_dt * z

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

        P_0_T = self.cal.zcb_price(T)
        P_0_t = self.cal.zcb_price(t)
        F_0_t = self.cal.forward_rate(t)

        exponent = (F_0_t - float(r_t)) * tau - 0.5 * (self.sigma ** 2) * t * (tau ** 2)
        return float((P_0_T / P_0_t) * np.exp(exponent))
