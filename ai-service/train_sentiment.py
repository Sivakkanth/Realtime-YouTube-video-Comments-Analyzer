import os
import mlflow
import mlflow.pyfunc
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

MODEL_NAME = "dilexsan/bertweet_base_sentimental"
MLFLOW_MODEL_NAME = "youtube_comment_sentiment_analysis"
MLFLOW_TRACKING_URI = "http://localhost:5000"

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment(MLFLOW_MODEL_NAME)

class SentimentWrapper(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
        self.classifier = pipeline("text-classification", model=model, tokenizer=self.tokenizer, framework="pt", return_all_scores=False)

    def predict(self, context, model_input: pd.DataFrame):
        texts = model_input["text"].tolist()
        sentiment = []
        for txt in texts:
            try:
                out = self.classifier(txt)[0]
                label = out["label"]
                if label.lower() == "neutral":
                    continue

                sentiment.append(label.lower())
            except Exception as e:
                sentiment.append(f"Error: {str(e)}")
        return sentiment

if __name__ == "__main__":
    with mlflow.start_run() as run:
        mlflow.pyfunc.log_model(
            artifact_path="model",
            python_model=SentimentWrapper(),
            conda_env={
                'channels': ['defaults'],
                'dependencies': [
                    'python=3.10',
                    'pip',
                    {'pip': [
                        'mlflow',
                        'torch',
                        'transformers',
                        'sentencepiece',
                        'pandas'
                    ]}
                ],
                'name': 'mlflow-env'
            },
            registered_model_name=MLFLOW_MODEL_NAME
        )
    print(f"Sentiment model logged and registered in MLflow: {MLFLOW_MODEL_NAME}")