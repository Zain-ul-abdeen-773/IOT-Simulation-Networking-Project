import pandas as pd
import numpy as np

def generate_gan_ddos():
    print("Simulating GAN Generator Output...")
    # Load normal traffic to get bounds
    df = pd.read_csv('clean_mqtt_traffic.csv')
    
    # Generate 500 malicious packets
    # A volumetric DDoS has massive packet sizes and tiny inter-arrival times
    n = 500
    
    # GAN generated packet sizes (anomaly bounds)
    sizes = np.random.normal(loc=15000, scale=2000, size=n)
    
    # GAN generated inter-arrival times (micro-bursts)
    arrivals = np.random.exponential(scale=10.0, size=n)
    
    # Simulated flow duration for anomalous traffic
    durations = np.random.normal(loc=150.0, scale=30.0, size=n)
    
    ddos_df = pd.DataFrame({
        'packetSize': sizes,
        'interArrival': arrivals,
        'flowDuration': durations
    })
    
    ddos_df.to_csv('ddos_traffic.csv', index=False)
    print("Generated 500 GAN-simulated malicious packets in ddos_traffic.csv")

if __name__ == '__main__':
    generate_gan_ddos()
