export interface TwinNode { id: string; name: string; type: string; state: Record<string, unknown>; metadata?: Record<string, unknown> }
export interface TwinEdge { source: string; target: string; type: string; metadata?: Record<string, unknown> }
export interface TwinGraph { nodes: TwinNode[]; edges: TwinEdge[] }
export interface Timestep { timestep: number; actual_temperature: number; measured_temperature: number; reported_temperature: number; heater_output: number; actuator_status: string; decision_reason: string; sensor_compromised: boolean }
export interface Impact { timestep: number; severity: string; actual_temperature: number; description: string; cause: string }
export interface Metrics { sample_count: number; peak_temperature: number | null; safe_min: number; safe_max: number; setpoint: number; overheat_steps: number; maximum_setpoint_deviation: number; impact_score: number; safe: boolean }
export interface TimelineEvent { timestep: number; type: string; source: string; target?: string | null; action: string; parameters: Record<string, unknown> }
export interface SimulationResult { scenario: string; timesteps: Timestep[]; impacts: Impact[]; metrics: Metrics; timeline: TimelineEvent[]; final_state: Record<string, TwinNode> }
