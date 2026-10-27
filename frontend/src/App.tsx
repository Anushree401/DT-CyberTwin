import { useCallback, useEffect, useMemo, useState } from 'react'
import { Activity, AlertTriangle, CheckCircle2, CircleHelp, Cpu, GitBranch, Play, RefreshCw, ShieldAlert, Thermometer, Wifi, Zap, Maximize2, Minimize2, X } from 'lucide-react'
import { Background, Controls, MiniMap, ReactFlow, type Edge, type Node } from '@xyflow/react'
import { CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import type { Impact, SimulationResult, TimelineEvent, TwinGraph } from './types'

const API = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000'
const positions: Record<string, { x: number; y: number }> = {
  'operator-01': { x: 0, y: 110 }, 'workstation-01': { x: 210, y: 110 }, 'gateway-01': { x: 420, y: 110 }, 'plc-01': { x: 630, y: 110 },
  'sensor-01': { x: 420, y: 320 }, 'controller-01': { x: 630, y: 320 }, 'actuator-01': { x: 840, y: 320 }, 'process-01': { x: 1050, y: 320 },
}
const icons: Record<string, typeof Cpu> = { user: Wifi, workstation: Cpu, gateway: GitBranch, plc: Cpu, sensor: Activity, controller: Cpu, actuator: Zap, physical_process: Thermometer }

function nodeLabel(type: string) { return type.replaceAll('_', ' ') }
function Topology({ graph, result }: { graph: TwinGraph | null; result: SimulationResult | null }) {
  const compromised = useMemo(() => new Set(Object.values(result?.final_state ?? {}).filter(n => Boolean(n.state?.compromised)).map(n => n.id)), [result])
  const nodes: Node[] = useMemo(() => (graph?.nodes ?? []).map(n => ({
    id: n.id, position: positions[n.id] ?? { x: 0, y: 0 },
    data: { label: <div className="node-label"><span className={`node-icon ${compromised.has(n.id) ? 'danger' : ''}`}>{(() => { const Icon = icons[n.type] ?? Cpu; return <Icon size={16} /> })()}</span><span><strong>{n.name}</strong><small>{nodeLabel(n.type)}</small></span>{compromised.has(n.id) && <span className="compromised-dot" />}</div> },
    className: compromised.has(n.id) ? 'twin-node compromised' : 'twin-node',
    style: { width: 208, minHeight: 76 },
  })), [graph, compromised])
  const edges: Edge[] = useMemo(() => (graph?.edges ?? []).map((e, i) => ({ id: `${e.source}-${e.target}-${i}`, source: e.source, target: e.target, label: e.type, animated: compromised.has(e.source) || compromised.has(e.target), style: { stroke: compromised.has(e.source) || compromised.has(e.target) ? '#fb7185' : '#475569', strokeWidth: 1.6 }, labelStyle: { fill: '#c4d0e1', fontSize: 11, fontWeight: 600 } })), [graph, compromised])
  return <div className="topology"><ReactFlow nodes={nodes} edges={edges} fitView fitViewOptions={{ padding: 0.18 }} nodesDraggable={false} nodesConnectable={false} elementsSelectable={false}><Background color="#253047" gap={18} /><Controls /><MiniMap nodeColor={n => n.className?.toString().includes('compromised') ? '#fb7185' : '#64748b'} /></ReactFlow></div>
}
function formatNumber(value: number | null | undefined) { return value == null ? '—' : value.toFixed(2) }
function severityClass(severity: string) { return severity.toLowerCase() === 'critical' ? 'critical' : severity.toLowerCase() === 'high' ? 'high' : 'medium' }
function EventRow({ event }: { event: TimelineEvent }) { return <div className="event-row"><span className="event-step">T{event.timestep}</span><span className={`event-type ${event.type}`}>{event.type.replaceAll('_', ' ')}</span><span className="event-copy"><strong>{event.action.replaceAll('_', ' ')}</strong><small>{event.source}{event.target ? ` → ${event.target}` : ''}</small></span></div> }
function ImpactRow({ impact }: { impact: Impact }) { return <div className="impact-row"><span className={`severity ${severityClass(impact.severity)}`}>{impact.severity}</span><div><strong>{impact.description}</strong><p>{impact.cause}</p><small>Step {impact.timestep} · {formatNumber(impact.actual_temperature)} temperature units</small></div></div> }

export default function App() {
  const [graph, setGraph] = useState<TwinGraph | null>(null)
  const [result, setResult] = useState<SimulationResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [attack, setAttack] = useState(true)
  const [steps, setSteps] = useState(12)
  const [attackTimestep, setAttackTimestep] = useState(2)
  const [spoofOffset, setSpoofOffset] = useState(-30)
  const [initialTemperature, setInitialTemperature] = useState(25)
  const [setpoint, setSetpoint] = useState(40)
  const [safeMax, setSafeMax] = useState(70)
  const [topologyExpanded, setTopologyExpanded] = useState(false)

  const loadGraph = useCallback(async () => {
    try { const response = await fetch(`${API}/twin`); if (!response.ok) throw new Error(`Graph request failed (${response.status})`); setGraph(await response.json()) }
    catch (e) { setError(e instanceof Error ? e.message : 'Could not load twin graph') }
  }, [])
  useEffect(() => { void loadGraph() }, [loadGraph])

  const runSimulation = async (overrideAttack = attack) => {
    setLoading(true); setError('')
    try {
      const response = await fetch(`${API}/simulations/industrial-temperature`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ steps, attack: overrideAttack, attack_timestep: attackTimestep, spoof_offset: spoofOffset, initial_temperature: initialTemperature, setpoint, safe_max: safeMax }) })
      const payload = await response.json()
      if (!response.ok) throw new Error(typeof payload.detail === 'string' ? payload.detail : `Simulation failed (${response.status})`)
      setAttack(overrideAttack); setResult(payload as SimulationResult)
    } catch (e) { setError(`${e instanceof Error ? e.message : 'Simulation request failed'}. Check that the FastAPI backend is running at ${API}.`) }
    finally { setLoading(false) }
  }

  const chartData = result?.timesteps ?? []
  const stateCounts = useMemo(() => { const values = Object.values(result?.final_state ?? {}); return { compromised: values.filter(n => Boolean(n.state?.compromised)).length, assets: graph?.nodes.length ?? 0 } }, [result, graph])

  useEffect(() => {
    if (!topologyExpanded) return
    const onKeyDown = (event: KeyboardEvent) => { if (event.key === 'Escape') setTopologyExpanded(false) }
    window.addEventListener('keydown', onKeyDown)
    document.body.classList.add('topology-expanded-open')
    return () => { window.removeEventListener('keydown', onKeyDown); document.body.classList.remove('topology-expanded-open') }
  }, [topologyExpanded])

  return <main className="app-shell">
    <header className="topbar"><div className="brand-mark"><GitBranch size={21} /></div><div className="brand"><strong>DT-CyberTwin</strong><span>Cyber-physical simulation console</span></div><div className="topbar-right"><span className="environment"><span className="status-dot" /> SIMULATION ENVIRONMENT</span><span className="api-address">API {API}</span></div></header>
    <section className="page-heading"><div><div className="eyebrow">REFERENCE SCENARIO / INDUSTRIAL TEMPERATURE CONTROL</div><h1>Cyber-physical operations</h1><p>Explore how a cyber attack on sensor telemetry can influence a simulated industrial temperature-control loop.</p><div className="heading-context"><span><strong>01</strong> Configure a scenario</span><span><strong>02</strong> Run the simulation</span><span><strong>03</strong> Compare telemetry and impact</span></div></div><button className="button secondary" onClick={() => { setResult(null); setError(''); void loadGraph() }}><RefreshCw size={15} /> Reset view</button></section>
    {error && <div className="error-banner"><AlertTriangle size={17} /><span>{error}</span><button onClick={() => setError('')} aria-label="Dismiss error">×</button></div>}
    <section className="metric-grid">
      <article className="metric-card"><div className="metric-label"><Thermometer size={16} /> PEAK TEMPERATURE</div><div className="metric-value">{formatNumber(result?.metrics.peak_temperature)}<small>°</small></div><div className="metric-note">Configured safety limit: {result?.metrics.safe_max ?? safeMax}°</div></article>
      <article className="metric-card"><div className="metric-label"><ShieldAlert size={16} /> SAFETY STATUS</div><div className={`metric-value status-value ${result ? (result.metrics.safe ? 'safe-text' : 'unsafe-text') : ''}`}>{result ? (result.metrics.safe ? 'Within limits' : 'Limit exceeded') : 'Not run'}</div><div className="metric-note">Based on {result?.metrics.safe_min ?? 0}°–{result?.metrics.safe_max ?? safeMax}° safety range</div></article>
      <article className="metric-card"><div className="metric-label"><AlertTriangle size={16} /> IMPACT SCORE</div><div className="metric-value">{result ? formatNumber(result.metrics.impact_score) : '—'}<small>/100</small></div><div className="metric-note">Model-defined out-of-range score</div></article>
      <article className="metric-card"><div className="metric-label"><GitBranch size={16} /> COMPROMISED ASSETS</div><div className="metric-value">{result ? stateCounts.compromised : '—'}<small>/{stateCounts.assets}</small></div><div className="metric-note">Assets flagged in final state</div></article>
    </section>

    <div className="main-grid">
      <section className={`panel topology-panel ${topologyExpanded ? 'topology-expanded' : ''}`}><div className="panel-heading"><div><h2>Digital twin topology</h2><p>Follow the path from operator and network assets to the physical process</p></div><span className="legend-item"><span className="legend-line" /> Connection</span><span className="legend-item"><span className="legend-line danger-line" /> Compromised path</span><button className="topology-expand-button" onClick={() => setTopologyExpanded(v => !v)} aria-label={topologyExpanded ? "Exit full-screen topology" : "Expand topology full screen"} title={topologyExpanded ? "Exit full screen (Esc)" : "Expand topology full screen"}>{topologyExpanded ? <><Minimize2 size={16} /><span>Exit full screen</span><X size={15} /></> : <><Maximize2 size={16} /><span>Expand</span></>}</button></div><Topology graph={graph} result={result} /></section>
      <section className="panel controls-panel"><div className="panel-heading"><div><h2>Scenario controls</h2><p>Configure and execute a simulation</p></div><span className="live-tag">DETERMINISTIC</span></div>
        <div className="scenario-intro"><strong>Choose what to test</strong><p><b>Baseline</b> runs without an attack. <b>Sensor spoofing</b> falsifies the sensor reading to test whether the controller reacts safely.</p></div><div className="scenario-toggle"><button className={!attack ? 'selected' : ''} onClick={() => setAttack(false)}>Baseline</button><button className={attack ? 'selected attack-selected' : ''} onClick={() => setAttack(true)}>Sensor spoofing</button></div>
        <label className="field-label">Simulation timesteps <strong>{steps}</strong><input type="range" min="3" max="60" value={steps} onChange={e => { const next = Number(e.target.value); setSteps(next); if (attackTimestep >= next) setAttackTimestep(next - 1) }} /></label>
        <label className="field-label">Initial temperature <strong>{initialTemperature}°</strong><input type="range" min="10" max="60" value={initialTemperature} onChange={e => setInitialTemperature(Number(e.target.value))} /></label>
        <label className="field-label">Controller setpoint <strong>{setpoint}°</strong><input type="range" min="20" max="60" value={setpoint} onChange={e => setSetpoint(Number(e.target.value))} /></label>
        <label className="field-label">Safety upper limit <strong>{safeMax}°</strong><input type="range" min="45" max="100" value={safeMax} onChange={e => setSafeMax(Number(e.target.value))} /></label>
        {attack && <><label className="field-label">Attack timestep <strong>{attackTimestep}</strong><input type="range" min="0" max={Math.max(0, steps - 1)} value={attackTimestep} onChange={e => setAttackTimestep(Number(e.target.value))} /></label><label className="field-label">Spoof offset <strong>{spoofOffset}°</strong><input type="range" min="-50" max="-5" value={spoofOffset} onChange={e => setSpoofOffset(Number(e.target.value))} /></label><div className="notice"><AlertTriangle size={15} /><span>Simulated false-low telemetry can keep the heater active even when the physical temperature is high.</span></div></>}
        <button className="button primary run-button" disabled={loading} onClick={() => void runSimulation()}>{loading ? <RefreshCw size={16} className="spin" /> : <Play size={16} fill="currentColor" />}{loading ? 'Running simulation…' : 'Run simulation'}</button>
        <button className="button secondary compare-button" disabled={loading} onClick={() => void runSimulation(!attack)}><Activity size={16} /> Run {attack ? 'baseline' : 'attack'} comparison</button>
      </section>
    </div>

    <section className="panel chart-panel"><div className="panel-heading"><div><h2>Temperature telemetry</h2><p>Compare physical temperature with what the sensor measures and reports to the controller</p></div>{result && <span className={`result-chip ${result.metrics.safe ? 'chip-safe' : 'chip-danger'}`}>{result.metrics.safe ? <CheckCircle2 size={14} /> : <AlertTriangle size={14} />}{result.metrics.safe ? 'Within safety limits' : 'Safety limit exceeded'}</span>}</div>
      {result ? <div className="chart-wrap"><ResponsiveContainer width="100%" height="100%"><LineChart data={chartData} margin={{ top: 12, right: 18, left: 2, bottom: 4 }}><CartesianGrid stroke="#253047" strokeDasharray="3 3" /><XAxis dataKey="timestep" tick={{ fill: '#8e9bb1', fontSize: 11 }} axisLine={{ stroke: '#344056' }} tickLine={false} label={{ value: 'Timestep', position: 'insideBottom', offset: -2, fill: '#8e9bb1', fontSize: 11 }} /><YAxis tick={{ fill: '#8e9bb1', fontSize: 11 }} axisLine={false} tickLine={false} domain={['auto', 'auto']} /><Tooltip contentStyle={{ background: '#101827', border: '1px solid #334155', borderRadius: 8, color: '#e5edf8' }} /><Legend /><Line type="monotone" dataKey="actual_temperature" name="Actual after step" stroke="#60a5fa" strokeWidth={2.5} dot={false} /><Line type="monotone" dataKey="measured_temperature" name="Measured at step start" stroke="#34d399" strokeWidth={1.8} dot={false} /><Line type="monotone" dataKey="reported_temperature" name="Reported by sensor" stroke="#fbbf24" strokeWidth={1.8} dot={false} /><Line type="monotone" dataKey={() => result.metrics.safe_max} name="Safety limit" stroke="#fb7185" strokeDasharray="6 4" dot={false} /></LineChart></ResponsiveContainer></div> : <div className="empty-state"><Activity size={28} /><strong>No simulation results yet</strong><span>Choose a scenario and run it to populate telemetry and impact data.</span></div>}
      {result && <div className="chart-foot"><span className="chart-key"><i className="key-blue" /> Actual after step = physical process state</span><span className="chart-key"><i className="key-green" /> Measured = sensor input</span><span className="chart-key"><i className="key-amber" /> Reported = value sent onward</span><span>Setpoint: <strong>{result.metrics.setpoint}°</strong></span><span>Max deviation from setpoint: <strong>{formatNumber(result.metrics.maximum_setpoint_deviation)}°</strong></span><span>Out-of-range steps: <strong>{result.metrics.overheat_steps}</strong></span></div>}
    </section>

    <div className="bottom-grid"><section className="panel"><div className="panel-heading"><div><h2>Impact findings</h2><p>Physical consequences detected by the model</p></div><span className="count-pill">{result?.impacts.length ?? 0}</span></div>{result && result.impacts.length ? <div className="list-scroll">{result.impacts.map((impact, i) => <ImpactRow key={`${impact.timestep}-${i}`} impact={impact} />)}</div> : <div className="compact-empty"><CheckCircle2 size={17} /><span>{result ? 'No safety-limit breaches detected in this run.' : 'Run a simulation to inspect impact findings.'}</span></div>}</section>
      <section className="panel"><div className="panel-heading"><div><h2>Event timeline</h2><p>Ordered simulation and attack events</p></div><span className="count-pill">{result?.timeline.length ?? 0}</span></div>{result ? <div className="list-scroll event-list">{result.timeline.slice().reverse().map((event, i) => <EventRow key={`${event.timestep}-${event.action}-${i}`} event={event} />)}</div> : <div className="compact-empty"><CircleHelp size={17} /><span>Events will appear here after a simulation.</span></div>}</section></div>
    <section className="explain-panel"><div className="explain-heading"><CircleHelp size={19} /><div><h2>How to interpret this dashboard</h2><p>The twin is a deterministic software simulation, not a live industrial system.</p></div></div><div className="explain-grid"><article><strong>Topology</strong><p>Each card is a simulated asset. Red outlines and links identify assets marked compromised in the final state.</p></article><article><strong>Safety status</strong><p>“Within limits” means the simulated physical temperature stayed inside the configured safety range; it does not mean the system is secure.</p></article><article><strong>Impact score</strong><p>A model-derived indicator of out-of-range behaviour. Interpret it alongside peak temperature, out-of-range steps, and the event timeline.</p></article><article><strong>Sensor spoofing</strong><p>The offset changes the sensor value reported to the controller. Compare it with actual temperature to see whether telemetry diverges from physical state.</p></article></div></section><footer><span>DT-CyberTwin · Research prototype</span><span><strong>Simulation only.</strong> Not connected to real industrial equipment.</span></footer>
  </main>
}
