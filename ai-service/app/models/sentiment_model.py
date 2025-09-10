# import mlflow.pyfunc

# # Tracking URI
# mlflow.set_tracking_uri("http://localhost:5000")

# # Registered model name
# MODEL_NAME = "youtube_comment_sentiment_analysis"

# # Load the latest version automatically
# sentiment_model = mlflow.pyfunc.load_model(f"models:/{MODEL_NAME}/latest")

# print("✅ Loaded the latest sentiment model successfully!")

import mlflow.pyfunc
import os

# Path to your MLflow model directory
# MODEL_PATH = r"D:\Engineering Notes\Semester 7\EC7203\Assignment\project\Realtime-YouTube-video-Comments-Analyzer\ai-service\mlruns\1\models\m-6f596ecd60ac4a64a26b9225757132d5\artifacts"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(
    BASE_DIR,
    "mlruns",
    "2",
    "models",
    "m-6da0166d88034c299f99908b8627bd34",
    "artifacts"
)

# Verify that MLmodel file exists
mlmodel_file = os.path.join(MODEL_PATH, "MLmodel")
if not os.path.exists(mlmodel_file):
    raise FileNotFoundError(f"MLmodel file not found in: {MODEL_PATH}")

# Load the model locally (no MLflow server needed)
sentiment_model = mlflow.pyfunc.load_model(MODEL_PATH)

print("✅ Sentiment model loaded successfully from local path!")