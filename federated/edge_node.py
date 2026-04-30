import pandas as pd
import numpy as np
from sklearn.linear_model import SGDRegressor
import pickle

class EdgeNode:
    def __init__(self, node_id, data_path):
        self.node_id = node_id
        self.data_path = data_path
        # Use SGDRegressor since it supports partial_fit (ideal for federated learning)
        self.model = SGDRegressor(max_iter=1000, tol=1e-3, random_state=42)
        
    def train_locally(self):
        print(f"[Edge Node {self.node_id}] Loading local dataset...")
        df = pd.read_csv(self.data_path)
        
        # Simulate local data slice based on node_id
        chunk_size = len(df) // 3
        start_idx = self.node_id * chunk_size
        local_df = df.iloc[start_idx : start_idx + chunk_size]
        
        X = local_df[["packetSize", "interArrival"]].values
        y = local_df["flowDuration"].values
        
        print(f"[Edge Node {self.node_id}] Training on {len(X)} local packets...")
        # Since we use SGD, we must normalize. For demonstration, we just fit directly.
        self.model.partial_fit(X, y)
        
        # Return weights (coef_ and intercept_)
        weights = {
            'coef': self.model.coef_,
            'intercept': self.model.intercept_
        }
        
        print(f"[Edge Node {self.node_id}] Sending local weights to Cloud.")
        return weights

if __name__ == '__main__':
    # Simulating an edge node running independently
    edge = EdgeNode(node_id=0, data_path='../model/clean_mqtt_traffic.csv')
    weights = edge.train_locally()
    
    # Save weights to simulate transmitting to cloud
    with open('edge_0_weights.pkl', 'wb') as f:
        pickle.dump(weights, f)
