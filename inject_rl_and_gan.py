import time
import re

def inject_rl_and_gan():
    with open('FinalCCNProject.alp', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Inject QTableBalancer
    with open('QTableBalancer.java', 'r', encoding='utf-8') as f:
        java_code = f.read().replace('package finalccnproject;\n', '')
    
    unique_id = str(int(time.time() * 1000) + 4)
    java_class_xml = f"""		<JavaClass>
			<Id>{unique_id}</Id>
			<Name><![CDATA[QTableBalancer]]></Name>
			<Text><![CDATA[{java_code.strip()}]]></Text>
		</JavaClass>
"""
    content = re.sub(r'<JavaClass>\s*<Id>\d+</Id>\s*<Name><!\[CDATA\[QTableBalancer\]\]></Name>.*?</JavaClass>', '', content, flags=re.DOTALL)
    content = content.replace('</JavaClasses>', java_class_xml + '\t</JavaClasses>')

    # 2. Inject GAN & RL Hook
    target_hook = r"""// 1\. Prepare features for AI Pipeline.*?dashboard\.addData\(agent\.flow_duration, pred, agent\.packet_size, anomalyScore\);"""
    
    new_hook = """// 0. GAN DDoS Simulation (5% chance to inject synthetic malicious data)
            if (Math.random() < 0.05) {
                agent.packet_size = 15000 + Math.random() * 5000;
                agent.inter_arrival = Math.random() * 5;
                agent.flow_duration = 150.0 + Math.random() * 50;
            }

            // 0.5 RL Load Balancer (Tabular Q-Learning)
            int simulatedQueue = (int)(agent.inter_arrival % 120); // proxy for queue
            String state = QTableBalancer.getState(simulatedQueue);
            double actionDelay = QTableBalancer.chooseAction(state);
            agent.flow_duration = agent.flow_duration * actionDelay; // Apply RL action!
            double reward = -agent.flow_duration; // Penalty for high latency
            QTableBalancer.update(state, actionDelay, reward, QTableBalancer.getState(simulatedQueue + 1));

            // 1. Prepare features for AI Pipeline
            double[] rfFeatures = new double[]{agent.packet_size, agent.inter_arrival};
            double[] anomalyFeatures = new double[]{agent.packet_size, agent.inter_arrival, agent.flow_duration};
            
            // 2. Score offline models natively in Java!
            double pred = OfflineAiPredictor.score(rfFeatures);
            double anomalyScore = AnomalyModel.score(anomalyFeatures);
            
            // 3. Score Time-Series Forecaster
            if (dashboard.actualLatencies.size() >= 3) {
                int s = dashboard.actualLatencies.size();
                double[] window = new double[]{
                    dashboard.actualLatencies.get(s-3),
                    dashboard.actualLatencies.get(s-2),
                    dashboard.actualLatencies.get(s-1)
                };
                double futureLatency = FutureForecaster.score(window);
                dashboard.addForecast(futureLatency);
            }
            
            // 4. Update Premium Multi-Graph Dashboard
            dashboard.addData(agent.flow_duration, pred, agent.packet_size, anomalyScore);"""
            
    content = re.sub(target_hook, new_hook, content, flags=re.DOTALL)

    with open('FinalCCNProject.alp', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Successfully injected RL Load Balancer and GAN DDoS Simulator!")

if __name__ == '__main__':
    inject_rl_and_gan()
