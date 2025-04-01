import mlflow.pyfunc
import mlflow
from mlflow.tracking import MlflowClient
from cleaning import CustomTextToVector
import numpy as np
import joblib

mlflow.set_tracking_uri("file:./mlruns")
MODEL_NAME = "YouTube_Comment_Sentiment_Analysis"
trans = CustomTextToVector()
encoder = joblib.load("models/label_encoder.pkl")
# Load the latest model from MLflow
model = mlflow.xgboost.load_model(f"models:/{MODEL_NAME}/Production")

def predict_sentiment(comment):
    vectors = trans.transform(comment)
    return encoder.inverse_transform(model.predict(np.array(vectors).reshape(len(vectors), -1)))
