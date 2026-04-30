#!/usr/bin/env python3
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
import m2cgen as m2c

def main():
    print("[1/4] Loading data for Forecasting...")
    df = pd.read_csv('clean_mqtt_traffic.csv')
    
    # We want to predict latency 10 packets into the future using the past 3 latencies
    latencies = df['flowDuration'].values
    
    X = []
    y = []
    
    # sliding window of 3 elements predicting element at i+10
    for i in range(len(latencies) - 13):
        window = latencies[i:i+3]
        target = latencies[i+13]
        X.append(window)
        y.append(target)
        
    X = np.array(X)
    y = np.array(y)
    
    print(f"Generated {len(X)} sliding windows.")
    
    print("[2/4] Training Autoregressive Random Forest...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    rf = RandomForestRegressor(n_estimators=10, max_depth=10, random_state=42)
    rf.fit(X_train, y_train)
    
    y_pred = rf.predict(X_test)
    print(f"Forecasting MAE (10 steps ahead): {mean_absolute_error(y_test, y_pred):.6f}")
    
    print("[3/4] Exporting FutureForecaster to Java...")
    rf_java = m2c.export_to_java(rf, class_name="FutureForecaster")
    with open("FutureForecaster.java", "w", encoding="utf-8") as f:
        f.write("package finalccnproject;\n\n" + rf_java)
        
    print("[4/4] Done!")

if __name__ == '__main__':
    main()
