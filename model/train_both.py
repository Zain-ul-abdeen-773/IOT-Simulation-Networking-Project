#!/usr/bin/env python3
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import OneClassSVM
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
import m2cgen as m2c

def main():
    print("[1/5] Loading data...")
    df = pd.read_csv('clean_mqtt_traffic.csv')
    
    X_lat = df[["packetSize", "interArrival"]].copy()
    y_lat = df["flowDuration"].copy()
    
    # We will use packetSize, interArrival, and flowDuration for Anomaly Detection
    X_anom = df[["packetSize", "interArrival", "flowDuration"]].copy()
    
    print("[2/5] Training Latency Predictor...")
    X_train, X_test, y_train, y_test = train_test_split(X_lat, y_lat, test_size=0.2, random_state=42)
    rf = RandomForestRegressor(n_estimators=10, max_depth=10, random_state=42)
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)
    print(f"Latency MAE: {mean_absolute_error(y_test, y_pred):.6f}")
    
    print("[3/5] Training Anomaly Detector...")
    ocsvm = OneClassSVM(nu=0.05) # 5% anomaly expectation
    ocsvm.fit(X_anom)
    print("OneClassSVM trained.")
    
    print("[4/5] Exporting Latency Predictor to Java...")
    rf_java = m2c.export_to_java(rf, class_name="OfflineAiPredictor")
    with open("OfflineAiPredictor.java", "w", encoding="utf-8") as f:
        f.write("package finalccnproject;\n\n" + rf_java)
        
    print("[5/5] Exporting Anomaly Detector to Java...")
    ocsvm_java = m2c.export_to_java(ocsvm, class_name="AnomalyModel")
    with open("AnomalyModel.java", "w", encoding="utf-8") as f:
        f.write("package finalccnproject;\n\n" + ocsvm_java)
        
    print("Done!")

if __name__ == '__main__':
    main()
