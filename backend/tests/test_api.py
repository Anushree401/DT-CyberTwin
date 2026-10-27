from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_twin_endpoint_returns_graph():
    response = client.get("/twin")
    assert response.status_code == 200
    assert len(response.json()["nodes"]) == 8
    assert len(response.json()["edges"]) == 8


def test_simulation_endpoint_returns_timeline_and_metrics():
    response = client.post("/simulations/industrial-temperature", json={"steps": 12, "attack": True})
    assert response.status_code == 200
    payload = response.json()
    assert len(payload["timesteps"]) == 12
    assert "impact_score" in payload["metrics"]
    assert any(event["action"] == "sensor_spoofing_started" for event in payload["timeline"])


def test_attack_timestep_must_fit_simulation():
    response = client.post("/simulations/industrial-temperature", json={"steps": 3, "attack": True, "attack_timestep": 3})
    assert response.status_code == 422


def test_simulation_metrics_include_safety_limits():
    response = client.post("/simulations/industrial-temperature", json={"steps": 12, "attack": False, "setpoint": 40, "safe_max": 70})
    assert response.status_code == 200
    metrics = response.json()["metrics"]
    assert metrics["safe_min"] == 0.0
    assert metrics["safe_max"] == 70.0
    assert metrics["setpoint"] == 40.0
