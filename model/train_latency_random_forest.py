#!/usr/bin/env python3
"""Train a Random Forest Regressor for IoT network latency prediction and export to Java."""

from pathlib import Path
import joblib
import m2cgen as m2c
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

INPUT_CSV = "clean_mqtt_traffic.csv"
MODEL_OUTPUT = "latency_predictor.pkl"
RANDOM_STATE = 42
TEST_SIZE = 0.2

def main() -> None:
    print("[1/7] Loading dataset...")
    input_path = Path.cwd() / INPUT_CSV
    df = pd.read_csv(input_path)
    
    print("[2/7] Extracting feature columns...")
    X = df[["packetSize", "interArrival"]].copy()

    print("[3/7] Generating synthetic latency target using physical network formula...")
    np.random.seed(RANDOM_STATE)
    y = (
        0.02
        + (X["packetSize"] * 0.00001)
        + (X["interArrival"] * 0.05)
        + np.random.normal(0, 0.005, len(df))
    )

    print("[4/7] Splitting train and test sets (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )

    print("[5/7] Initializing Random Forest Ensemble...")
    model = RandomForestRegressor(n_estimators=10, max_depth=10, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)

    print("[6/7] Evaluating model...")
    y_pred = model.predict(X_test)
    print(f"MAE: {mean_absolute_error(y_test, y_pred):.6f}")

    print("[7/7] Exporting model to pure Java using m2cgen...")
    java_code = m2c.export_to_java(model, class_name="OfflineAiPredictor")
    with open("OfflineAiPredictor.java", "w", encoding="utf-8") as java_file:
        java_file.write(java_code)
    print("Exported Java model to OfflineAiPredictor.java")

if __name__ == "__main__":
    main()
