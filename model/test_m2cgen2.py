import m2cgen as m2c
from sklearn.ensemble import AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
import numpy as np

X = np.array([[1.0, 2.0], [3.0, 4.0]])
y = np.array([1.0, 2.0])

model = AdaBoostRegressor(estimator=DecisionTreeRegressor(max_depth=4), n_estimators=50)
model.fit(X, y)
try:
    code = m2c.export_to_java(model, class_name="AdaBoostAI")
    print("m2cgen supports AdaBoostRegressor!")
except Exception as e:
    print(f"Error: {e}")
