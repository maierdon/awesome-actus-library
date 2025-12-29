"""Stochastic interest rate models & ALM scenario generation.

Modules
-------
models: Short-rate model implementations (Vasicek, CIR, Ho-Lee, Hull-White).
calibration: Term structure calibration (CurveCalibrator, Splines).
simulation: Monte Carlo simulation containers.
integration: Adapters for ACTUS risk factor integration.
factory: Helper to instantiate models by name.
"""

from .factory import create_model, available_models, describe_models
from .models.base import ShortRateModel
from .calibration.curve import CurveCalibrator
from .simulation import SimulationResult
from .integration import simulation_to_reference_index, simulation_to_scenarios

__all__ = [
    "create_model",
    "available_models",
    "describe_models",
    "ShortRateModel",
    "CurveCalibrator",
    "SimulationResult",
    "simulation_to_reference_index",
    "simulation_to_scenarios",
]
