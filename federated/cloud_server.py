import numpy as np
import pickle

class CloudAggregator:
    def __init__(self):
        self.global_weights = None
        
    def aggregate_weights(self, edge_weights_list):
        print("[Cloud Server] Received weights from Edge Nodes. Commencing FedAvg...")
        
        # Initialize global weights arrays
        avg_coef = np.zeros_like(edge_weights_list[0]['coef'])
        avg_intercept = np.zeros_like(edge_weights_list[0]['intercept'])
        
        n_nodes = len(edge_weights_list)
        
        # Federated Averaging (FedAvg) Mathematical Algorithm
        for w in edge_weights_list:
            avg_coef += w['coef'] / n_nodes
            avg_intercept += w['intercept'] / n_nodes
            
        self.global_weights = {
            'coef': avg_coef,
            'intercept': avg_intercept
        }
        
        print("[Cloud Server] Global Model mathematically aggregated successfully.")
        print(f"Global Coefs: {self.global_weights['coef']}")
        return self.global_weights

if __name__ == '__main__':
    # Simulating the Cloud receiving weights from 3 different Edge Nodes
    try:
        with open('edge_0_weights.pkl', 'rb') as f:
            w0 = pickle.load(f)
            
        # For simulation, let's pretend we received 3 slightly different weight packets
        w1 = {'coef': w0['coef'] * 1.05, 'intercept': w0['intercept'] * 0.95}
        w2 = {'coef': w0['coef'] * 0.92, 'intercept': w0['intercept'] * 1.08}
        
        cloud = CloudAggregator()
        global_model = cloud.aggregate_weights([w0, w1, w2])
        
    except Exception as e:
        print("Please run edge_node.py first to generate weights.")
