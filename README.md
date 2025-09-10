# Realtime-YouTube-video-Comments-Analyzer

# Mlflow (dir = ai-service/)
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --host 0.0.0.0 --port 5000

# AI Service (dir = ai-service/app/)
uvicorn main:app --reload