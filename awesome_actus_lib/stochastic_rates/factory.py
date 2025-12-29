from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from .models.base import ShortRateModel
from .calibration.curve import CurveCalibrator
from .models import CIR, HoLee, HullWhite, Vasicek


@dataclass(frozen=True)
class ModelInfo:
    key: str
    title: str
    strengths: List[str]
    limitations: List[str]
    suited_for: List[str]


MODEL_CATALOG: Dict[str, ModelInfo] = {
    "vasicek": ModelInfo(
        key="vasicek",
        title="Vasicek (mean-reverting Gaussian)",
        strengths=["Mean reversion", "Closed-form ZCB pricing", "Fast simulation"],
        limitations=["Can generate negative rates", "Does not exactly fit initial curve"],
        suited_for=["Teaching", "Quick stress testing", "Benchmarking"],
    ),
    "cir": ModelInfo(
        key="cir",
        title="CIR (mean-reverting square-root)",
        strengths=["Non-negative rates (under Feller)", "Closed-form ZCB pricing"],
        limitations=["Does not exactly fit initial curve", "Parameter constraints may be restrictive"],
        suited_for=["Long-horizon simulations where non-negativity matters", "Regulatory-style scenarios"],
    ),
    "ho_lee": ModelInfo(
        key="ho_lee",
        title="Ho–Lee (no-arbitrage, curve-fitting)",
        strengths=["Exact fit to initial discount curve", "Analytic ZCB pricing"],
        limitations=["No mean reversion → long-horizon drift can be unrealistic", "Gaussian → negative rates possible"],
        suited_for=["Short-horizon pricing", "Pedagogical comparison of no-arbitrage drift"],
    ),
    "hull_white": ModelInfo(
        key="hull_white",
        title="Hull–White 1F (no-arbitrage mean-reverting)",
        strengths=["Exact fit to initial curve", "Mean reversion stabilizes long horizons", "Industry-standard 1-factor model"],
        limitations=["Gaussian → negative rates possible", "One factor may underfit volatility surface"],
        suited_for=["ALM / pension fund scenario generation", "Risk analytics", "Benchmark model for term-structure work"],
    ),
}


def available_models() -> List[str]:
    return list(MODEL_CATALOG.keys())


def describe_models() -> List[ModelInfo]:
    return [MODEL_CATALOG[k] for k in available_models()]


def create_model(model: str, **params: Any) -> ShortRateModel:
    """Instantiate a short-rate model.

    Required parameters by model:
    - vasicek: r0, a, b, sigma
    - cir: r0, a, b, sigma
    - ho_lee: r0, sigma, calibrator
    - hull_white: r0, a, sigma, calibrator
    """

    key = (model or "").lower().replace("-", "_").strip()

    seed = params.get("seed")

    if key == "vasicek":
        return Vasicek(r0=params["r0"], a=params["a"], b=params["b"], sigma=params["sigma"], seed=seed)
    if key == "cir":
        return CIR(r0=params["r0"], a=params["a"], b=params["b"], sigma=params["sigma"], seed=seed)
    if key in ("ho_lee", "holee"):
        return HoLee(r0=params["r0"], sigma=params["sigma"], calibrator=params["calibrator"], seed=seed)
    if key in ("hull_white", "hullwhite"):
        return HullWhite(r0=params["r0"], a=params["a"], sigma=params["sigma"], calibrator=params["calibrator"], seed=seed)

    raise ValueError(f"Unknown model='{model}'. Available: {', '.join(available_models())}")
