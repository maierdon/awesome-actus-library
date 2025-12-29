from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
import numpy as np

@dataclass(frozen=True)
class NaturalCubicSpline1D:
    x: np.ndarray
    y: np.ndarray
    m: np.ndarray  # second derivatives

    @staticmethod
    def fit(x: Iterable[float], y: Iterable[float]) -> "NaturalCubicSpline1D":
        x_arr = np.asarray(list(x), dtype=float)
        y_arr = np.asarray(list(y), dtype=float)

        if x_arr.ndim != 1 or y_arr.ndim != 1:
            raise ValueError("x and y must be 1D")
        if x_arr.size != y_arr.size:
            raise ValueError("x and y must have the same length")
        if x_arr.size < 2:
            raise ValueError("Need at least 2 points")

        sort_idx = np.argsort(x_arr)
        x_arr = x_arr[sort_idx]
        y_arr = y_arr[sort_idx]

        dx = np.diff(x_arr)
        if np.any(dx <= 0):
            raise ValueError("x must be strictly increasing")

        n = x_arr.size
        m = np.zeros(n, dtype=float)

        if n <= 2:
            return NaturalCubicSpline1D(x=x_arr, y=y_arr, m=m)

        a = dx[:-1]
        b = 2.0 * (dx[:-1] + dx[1:])
        c = dx[1:]
        rhs = 6.0 * ((np.diff(y_arr[1:]) / dx[1:]) - (np.diff(y_arr[:-1]) / dx[:-1]))

        cp = np.empty_like(c)
        dp = np.empty_like(rhs)

        cp[0] = c[0] / b[0]
        dp[0] = rhs[0] / b[0]
        for i in range(1, n - 2):
            denom = b[i] - a[i - 1] * cp[i - 1]
            cp[i] = c[i] / denom
            dp[i] = (rhs[i] - a[i - 1] * dp[i - 1]) / denom

        m_inner = np.empty(n - 2, dtype=float)
        m_inner[-1] = dp[-1]
        for i in range(n - 4, -1, -1):
            m_inner[i] = dp[i] - cp[i] * m_inner[i + 1]

        m[1:-1] = m_inner
        return NaturalCubicSpline1D(x=x_arr, y=y_arr, m=m)

    def _interval_indices(self, xq: np.ndarray) -> np.ndarray:
        idx = np.searchsorted(self.x, xq, side="right") - 1
        return np.clip(idx, 0, self.x.size - 2)

    def evaluate(self, xq: Iterable[float] | float) -> np.ndarray | float:
        xq_arr = np.asarray(xq, dtype=float)
        scalar = xq_arr.ndim == 0
        if scalar:
            xq_arr = xq_arr.reshape(1)

        i = self._interval_indices(xq_arr)
        x_i = self.x[i]
        x_ip1 = self.x[i + 1]
        h = x_ip1 - x_i
        a = (x_ip1 - xq_arr) / h
        b = (xq_arr - x_i) / h

        y = (
            a * self.y[i]
            + b * self.y[i + 1]
            + ((a**3 - a) * self.m[i] + (b**3 - b) * self.m[i + 1]) * (h**2) / 6.0
        )
        return float(y[0]) if scalar else y

    def evaluate_first_derivative(self, xq: Iterable[float] | float) -> np.ndarray | float:
        xq_arr = np.asarray(xq, dtype=float)
        scalar = xq_arr.ndim == 0
        if scalar:
            xq_arr = xq_arr.reshape(1)

        i = self._interval_indices(xq_arr)
        x_i = self.x[i]
        x_ip1 = self.x[i + 1]
        h = x_ip1 - x_i
        a = (x_ip1 - xq_arr) / h
        b = (xq_arr - x_i) / h

        dy = (
            (self.y[i + 1] - self.y[i]) / h
            + (-(3 * a**2 - 1) * self.m[i] + (3 * b**2 - 1) * self.m[i + 1]) * h / 6.0
        )
        return float(dy[0]) if scalar else dy

    def evaluate_second_derivative(self, xq: Iterable[float] | float) -> np.ndarray | float:
        xq_arr = np.asarray(xq, dtype=float)
        scalar = xq_arr.ndim == 0
        if scalar:
            xq_arr = xq_arr.reshape(1)

        i = self._interval_indices(xq_arr)
        x_i = self.x[i]
        x_ip1 = self.x[i + 1]
        h = x_ip1 - x_i
        a = (x_ip1 - xq_arr) / h
        b = (xq_arr - x_i) / h

        d2 = a * self.m[i] + b * self.m[i + 1]
        return float(d2[0]) if scalar else d2
