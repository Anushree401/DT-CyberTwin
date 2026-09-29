# DT-CyberTwin

> **What happens to the system after a successful attack?**

Most security validation platforms answer whether an attacker **can** compromise a system.

DT-CyberTwin asks what happens **after they do**.

It is a stateful **Cyber-Physical Digital Twin** that models how an attack evolves through interconnected systems, how system state changes over time, and how a cyber compromise can propagate into operational and physical consequences.

```mermaid
flowchart LR
    A[Cyber Attack] --> B[Compromise]
    B --> C[State Change]
    C --> D[Propagation]
    D --> E[Control System Impact]
    E --> F[Physical Consequence]
    F --> G[Operational Impact]
    G --> H[Recovery / What-if]
```

---

## The Gap

Traditional security validation can establish:

```mermaid
flowchart LR
    A[Attacker] --> B[Initial Access]
    B --> C[Lateral Movement]
    C --> D[Compromise]
    D --> E[Exposure Validated]
```

But the system does not stop when the attack path is validated.

DT-CyberTwin continues the simulation:

```mermaid
flowchart LR
    A[Attacker] --> B[Initial Access]
    B --> C[Lateral Movement]
    C --> D[Controller Compromise]
    D --> E[Signal Corruption]
    E --> F[Incorrect Control]
    F --> G[Actuator Response]
    G --> H[Physical Consequence]
    H --> I[Operational Impact]
```

The focus shifts from:

> **Can the attack happen?**

to:

> **How will the system evolve if it happens?**

---

## What is DT-CyberTwin?

DT-CyberTwin maintains a continuously evolving digital representation of a cyber-physical environment.

It combines:

* **Stateful Digital Twin** — represents devices, services, controllers, sensors, actuators, and their current states.
* **Attack Simulation** — models attacks as evolving events rather than isolated vulnerabilities.
* **Dependency Graph** — captures relationships and propagation paths between components.
* **CPS Modeling** — connects cyber events to sensor, controller, actuator, and physical-system behavior.
* **Impact Propagation** — models cascading degradation across the system.
* **Causal Replay** — reconstructs how and why the system reached a particular state.
* **Adaptive Intelligence** — enables attacker, defender, and environment behavior to evolve with system state.

```mermaid
flowchart TB
    A[System Model] --> B[Digital Twin]
    B --> C[State Engine]
    C --> D[Simulation Engine]

    D --> E[Attacker]
    D --> F[Defender]
    D --> G[Environment]

    E --> D
    F --> D
    G --> D

    D --> H[Impact Propagation]
    H --> I[CPS Model]
    I --> J[Operational & Physical Consequences]

    D --> K[Causal Replay]
    K --> L[Counterfactual Analysis]
```

---

## A System That Evolves

The core of DT-CyberTwin is a **time-evolving system state**.

```mermaid
sequenceDiagram
    participant A as Attacker
    participant T as Digital Twin
    participant C as Controller
    participant P as Physical System

    A->>T: Compromise component
    T->>T: Update system state
    T->>C: Propagate cyber impact
    C->>P: Incorrect control decision
    P->>T: Physical state changes
    T->>T: Recalculate system state
    T->>A: Updated environment
```

At every simulation step:

```text
state(t+1) = f(
    state(t),
    agent actions,
    system conditions
)
```

This allows DT-CyberTwin to model not only **where an attacker can go**, but **what the system becomes as a consequence**.

---

## Example

Consider a simple industrial temperature-control system:

```mermaid
flowchart LR
    S[Temperature Sensor] --> C[Controller / PLC]
    C --> A[Actuator]
    A --> P[Physical Process]
    P --> S

    N[Network] -. Cyber Attack .-> S
    N -. Cyber Attack .-> C
```

Under normal conditions:

```text
Sensor → Controller → Actuator → Physical Process
                    ↑
                 Feedback
```

Now suppose the sensor telemetry is manipulated.

```mermaid
flowchart LR
    A[True Temperature] --> B[Sensor]
    B --> C[Manipulated Telemetry]
    C --> D[Controller]
    D --> E[Incorrect Actuation]
    E --> F[Physical Deviation]
```

DT-CyberTwin follows the entire chain:

**Cyber event → state transition → control response → physical consequence → operational impact**

---

## Architecture

```mermaid
flowchart TB
    subgraph Input["System Definition"]
        A[Topology]
        B[Component States]
        C[Vulnerabilities]
        D[System Conditions]
    end

    subgraph Twin["DT-CyberTwin Core"]
        E[Digital Twin]
        F[State Engine]
        G[Dependency Graph]
        H[Simulation Engine]
    end

    subgraph Intelligence["Adaptive Intelligence"]
        I[Attacker Agent]
        J[Defender Agent]
        K[Environment Agent]
    end

    subgraph CPS["Cyber-Physical Layer"]
        L[Sensor]
        M[Controller]
        N[Actuator]
        O[Physical Process]
    end

    subgraph Analysis["Analysis"]
        P[Impact Propagation]
        Q[Causal Replay]
        R[Counterfactual Analysis]
    end

    Input --> E
    E --> F
    E --> G
    F --> H
    G --> H

    I --> H
    J --> H
    K --> H
    H --> I
    H --> J
    H --> K

    H --> L
    L --> M
    M --> N
    N --> O
    O --> L

    H --> P
    P --> Q
    Q --> R
```

---

## What We Measure

DT-CyberTwin moves beyond a simple exposure result.

The simulation can track:

| Layer       | Example State                              |
| ----------- | ------------------------------------------ |
| Cyber       | compromise, privilege, connectivity        |
| Network     | latency, packet loss, availability         |
| System      | service degradation, dependency failures   |
| Control     | sensor deviation, controller instability   |
| Physical    | temperature, pressure, process deviation   |
| Operational | downtime, degraded functionality, recovery |

---

## The Core Idea

```mermaid
flowchart LR
    A["Attack Simulation"] --> B["+ Stateful Digital Twin"]
    B --> C["+ Dependency Graph"]
    C --> D["+ CPS Model"]
    D --> E["+ Impact Propagation"]
    E --> F["System Consequences"]
```

**DT-CyberTwin is not just asking whether a system can be breached.**

It asks:

> **Once the breach occurs, how does the system evolve?**

---

## Project Status

DT-CyberTwin is being developed as a research and competition prototype for **Digital Twins and Cyber-Physical Systems**, with the initial implementation focused on synthetic CPS environments and state-based simulation.

The initial development path is:

```mermaid
flowchart LR
    A[Digital Twin Core] --> B[State Evolution]
    B --> C[Attack Simulation]
    C --> D[CPS Model]
    D --> E[Impact Propagation]
    E --> F[Causal Replay]
    F --> G[Adaptive Agents]
    G --> H[Counterfactual Analysis]
```

---

## Vision

Security validation should not end at **"compromised."**

DT-CyberTwin aims to bridge the gap between:

**attack validation**

and

**system-level consequence understanding.**

> **Simulate the attack.
> Evolve the system.
> Understand the consequence.**
