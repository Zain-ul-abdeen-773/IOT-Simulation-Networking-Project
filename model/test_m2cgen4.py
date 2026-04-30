import m2cgen as m2c
from sklearn.ensemble import IsolationForest
import numpy as np

X = np.array([[1.0, 2.0], [3.0, 4.0], [100.0, 200.0]])

model = IsolationForest(n_estimators=10)
model.fit(X)
try:
    code = m2c.export_to_java(model, class_name="AnomalyAI")
    print("m2cgen supports IsolationForest!")
except Exception as e:
    print(f"Error: {e}")
