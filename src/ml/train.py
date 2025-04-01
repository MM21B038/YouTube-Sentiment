import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import mlflow
import mlflow.xgboost
from mlflow.models.signature import infer_signature
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# Set MLflow tracking and experiment
mlflow.set_tracking_uri("file:./mlruns")
mlflow.set_experiment("Sentiment_Analysis")

# Define file paths
FEATURES_PATH = "data/processed/features.csv"
MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

# Load features
df = pd.read_csv(FEATURES_PATH)

# Split data into features and labels
X = df.drop(columns=['label'])
y = df['label']

# Map sentiment labels to numeric values
# Adjust the mapping if necessary for your dataset
y = y.map({1: -1, 2: -1, 3: 0, 4: 1, 5: 1})

# Encode labels
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Split into training and testing datasets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize XGBoost model
model = xgb.XGBClassifier(eval_metric='mlogloss')

with mlflow.start_run(run_name = "xgb"):
    # Train the model
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average="weighted")
    for param, value in model.get_params().items():
        mlflow.log_param(param, value)
    
    # Log metrics to MLflow
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("f1_score", f1)

    # 🔍 Infer model signature (input-output mapping)
    signature = infer_signature(X_test[:1], model.predict(X_test[:1]))

    # Log the model using MLflow's XGBoost integration
    mlflow.xgboost.log_model(model, "xgboost_model", signature=signature, input_example=X_test[:1])

    # Save the model and label encoder locally for future use
    model_path = os.path.join(MODEL_DIR, "xg_model.pkl")
    joblib.dump(model, model_path)
    encoder_path = os.path.join(MODEL_DIR, "label_encoder.pkl")
    joblib.dump(label_encoder, encoder_path)
    
    # Log the saved model file as an artifact
    mlflow.log_artifact(model_path, artifact_path="xg_model")
    mlflow.log_artifact(encoder_path, artifact_path="xg_model")

    print(f"Model training complete. Accuracy: {accuracy:.4f}, F1 Score: {f1:.4f}")