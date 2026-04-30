import m2cgen as m2c
from sklearn.ensemble import RandomForestRegressor
import numpy as np

X = np.array([[1.0, 2.0], [3.0, 4.0]])
y = np.array([1.0, 2.0])

model = RandomForestRegressor(n_estimators=10)
model.fit(X, y)
try:
    code = m2c.export_to_java(model, class_name="RandomForestAI")
    print("m2cgen supports RandomForestRegressor!")
except Exception as e:
    print(f"Error: {e}")
