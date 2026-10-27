"""Translate CPS telemetry into explainable impact findings."""


def propagate_temperature_impact(
    samples: list[dict], *, safe_max: float = 70.0, critical_max: float = 85.0
) -> list[dict]:
    findings: list[dict] = []
    for sample in samples:
        temperature = float(sample["actual_temperature"])
        timestep = int(sample["timestep"])
        if temperature > critical_max:
            severity, description = "critical", "Temperature exceeded the critical operating limit."
        elif temperature > safe_max:
            severity, description = "high", "Temperature exceeded the safe operating limit."
        else:
            continue
        findings.append({
            "timestep": timestep,
            "severity": severity,
            "actual_temperature": temperature,
            "description": description,
            "cause": "heater remained active while reported sensor temperature was below setpoint" if sample.get("sensor_compromised") else "physical process exceeded its configured limit",
        })
    return findings
