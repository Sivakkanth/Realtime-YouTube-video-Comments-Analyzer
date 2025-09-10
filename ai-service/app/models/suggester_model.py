import mlflow.pyfunc

# Tracking URI
mlflow.set_tracking_uri("http://localhost:5000")

# Registered model name
MODEL_NAME = "youtube_comment_suggestion"

# Load the latest version automatically
suggester_model = mlflow.pyfunc.load_model(f"models:/{MODEL_NAME}/latest")

print("✅ Loaded the latest suggester model successfully!")

# import mlflow.pyfunc
# import os

# # Path to your MLflow model directory
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# MODEL_PATH = os.path.join(
#     BASE_DIR,
#     "mlruns",
#     "3",
#     "models",
#     "m-25d8b234074f4920885dec2e0196b238",
#     "artifacts"
# )

# # Verify that MLmodel file exists
# mlmodel_file = os.path.join(MODEL_PATH, "MLmodel")
# if not os.path.exists(mlmodel_file):
#     raise FileNotFoundError(f"MLmodel file not found in: {MODEL_PATH}")

# # Load the model locally (no MLflow server needed)
# suggester_model = mlflow.pyfunc.load_model(MODEL_PATH)
# print("✅ Suggester model loaded successfully from local path!")