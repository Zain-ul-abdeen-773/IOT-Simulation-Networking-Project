# Aegis-IoT: Neural Network Intelligence Platform

> // [SYSTEM_STATUS]: ACTIVE
> // [OBJECTIVE]: AUTONOMOUS_IOT_ORCHESTRATION_AND_THREAT_NEUTRALIZATION
> // [DIRECTIVE]: ELIMINATE_LATENCY_THROUGH_NATIVE_BYTECODE_INFERENCE

The traditional approach to IoT network modeling is fundamentally broken. It relies on static heuristics, synthetic data, and disconnected analytics bridged by bloated, high-latency REST APIs. **Aegis-IoT** obliterates this paradigm. This platform is a high-performance, intelligent topography designed to predict, react, and defend itself in real-time. By fusing native Java execution with transpiled machine learning kernels, we have created a self-healing, predictive network that identifies threats and optimizes loads in microseconds. This is not a simulation; it is a brutalist engineering environment where intelligence is treated as a bare-metal primitive.

## II. The Architecture Blueprint (Expanded)

The system architecture is designed for zero-latency inference and decoupled visualization. We rejected bloated inter-process communication in favor of a bare-metal execution loop within the Java Virtual Machine.

```mermaid
graph TD
    subgraph "Data Acquisition Layer"
        S[Sensor Device Array] -->|MQTTPacket| G[Gateway Node]
        G -->|NetworkMetrics| SINK[Cloud Processing Sink]
    end

    subgraph "The Intelligence Core (AnyLogic JVM)"
        SINK -->|Packet State| RF[Random Forest Predictor]
        SINK -->|Feature Vector| SVM[OneClassSVM Radar]
        SINK -->|Temporal Window| TS[Forecasting Engine]
        SINK -->|State/Reward| RL[Q-Table Load Balancer]
        
        RL -->|Throttling Multiplier| G
        RF -->|Inference Score| SINK
        SVM -->|Anomaly Flag| SINK
    end

    subgraph "The Watchtower (NOC Dashboard)"
        SINK --> D1[Latency Hub]
        SINK --> D2[Security Radar]
        SINK --> D3[Telemetry Matrix]
        SINK --> D4[Energy/Digital Twin]
    end

    subgraph "Distributed Learning Hub"
        EDGE[Federated Edge Nodes] -->|Local Weights| AGG[Cloud Aggregator]
        AGG -->|Global Weights| RF
    end

    SINK -.->|JSON Stream| WD[React/Vite Web Dashboard]
```

### // The Simulation Layer :: AnyLogic Agent-Based Topology
The core engine utilizes an agent-based discrete-event model to simulate heterogeneous IoT environments. `SensorDevice` agents generate `MQTTPacket` payloads, which carry complex `NetworkMetrics` structs (packet size, inter-arrival time, flow duration). These packets traverse the `Gateway` agents, where the first level of traffic policing occurs. The routing logic is not static; it is influenced by the **Mutation Engine**, which injects dynamic Java code into the agent's behavior at runtime to facilitate real-time decision-making based on AI inference scores.

### // The Machine Learning Pipeline :: M2CGen Architecture
Latency is the enemy of intelligence. To achieve microsecond-scale inference, we eliminated the "Python Gap." We train high-dimensional models—**Voting Regressors** for predictive latency and **OneClassSVMs** for DDoS anomaly detection—in scikit-learn. Using the `m2cgen` (Model 2 Code Generator) framework, we transpile the models' Abstract Syntax Trees (AST) directly into pure, zero-dependency Java classes (`OfflineAiPredictor.java`). This allows the AnyLogic JVM to execute complex decision trees as native method calls, bypassing the overhead of JNI or socket-based communication.

## III. Federated & Reinforcement Mechanics

### // The QTableBalancer :: Reinforcement State-Space
Congestion management is handled by a custom **Tabular Q-Learning Agent** implemented in native Java (`QTableBalancer.java`). The agent operates in a multi-dimensional state-space comprising current queue depth and packet arrival rates.
- **State Space:** Discrete buckets of network load and congestion levels.
- **Action Space:** Dynamic throttling multipliers applied to packet flow durations.
- **Reward Function:** A high-penalty function that punishes buffer overflows and latency spikes while rewarding high throughput.
The agent continuously mutates its internal Q-Table, converging on an optimal traffic management policy without manual heuristic tuning.

### // The Federated Edge :: Weight Distribution & Aggregation
To fulfill the requirement for decentralized intelligence, we implemented a modular **Federated Learning** suite (`/federated`).
- **Edge Nodes:** Python-based agents simulate localized IoT sensor arrays. They load local traffic partitions and train **SGD Regressors** locally.
- **Privacy Preservation:** Raw packet data never leaves the edge node. Only the model's coefficients and intercept (weights) are transmitted.
- **Cloud Aggregation:** The `cloud_server.py` implements the **FedAvg** (Federated Averaging) algorithm, mathematically aggregating weights from `n` edge nodes to produce a global model. This global state is then periodically injected back into the AnyLogic inference core to update the predictive baseline.

## IV. The Injection Engine (The Flex)

The true engineering mastery of **Aegis-IoT** lies in its **Mutation Engine** (`/injection_scripts`). We developed a suite of Python scripts that utilize regex-based XML parsing to perform surgical operations on the AnyLogic `.alp` file.
- **Code Injection:** Scripts like `inject_multi_dashboard.py` and `inject_rl_and_gan.py` scan the XML for specific metadata markers (e.g., `<AdditionalClassCode>`, `<StartupCode>`) and inject entire Java Swing classes and logic hooks directly into the simulation source.
- **UI Mutation:** The engine dynamically positions and initializes four independent, hardware-accelerated dashboard windows (`LatencyDash`, `SecurityDash`, `TelemetryDash`, `EnergyDash`) by patching the simulation's startup sequence.
This allows for the rapid deployment of complex AI and UI features without the need for manual GUI interaction in the AnyLogic IDE.

## V. Telemetry & Visualization

Observability is handled by a dual-stack visualization system designed for absolute monitoring.
1. **The Native NOC:** Four independent Java Swing windows provide real-time, high-refresh-rate monitoring of the SVM anomaly radar, the autoregressive t+10 forecaster, and the Digital Twin health score.
2. **The Web Interface:** A modern **React/Vite** dashboard (`/dashboard`) consumes the `mqtt_ready` JSON data stream. It utilizes `recharts` for high-fidelity visualization of packet size distributions and `framer-motion` for a responsive, high-aura UI. The frontend maps the physical network topography to a virtual mirror, providing a complete Digital Twin of the IoT environment.

## VI. The Arsenal (Tech Stack Matrix)

> **Simulation Engine:** AnyLogic // Native Java // Discrete Event Logic
> **Neural & Predictive:** Scikit-Learn // M2CGen // Federated SGD // Q-Learning
> **Mutation & Injection:** Python 3.x // XML Regex Patching // AST Manipulation
> **Telemetry:** React // Vite // Tailwind CSS // Recharts // Java2D

## VII. Ignition Protocol

[SYS] :: START_DEPLOYMENT_SEQUENCE

**1. Machine Learning Synthesis**
```powershell
cd model
python train_latency_random_forest.py
python test_m2cgen4.py
```

**2. Simulation Mutation**
```powershell
cd injection_scripts
python inject_multi_dashboard.py
python inject_rl_and_gan.py
```

**3. Frontend & Federated Activation**
```powershell
# Launch Analytics Hub
cd dashboard
npm install; npm run dev

# Launch Federated Learning rounds
cd federated
python plot_federated.py
```

***
// [SYSTEM_LOG]: ARCHITECTURE_DEPLOYED_SUCCESSFULLY
// [SYSTEM_LOG]: READY_FOR_SIMULATION_RUN
***
