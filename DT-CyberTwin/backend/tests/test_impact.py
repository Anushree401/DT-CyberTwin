from impact.metrics import calculate_impact_metrics
from impact.propagation import propagate_temperature_impact


def test_metrics_identify_overheating():
    metrics = calculate_impact_metrics([25, 40, 72, 80], safe_max=70, setpoint=40)
    assert metrics["safe"] is False
    assert metrics["overheat_steps"] == 2
    assert metrics["peak_temperature"] == 80
    assert metrics["impact_score"] > 0


def test_impact_propagation_explains_threshold_breach():
    findings = propagate_temperature_impact([
        {"timestep": 0, "actual_temperature": 45, "sensor_compromised": False},
        {"timestep": 1, "actual_temperature": 75, "sensor_compromised": True},
        {"timestep": 2, "actual_temperature": 90, "sensor_compromised": True},
    ])
    assert [item["severity"] for item in findings] == ["high", "critical"]


def test_metrics_expose_safety_limits_separately_from_setpoint():
    metrics = calculate_impact_metrics([40, 45.104], safe_min=0, safe_max=70, setpoint=40)
    assert metrics["safe"] is True
    assert metrics["safe_max"] == 70.0
    assert metrics["setpoint"] == 40.0
    assert metrics["maximum_setpoint_deviation"] == 5.104
    assert metrics["overheat_steps"] == 0


def test_metrics_reject_invalid_safety_range():
    import pytest

    with pytest.raises(ValueError, match="safe_min must be less than safe_max"):
        calculate_impact_metrics([25], safe_min=70, safe_max=70)
