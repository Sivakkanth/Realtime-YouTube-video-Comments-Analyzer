import mlflow.pyfunc

# Tracking URI
mlflow.set_tracking_uri("http://localhost:5000")

# Registered model name
MODEL_NAME = "youtube_comment_summarizer"

# Load the latest version automatically
summarizer_model = mlflow.pyfunc.load_model(f"models:/{MODEL_NAME}/latest")

print("✅ Loaded the latest summarizer model successfully!")

# import mlflow.pyfunc
# import os

# # Path to your MLflow model directory
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# MODEL_PATH = os.path.join(
#     BASE_DIR,
#     "mlruns",
#     "1",
#     "models",
#     "m-9465c416e2ba430cb5834ba6ecaadf1f",
#     "artifacts"
# )

# # Verify that MLmodel file exists
# mlmodel_file = os.path.join(MODEL_PATH, "MLmodel")
# if not os.path.exists(mlmodel_file):
#     raise FileNotFoundError(f"MLmodel file not found in: {MODEL_PATH}")

# # Load the model locally (no MLflow server needed)
# summarizer_model = mlflow.pyfunc.load_model(MODEL_PATH)

# print("✅ Summarizer model loaded successfully from local path!")