import m2cgen as m2c
from sklearn.ensemble import VotingRegressor
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import numpy as np

X = np.array([[1.0, 2.0], [3.0, 4.0]])
y = np.array([1.0, 2.0])

model_linear = LinearRegression()
model_svr = SVR() 
# We don't use pipeline for SVR because m2cgen handles model extraction. Let's see if it works with pipeline.
model_pipeline = make_pipeline(StandardScaler(), SVR())

voting_regressor = VotingRegressor(
    estimators=[
        ("linear_regression", model_linear),
        ("scaled_svr", model_pipeline)
    ]
)
voting_regressor.fit(X, y)
try:
    code = m2c.export_to_java(voting_regressor, class_name="AiPredictorEnsemble")
    print("m2cgen supports VotingRegressor!")
except Exception as e:
    print(f"Error: {e}")
