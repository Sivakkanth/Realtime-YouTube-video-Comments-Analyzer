import mlflow.pyfunc
import os

# Path to your MLflow model directory
# MODEL_PATH = r"D:\Engineering Notes\Semester 7\EC7203\Assignment\project\Realtime-YouTube-video-Comments-Analyzer\ai-service\mlruns\1\models\m-6f596ecd60ac4a64a26b9225757132d5\artifacts"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(
    BASE_DIR,
    "mlruns",
    "1",
    "models",
    "m-6f596ecd60ac4a64a26b9225757132d5",
    "artifacts"
)

# Verify that MLmodel file exists
mlmodel_file = os.path.join(MODEL_PATH, "MLmodel")
if not os.path.exists(mlmodel_file):
    raise FileNotFoundError(f"MLmodel file not found in: {MODEL_PATH}")

# Load the model locally (no MLflow server needed)
summarizer_model = mlflow.pyfunc.load_model(MODEL_PATH)

print("✅ Summarizer model loaded successfully from local path!")

# MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
# MLFLOW_MODEL_NAME = "youtube_comment_summarizer"

# mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# summarizer_model = mlflow.pyfunc.load_model(
#     model_uri=f"models:/{MLFLOW_MODEL_NAME}/Production"
# )

# # Load latest model from MLflow registry
# def load_summarizer():
#     model_uri = f"models:/{MLFLOW_MODEL_NAME}/latest"
#     summarizer_model = mlflow.pyfunc.load_model(model_uri)
#     return summarizer_model

# summarizer_model = load_summarizer()

# from transformers import pipeline, AutoTokenizer

# MODEL_NAME = "facebook/bart-large-cnn"

# def load_summarizer():
#     """Load the summarizer model and tokenizer"""
#     summarizer = pipeline("summarization", model=MODEL_NAME, framework="pt")
#     tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
#     return summarizer, tokenizer

# summarizer, tokenizer = load_summarizer()