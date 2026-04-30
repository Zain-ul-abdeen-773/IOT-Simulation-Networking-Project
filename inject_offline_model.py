import re

def inject_offline_model():
    with open('model/OfflineAiPredictor.java', 'r', encoding='utf-8') as f:
        offline_model_code = f.read()

    with open('FinalCCNProject.alp', 'r', encoding='utf-8') as f:
        content = f.read()

    main_start = content.find('<Name><![CDATA[Main]]></Name>')
    if main_start == -1:
        print("Main agent not found")
        return

    # Add the OfflineAiPredictor class to AdditionalClassCode
    # We will find </AdditionalClassCode> and inject right before it
    if '</AdditionalClassCode>' in content:
        content = content.replace('</AdditionalClassCode>', offline_model_code + '\n]]></AdditionalClassCode>')
    else:
        print("Could not find AdditionalClassCode")
        return

    # Update the packet hook to use OfflineAiPredictor.score
    target_hook = """    if (dashboard != null) {
        try {
            double[] features = new double[]{agent.packet_size, 0, 0, 0};
            
            // 1. Train AI Predictor online!
            if (aiPredictor != null) {
                aiPredictor.addTrainingSample(features, agent.flow_duration);
            }
            
            // 2. Make Prediction
            double pred = 0.0;
            if (aiPredictor != null) {
                pred = aiPredictor.predict(features);
            }
            
            // 3. Update Multi-Graph Dashboard
            dashboard.addData(agent.flow_duration, pred, agent.packet_size);
        } catch (Throwable e) { 
            dashboard.logError(e.toString()); 
        }
    }"""
    
    new_hook = """    if (dashboard != null) {
        try {
            // 1. Prepare features for Pre-Trained Random Forest Model
            double[] rfFeatures = new double[]{agent.packet_size, agent.inter_arrival};
            
            // 2. Score offline Random Forest model natively in Java!
            double pred = OfflineAiPredictor.score(rfFeatures);
            
            // 3. Update Multi-Graph Dashboard
            dashboard.addData(agent.flow_duration, pred, agent.packet_size);
        } catch (Throwable e) { 
            dashboard.logError("RF Error: " + e.toString()); 
        }
    }"""
    
    content = content.replace(target_hook, new_hook)

    with open('FinalCCNProject.alp', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Successfully injected 1.3 MB Random Forest model into AnyLogic!")

if __name__ == '__main__':
    inject_offline_model()
