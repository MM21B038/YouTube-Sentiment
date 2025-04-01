import mlflow
from mlflow.tracking import MlflowClient
import mlflow.exceptions

MODEL_NAME = "YouTube_Comment_Sentiment_Analysis"
client = MlflowClient()

# Get latest trained model
new_run = mlflow.search_runs(experiment_names=["Sentiment_Analysis"], order_by=["start_time desc"]).iloc[0]
new_model_uri = f"runs:/{new_run.run_id}/xgboost_model"
new_accuracy = new_run["metrics.accuracy"]

def get_latest_production_model():
    versions = client.get_latest_versions(MODEL_NAME, stages=["Production"])
    return versions[0] if versions else None

try:
    prev_model = get_latest_production_model()
    if prev_model:
        prev_model_metrics = client.get_run(prev_model.run_id).data.metrics
        prev_accuracy = prev_model_metrics.get("accuracy", 0)

        if new_accuracy >= prev_accuracy:
            print("✅ New model is better! Promoting to Staging.")
            # Archive the previous Production model
            client.transition_model_version_stage(MODEL_NAME, prev_model.version, stage="Archived")
            # Create a new model version from the new run
            client.create_model_version(MODEL_NAME, new_model_uri, new_run.run_id)
            # Promote the latest model version to Staging
            staging_model = client.get_latest_versions(MODEL_NAME)[0]
            client.transition_model_version_stage(MODEL_NAME, staging_model.version, stage="Production")
        else:
            print("⚠️ New model is NOT better. Keeping the previous model in Production.")
    else:
        print("🚀 No Production model found. Registering new model in Staging.")
        try:
            client.create_registered_model(MODEL_NAME)
        except mlflow.exceptions.MlflowException as e:
            if "already exists" in str(e):
                print(f"Model {MODEL_NAME} is already registered.")
            else:
                raise e
        client.create_model_version(MODEL_NAME, new_model_uri, new_run.run_id)
        staging_model = client.get_latest_versions(MODEL_NAME)[0]
        client.transition_model_version_stage(MODEL_NAME, staging_model.version, stage="Staging")
except Exception as e:
    # This block catches any other exceptions (e.g., on first model training)
    print("🚀 First model training. Registering it in Staging.")
    try:
        client.create_registered_model(MODEL_NAME)
    except mlflow.exceptions.MlflowException as e:
        if "already exists" in str(e):
            print(f"Model {MODEL_NAME} is already registered.")
        else:
            raise e
    client.create_model_version(MODEL_NAME, new_model_uri, new_run.run_id)
    staging_model = client.get_latest_versions(MODEL_NAME)[0]
    client.transition_model_version_stage(MODEL_NAME, staging_model.version, stage="Production")