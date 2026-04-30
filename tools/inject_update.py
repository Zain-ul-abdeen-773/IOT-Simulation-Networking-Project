import re

def inject():
    with open('FinalCCNProject.alp', 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the line: metrics.recordLatency( agent.flow_duration );
    target = 'metrics.recordLatency( agent.flow_duration );'
    
    # We want to add dataset updates
    replacement = target + """
    latencyDataset.add(agent.flow_duration);
    try {
        aiLatencyDataset.add(aiPredictor.predict(new double[]{agent.packet_size, 0, 0, 0}));
    } catch (Exception e) {}
"""
    
    new_content = content.replace(target, replacement)
    
    with open('FinalCCNProject.alp', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Injected dataset updates!")

if __name__ == '__main__':
    inject()
