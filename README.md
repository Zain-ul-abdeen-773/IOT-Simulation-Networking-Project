> We didn't build a simulation. We built a nervous system.

The traditional approach to IoT network simulation is fundamentally flawed. It relies on static models, synthetic data, and disconnected analytics. 

This project shatters that paradigm. We engineered a high-performance, intelligent network topography that doesn't just route packets—it thinks, predicts, and defends itself in real-time. This is a brutalist, zero-latency environment where advanced machine learning is fused directly into the bare-metal simulation loop.

### the forge.

Most systems bridge AI and simulation via bloated REST APIs or slow Python interconnects. We rejected that. Inference latency had to be zero. 

We trained our deep learning models offline—Random Forest Regressors for latency prediction, OneClassSVMs for anomaly detection—and used mathematical transpilation (`m2cgen`) to compile the decision trees directly into native Java bytecode. The result? Microsecond inference running natively inside the AnyLogic Discrete Event engine. 

But predictive analytics wasn't enough. We needed autonomous intervention. 
We integrated a bare-metal **Tabular Q-Learning Agent** directly into the packet sink. It continuously monitors queue states, calculates reward penalties based on latency spikes, and dynamically throttles traffic loads. 

To break the UI bottleneck, we dismantled the monolithic reporting interface. The telemetry is now handled by a decoupled, four-monitor Java Swing NOC (Network Operations Center) running on independent thread pools.
1. **Latency & Forecasting Hub:** Real-time t+10 auto-regressive prediction.
2. **Security & Anomaly Radar:** Visualizing the OneClassSVM defense against injected GAN-based DDoS attacks.
3. **Telemetry & Error Matrix:** Absolute ground-truth of system health.
4. **Energy Dynamics & Digital Twin:** Tracking synthetic battery depletion and calculating a composite virtual node health score.

Finally, we decentralized the intelligence. Rather than pooling sensitive IoT data, we built a modular **Federated Learning** architecture (Edge-to-Cloud `FedAvg`) where nodes train models locally and mathematically aggregate weights globally.

### the arsenal.

**The Simulation Engine**
- `AnyLogic Framework` — Multi-agent discrete event orchestration.
- `Native Java 8+` — The bare-metal execution layer.
- `Java Swing / Java2D` — Hardware-accelerated, decoupled dashboard threading.

**The Intelligence Core**
- `Scikit-Learn` & `NumPy` — Offline model generation.
- `m2cgen` — Abstract Syntax Tree transpilation to Java.
- `Tabular Q-Learning` — Native reinforcement learning for dynamic load balancing.
- `GAN Injector` — Synthetic adversarial traffic generation.

**The Edge Infrastructure**
- `Federated Averaging (FedAvg)` — Distributed, privacy-preserving training pipeline.
- `React & Vite` — The external web analytics interface.

### initiation.

Clone the repository. Open `FinalCCNProject.alp` in AnyLogic. 
Press `F7` to compile the bytecode. Hit Run. 
If you want to see the decentralized training:

```bash
# Ignite the local web dashboard
cd dashboard && npm run dev

# Execute the Federated Learning node simulation
cd federated && python plot_federated.py
```