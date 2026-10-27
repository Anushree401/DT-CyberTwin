from cps.dynamics import TemperatureCPS


def test_cps_step_is_deterministic_and_bounded():
    first = TemperatureCPS()
    second = TemperatureCPS()
    results_a = [first.step(step).model_dump() for step in range(5)]
    results_b = [second.step(step).model_dump() for step in range(5)]
    assert results_a == results_b
    assert all(0.0 <= row["heater_output"] <= 1.0 for row in results_a)


def test_spoofed_low_reading_keeps_heater_on_at_high_actual_temperature():
    cps = TemperatureCPS(initial_temperature=75.0, setpoint=40.0)
    cps.sensor.spoof(-40.0)
    result = cps.step(0)
    assert result.actual_temperature > 70.0
    assert result.reported_temperature < 40.0
    assert result.heater_output == 1.0
    assert result.sensor_compromised is True


def test_step_distinguishes_measurement_from_post_step_temperature():
    cps = TemperatureCPS(initial_temperature=25.0, setpoint=40.0)
    result = cps.step(0)
    assert result.measured_temperature == 25.0
    assert result.reported_temperature == 25.0
    assert result.actual_temperature > result.measured_temperature
