"""FastAPI entry point for DT-CyberTwin."""
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import SimulationRequest, SimulationResponse
from scenarios.industrial_temperature import build_industrial_temperature_twin
from scenarios.runner import run_industrial_temperature_scenario

app = FastAPI(
    title="DT-CyberTwin",
    version="0.1.0",
    description="Deterministic cyber-physical simulation for industrial temperature control.",
)

_allowed_origins = os.getenv("DT_CYBERTWIN_CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in _allowed_origins.split(",") if origin.strip()],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "dt-cybertwin"}


@app.get("/twin")
def get_twin() -> dict:
    twin = build_industrial_temperature_twin()
    return {
        "nodes": [twin.get_node(node_id).model_dump(mode="json") for node_id in twin.graph.nodes],
        "edges": [twin.get_edge(source, target).model_dump(mode="json") for source, target in twin.graph.edges],
    }


@app.post("/simulations/industrial-temperature", response_model=SimulationResponse)
def simulate_temperature(request: SimulationRequest) -> dict:
    try:
        return run_industrial_temperature_scenario(request)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
