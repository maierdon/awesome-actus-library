from __future__ import annotations
import warnings
from dataclasses import dataclass
from typing import Iterable, Optional, Union, Literal
import numpy as np

from .spline import NaturalCubicSpline1D

@dataclass(frozen=True)
class CurveCalibrator:
    """Calibrate a smooth spot/discount curve from market inputs."""
    times: np.ndarray
    P: np.ndarray
    R: np.ndarray
    _spline_R: NaturalCubicSpline1D
    t_min: float
    t_max: float
    P_0_tmax: float
    F_0_tmax: float
    extrapolation_mode: Literal["flat", "strict"] = "flat"

    @staticmethod
    def from_market(
        times: Iterable[float],
        *,
        zcb_prices: Optional[Iterable[float]] = None,
        spot_rates: Optional[Iterable[float]] = None,
        extrapolation_mode: Literal["flat", "strict"] = "flat",
    ) -> "CurveCalibrator":
        times_arr = np.asarray(list(times), dtype=float)
        if times_arr.ndim != 1 or times_arr.size < 2:
            raise ValueError("times must be a 1D array with at least 2 points")

        sort_idx = np.argsort(times_arr)
        times_arr = times_arr[sort_idx]
        if np.any(np.diff(times_arr) <= 0):
            raise ValueError("times must be strictly increasing")

        provided = (zcb_prices is not None) + (spot_rates is not None)
        if provided != 1:
            raise ValueError("Provide exactly one of zcb_prices or spot_rates")

        prepend_zero = bool(times_arr[0] > 0.0)
        if prepend_zero:
            times_full = np.insert(times_arr, 0, 0.0)
        else:
            times_full = times_arr

        safe_times = np.where(times_full == 0.0, 1e-12, times_full)

        if zcb_prices is not None:
            P_sorted = np.asarray(list(zcb_prices), dtype=float)[sort_idx]
            if np.any(P_sorted <= 0.0):
                raise ValueError("All zcb_prices must be > 0")
            P_full = np.insert(P_sorted, 0, 1.0) if prepend_zero else P_sorted
            R_full = -np.log(P_full) / safe_times
        else:
            R_sorted = np.asarray(list(spot_rates), dtype=float)[sort_idx]
            if prepend_zero:
                R0 = float(R_sorted[0])
                R_full = np.insert(R_sorted, 0, R0)
            else:
                R_full = R_sorted
            P_full = np.exp(-R_full * times_full)

        spline = NaturalCubicSpline1D.fit(times_full, R_full)

        t_min = float(times_full[0])
        t_max = float(times_full[-1])
        P_0_tmax = float(P_full[-1])

        R_tmax = float(spline.evaluate(t_max))
        dR_dt_tmax = float(spline.evaluate_first_derivative(t_max))
        F_0_tmax = float(R_tmax + t_max * dR_dt_tmax)

        return CurveCalibrator(
            times=times_full,
            P=P_full,
            R=R_full,
            _spline_R=spline,
            t_min=t_min,
            t_max=t_max,
            P_0_tmax=P_0_tmax,
            F_0_tmax=F_0_tmax,
            extrapolation_mode=extrapolation_mode,
        )

    def _check_extrapolation(self, t: np.ndarray) -> None:
        if self.extrapolation_mode == "strict":
            if np.any(t > self.t_max):
                max_q = np.max(t)
                raise ValueError(
                    f"Extrapolation requested: t={max_q:.2f} > t_max={self.t_max:.2f}. "
                    f"Use extrapolation_mode='flat' to allow."
                )
        elif self.extrapolation_mode == "flat":
             if np.any(t > self.t_max):
                max_q = np.max(t)
                warnings.warn(
                    f"Extrapolating beyond curve data: t={max_q:.2f} > t_max={self.t_max:.2f}. "
                    f"Using flat-forward assumption.",
                    UserWarning, stacklevel=3
                )

    def spot_rate(self, t: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        arr = np.asarray(t, dtype=float)
        scalar = arr.ndim == 0
        if scalar:
            arr = arr.reshape(1)

        arr_safe = np.maximum(arr, 0.0)
        self._check_extrapolation(arr_safe)

        res = np.empty_like(arr_safe)
        in_range = arr_safe <= self.t_max

        if np.any(in_range):
            res[in_range] = self._spline_R.evaluate(arr_safe[in_range])

        if np.any(~in_range):
            tt = arr_safe[~in_range]
            P = self.P_0_tmax * np.exp(-self.F_0_tmax * (tt - self.t_max))
            res[~in_range] = -np.log(P) / np.maximum(tt, 1e-12)

        return float(res[0]) if scalar else res

    def zcb_price(self, t: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        arr = np.asarray(t, dtype=float)
        scalar = arr.ndim == 0
        if scalar:
            arr = arr.reshape(1)

        arr_safe = np.maximum(arr, 0.0)
        self._check_extrapolation(arr_safe)

        res = np.empty_like(arr_safe)
        in_range = arr_safe <= self.t_max

        if np.any(in_range):
            R_t = self.spot_rate(arr_safe[in_range])
            res[in_range] = np.exp(-np.asarray(R_t, dtype=float) * arr_safe[in_range])

        if np.any(~in_range):
            tt = arr_safe[~in_range]
            res[~in_range] = self.P_0_tmax * np.exp(-self.F_0_tmax * (tt - self.t_max))

        return float(res[0]) if scalar else res

    def forward_rate(self, t: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        arr = np.asarray(t, dtype=float)
        scalar = arr.ndim == 0
        if scalar:
            arr = arr.reshape(1)

        arr_safe = np.maximum(arr, 0.0)
        self._check_extrapolation(arr_safe)

        res = np.empty_like(arr_safe)
        in_range = arr_safe <= self.t_max

        if np.any(in_range):
            R_t = self._spline_R.evaluate(arr_safe[in_range])
            dR = self._spline_R.evaluate_first_derivative(arr_safe[in_range])
            res[in_range] = R_t + arr_safe[in_range] * dR

        if np.any(~in_range):
            res[~in_range] = self.F_0_tmax

        return float(res[0]) if scalar else res

    def forward_rate_slope(self, t: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        arr = np.asarray(t, dtype=float)
        scalar = arr.ndim == 0
        if scalar:
            arr = arr.reshape(1)

        arr_safe = np.maximum(arr, 0.0)
        self._check_extrapolation(arr_safe)

        res = np.empty_like(arr_safe)
        in_range = arr_safe <= self.t_max

        if np.any(in_range):
            dR = self._spline_R.evaluate_first_derivative(arr_safe[in_range])
            d2R = self._spline_R.evaluate_second_derivative(arr_safe[in_range])
            res[in_range] = 2.0 * dR + arr_safe[in_range] * d2R

        if np.any(~in_range):
            res[~in_range] = 0.0

        return float(res[0]) if scalar else res
