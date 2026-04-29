#!/usr/bin/env python3
"""Train a Voting Regressor for IoT network latency prediction."""

from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import AdaBoostRegressor, VotingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor

INPUT_CSV = "clean_mqtt_traffic.csv"
MODEL_OUTPUT = "latency_predictor.pkl"
RANDOM_STATE = 42
TEST_SIZE = 0.2


def build_adaboost_model(random_state: int) -> AdaBoostRegressor:
    """Create an AdaBoost regressor with a depth-limited decision tree base model."""
    base_tree = DecisionTreeRegressor(max_depth=4, random_state=random_state)

    # Support both new and older scikit-learn parameter names.
    try:
        return AdaBoostRegressor(
            estimator=base_tree,
            n_estimators=50,
            random_state=random_state,
        )
    except TypeError:
        return AdaBoostRegressor(
            base_estimator=base_tree,
            n_estimators=50,
            random_state=random_state,
        )


def main() -> None:
    print("[1/7] Loading dataset...")
    input_path = Path.cwd() / INPUT_CSV
    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_path}. Please ensure {INPUT_CSV} exists in the current directory."
        )

    df = pd.read_csv(input_path)
    print(f"Loaded {len(df)} rows from {input_path}")

    print("[2/7] Extracting feature columns...")
    required_columns = ["packet_size", "inter_arrival_time"]
    missing_columns = [column for column in required_columns if column not in df.columns]
    if missing_columns:
        raise KeyError(
            f"Missing required feature columns: {missing_columns}. Available columns: {list(df.columns)}"
        )

    X = df[["packet_size", "inter_arrival_time"]].copy()

    print("[3/7] Generating synthetic latency target using physical network formula...")
    np.random.seed(RANDOM_STATE)
    y = (
        0.02
        + (X["packet_size"] * 0.00001)
        + (X["inter_arrival_time"] * 0.05)
        + np.random.normal(0, 0.005, len(df))
    )

    print("[4/7] Splitting train and test sets (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
    )
    print(f"Train size: {len(X_train)} | Test size: {len(X_test)}")

    print("[5/7] Initializing base models...")
    model_linear = LinearRegression()
    model_svr = make_pipeline(StandardScaler(), SVR())
    model_adaboost = build_adaboost_model(RANDOM_STATE)

    print("[6/7] Building and training Voting Regressor ensemble...")
    voting_regressor = VotingRegressor(
        estimators=[
            ("linear_regression", model_linear),
            ("scaled_svr", model_svr),
            ("adaboost_tree", model_adaboost),
        ]
    )
    voting_regressor.fit(X_train, y_train)

    print("[7/7] Evaluating model and saving artifact...")
    y_pred = voting_regressor.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Mean Absolute Error (MAE): {mae:.6f}")
    print(f"R^2 Score: {r2:.6f}")

    output_path = Path.cwd() / MODEL_OUTPUT
    joblib.dump(voting_regressor, output_path)
    print(f"Saved trained Voting Regressor to: {output_path}")


if __name__ == "__main__":
    main()
