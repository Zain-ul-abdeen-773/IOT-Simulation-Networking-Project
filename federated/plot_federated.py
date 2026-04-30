import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_absolute_error
import os

def run_federated_simulation():
    print("Loading Dataset for Federated Learning...")
    df = pd.read_csv('../model/clean_mqtt_traffic.csv')
    
    # Simulating 3 Edge Nodes
    X = df[['packetSize', 'interArrival']].values
    y = df['flowDuration'].values
    
    # Normalize features for SGD
    X = (X - X.mean(axis=0)) / X.std(axis=0)
    
    # Partition data
    n_samples = len(X)
    chunk = n_samples // 3
    nodes_X = [X[0:chunk], X[chunk:2*chunk], X[2*chunk:]]
    nodes_y = [y[0:chunk], y[chunk:2*chunk], y[2*chunk:]]
    
    # Initialize Global Model
    global_model = SGDRegressor(max_iter=1, tol=None, warm_start=True, random_state=42)
    # Fit once to initialize shapes
    global_model.fit(X[:10], y[:10])
    
    n_rounds = 10
    global_errors = []
    
    print(f"Starting FedAvg over {n_rounds} rounds...")
    for round_num in range(n_rounds):
        avg_coef = np.zeros_like(global_model.coef_)
        avg_intercept = np.zeros_like(global_model.intercept_)
        
        # Edge Nodes Train Locally
        for i in range(3):
            # Each node gets the global model weights first
            local_model = SGDRegressor(max_iter=5, tol=None, warm_start=True, random_state=42)
            local_model.fit(nodes_X[i][:10], nodes_y[i][:10]) # Initialize
            local_model.coef_ = global_model.coef_.copy()
            local_model.intercept_ = global_model.intercept_.copy()
            
            # Train locally for a few epochs
            local_model.partial_fit(nodes_X[i], nodes_y[i])
            
            # Send weights to cloud
            avg_coef += local_model.coef_ / 3.0
            avg_intercept += local_model.intercept_ / 3.0
            
        # Cloud Aggregation (FedAvg)
        global_model.coef_ = avg_coef
        global_model.intercept_ = avg_intercept
        
        # Evaluate Global Model
        y_pred = global_model.predict(X)
        mae = mean_absolute_error(y, y_pred)
        global_errors.append(mae)
        print(f"Round {round_num+1} Global MAE: {mae:.2f}")

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, n_rounds+1), global_errors, marker='o', linestyle='-', color='#00F0FF', linewidth=3, markersize=10)
    
    # Styling for AI Dashboard look
    ax = plt.gca()
    ax.set_facecolor('#0D1117')
    plt.gcf().patch.set_facecolor('#0D1117')
    
    plt.title('Federated Learning (FedAvg) Convergence', color='white', fontsize=18, pad=20)
    plt.xlabel('Communication Round (Edge to Cloud)', color='white', fontsize=14)
    plt.ylabel('Global Model Error (MAE)', color='white', fontsize=14)
    
    ax.tick_params(colors='white', which='both')
    for spine in ax.spines.values():
        spine.set_edgecolor('#30363D')
    
    plt.grid(color='#30363D', linestyle='--', linewidth=1, alpha=0.5)
    
    # Save directly to artifacts
    artifacts_dir = r"C:\Users\Zain\.gemini\antigravity\brain\f9e68cf6-4140-46b0-9656-642968f01bec\artifacts"
    os.makedirs(artifacts_dir, exist_ok=True)
    save_path = os.path.join(artifacts_dir, 'fedavg_convergence.png')
    plt.savefig(save_path, bbox_inches='tight', dpi=150)
    print(f"Graph saved to {save_path}")

if __name__ == '__main__':
    run_federated_simulation()
