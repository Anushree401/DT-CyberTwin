"""Evaluation metrics for the simulated temperature process.

Safety is evaluated against [safe_min, safe_max]. The control setpoint is a
separate target and deviations from it are not automatically safety violations.
"""
from typing import Iterable


def calculate_impact_metrics(
    actual_temperatures: Iterable[float],
    *,
    safe_min: float = 0.0,
    safe_max: float = 70.0,
    setpoint: float = 40.0,
) -> dict:
    if safe_min >= safe_max:
        raise ValueError("safe_min must be less than safe_max")

    values = [float(value) for value in actual_temperatures]
    if not values:
        return {
            "sample_count": 0,
            "peak_temperature": None,
            "safe_min": float(safe_min),
            "safe_max": float(safe_max),
            "setpoint": float(setpoint),
            "overheat_steps": 0,
            "maximum_setpoint_deviation": 0.0,
            "impact_score": 0.0,
            "safe": True,
        }

    peak = max(values)
    out_of_range_steps = sum(value > safe_max or value < safe_min for value in values)
    max_deviation = max(abs(value - setpoint) for value in values)
    excess = sum(max(0.0, value - safe_max, safe_min - value) for value in values)
    score = min(100.0, round(excess * 2.0, 2))
    return {
        "sample_count": len(values),
        "peak_temperature": round(peak, 3),
        "safe_min": float(safe_min),
        "safe_max": float(safe_max),
        "setpoint": float(setpoint),
        "overheat_steps": out_of_range_steps,
        "maximum_setpoint_deviation": round(max_deviation, 3),
        "impact_score": score,
        "safe": out_of_range_steps == 0,
    }
