"""API schemas for requesting and returning deterministic scenarios."""
from pydantic import BaseModel, Field


class SimulationRequest(BaseModel):
    steps: int = Field(default=12, ge=1, le=500)
    attack: bool = True
    attack_timestep: int = Field(default=2, ge=0, le=499)
    spoof_offset: float = Field(default=-30.0, ge=-100.0, le=100.0)
    initial_temperature: float = Field(default=25.0, ge=-50.0, le=200.0)
    setpoint: float = Field(default=40.0, ge=0.0, le=150.0)
    safe_max: float = Field(default=70.0, ge=1.0, le=250.0)


class SimulationResponse(BaseModel):
    scenario: str
    timesteps: list[dict]
    impacts: list[dict]
    metrics: dict
    timeline: list[dict]
    final_state: dict = Field(default_factory=dict)
