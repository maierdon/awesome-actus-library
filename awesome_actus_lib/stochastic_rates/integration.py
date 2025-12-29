from __future__ import annotations
import warnings
from dataclasses import dataclass
from typing import Dict, List, Optional
import numpy as np
import pandas as pd

from .simulation import SimulationResult

# Try import from package, assuming standard structure
try:
    from awesome_actus_lib.models.RiskFactor import ReferenceIndex
except ImportError:
    # Try relative if absolute fails (e.g. during local dev without install)
    try:
        from ..models.RiskFactor import ReferenceIndex
    except ImportError:
        # Fallback stub for standalone testing/examples
        class ReferenceIndex:
            def __init__(self, marketObjectCode, source):
                self.marketObjectCode = marketObjectCode
                self.source = source

# ... (freq map code remains)

_FREQ_MAP = {
    "D": lambda i: pd.DateOffset(days=i),
    "W": lambda i: pd.DateOffset(weeks=i),
    "M": lambda i: pd.DateOffset(months=i),
    "Q": lambda i: pd.DateOffset(months=3 * i),
    "Y": lambda i: pd.DateOffset(years=i),
    "A": lambda i: pd.DateOffset(years=i),
}

def _parse_freq(freq: str) -> str:
    freq_upper = freq.upper().strip()
    if freq_upper in _FREQ_MAP:
        return freq_upper
    if freq_upper.startswith("P") and "L" in freq_upper:
        for char in reversed(freq_upper.split("L")[0]):
            if char.isalpha() and char != "P":
                if char in _FREQ_MAP:
                    return char
                break
    for char in freq_upper:
        if char in _FREQ_MAP:
            return char
    raise ValueError(f"Unknown frequency format: {freq!r}")

def supported_frequencies() -> List[str]:
    return list(_FREQ_MAP.keys())

@dataclass(frozen=True)
class ScenarioSet:
    market_code: str
    scenarios: Dict[str, object] 

    def __len__(self) -> int:
        return len(self.scenarios)

    def __iter__(self):
        return iter(self.scenarios.items())

    def scenario_names(self) -> List[str]:
        return list(self.scenarios.keys())

def simulation_to_reference_index(
    sim: SimulationResult,
    *,
    base_date: str,
    market_code: str,
    path: int = 0,
    freq: str = "M",
):
    try:
        from awesome_actus_lib.models.RiskFactor import ReferenceIndex
    except ImportError:
        try:
            from ..models.RiskFactor import ReferenceIndex
        except ImportError:
            # Fallback stub
            class ReferenceIndex:
                def __init__(self, marketObjectCode, source):
                    self.marketObjectCode = marketObjectCode
                    self.source = source

    sim.assert_valid()
    if path < 0 or path >= sim.rates.shape[1]:
        raise IndexError(f"path index out of range: {path}")

    base = pd.to_datetime(base_date)
    freq_key = _parse_freq(freq)
    offset_fn = _FREQ_MAP[freq_key]

    _EXPECTED_STEPS_PER_YEAR = {"D": 365, "W": 52, "M": 12, "Q": 4, "Y": 1, "A": 1}
    if freq_key in _EXPECTED_STEPS_PER_YEAR:
        expected_steps = int(sim.horizon * _EXPECTED_STEPS_PER_YEAR[freq_key])
        actual_steps = sim.n_steps 
        # actual_steps is M (number of intervals). len(times) is M+1.
        # The Warning should compare intervals (M) vs expected intervals.
        if abs(actual_steps - expected_steps) > 1:
            warnings.warn(
                f"Time-step mismatch: simulation has {actual_steps} steps but freq='{freq}' "
                f"expects ~{expected_steps} steps. Use M={expected_steps} for correct alignment.",
                UserWarning,
                stacklevel=2,
            )

    _PANDAS_FREQ_MAP = {"D": "D", "W": "W", "M": "MS", "Q": "QS", "Y": "YS", "A": "YS"}
    pandas_freq = _PANDAS_FREQ_MAP.get(freq_key, freq_key)

    try:
        dates = pd.date_range(start=base, periods=sim.times.size, freq=pandas_freq).strftime("%Y-%m-%d").tolist()
    except ValueError:
        # Fallback for unsupported frequencies (e.g. custom ones not in map)
        offset_fn = _FREQ_MAP[freq_key]
        dates = [(base + offset_fn(i)).strftime("%Y-%m-%d") for i in range(sim.times.size)]

    df = pd.DataFrame({
        "date": dates,
        "value": sim.rates[:, path],
    })

    return ReferenceIndex(marketObjectCode=market_code, source=df)

def simulation_to_scenarios(
    sim: SimulationResult,
    *,
    base_date: str,
    market_code: str,
    max_scenarios: Optional[int] = None,
    freq: str = "M",
    name_prefix: str = "SCEN",
) -> ScenarioSet:
    sim.assert_valid()
    n_paths = sim.rates.shape[1]
    n_use = n_paths if (max_scenarios is None) else min(int(max_scenarios), n_paths)

    scenarios: Dict[str, object] = {}
    for j in range(n_use):
        scenarios[f"{name_prefix}_{j:04d}"] = simulation_to_reference_index(
            sim, base_date=base_date, market_code=market_code, path=j, freq=freq
        )

    return ScenarioSet(market_code=market_code, scenarios=scenarios)
