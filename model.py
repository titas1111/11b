# from sklearn.ensemble import RandomForestRegressor
# from sklearn.metrics import mean_absolute_error
from sklearn.externals import joblib


def predict(flat):
    model = joblib.load("my_model.pkl")
    return model.predict(flat)
