import re
import os

with open('train_latency_voting_regressor.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('"packet_size"', '"packetSize"')
content = content.replace('"inter_arrival_time"', '"interArrival"')

content = content.replace('from sklearn.ensemble import AdaBoostRegressor, VotingRegressor', 'from sklearn.ensemble import RandomForestRegressor')
content = content.replace('from sklearn.linear_model import LinearRegression\n', '')
content = content.replace('from sklearn.pipeline import make_pipeline\n', '')
content = content.replace('from sklearn.preprocessing import StandardScaler\n', '')
content = content.replace('from sklearn.svm import SVR\n', '')
content = content.replace('from sklearn.tree import DecisionTreeRegressor\n', '')

# Remove entire build_adaboost_model block
content = re.sub(r'def build_adaboost_model.*?return AdaBoostRegressor.*?random_state,\n        \)\n', '', content, flags=re.DOTALL)

voting_logic_regex = r'print\("\[5/7\] Initializing base models\.\.\."\).*?voting_regressor\.fit\(X_train, y_train\)'
new_logic = """print("[5/7] Initializing Random Forest Ensemble...")
    voting_regressor = RandomForestRegressor(n_estimators=50, max_depth=10, random_state=RANDOM_STATE)
    voting_regressor.fit(X_train, y_train)"""
content = re.sub(voting_logic_regex, new_logic, content, flags=re.DOTALL)

content = content.replace('import joblib', 'import joblib\nimport m2cgen as m2c')

export_logic = """joblib.dump(voting_regressor, output_path)
    print(f"Saved trained model to: {output_path}")

    print("[8/7] Exporting model to pure Java using m2cgen...")
    java_code = m2c.export_to_java(voting_regressor, class_name="OfflineAiPredictor")
    with open("OfflineAiPredictor.java", "w", encoding="utf-8") as java_file:
        java_file.write(java_code)
    print("Exported Java model to OfflineAiPredictor.java")
"""
content = content.replace('joblib.dump(voting_regressor, output_path)\n    print(f"Saved trained Voting Regressor to: {output_path}")', export_logic)

with open('train_latency_random_forest.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Created train_latency_random_forest.py")
