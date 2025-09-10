import os
import mlflow
import mlflow.pyfunc
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

os.environ["HTTP_PROXY"] = "http://10.50.225.222:3128"
os.environ["HTTPS_PROXY"] = "http://10.50.225.222:3128"
os.environ["NO_PROXY"] = "localhost,127.0.0.1"

MODEL_NAME = "Sivakkanth/youtube_comments_summarizer"
MLFLOW_MODEL_NAME = "youtube_comment_summarizer"
MLFLOW_TRACKING_URI = "http://localhost:5000"

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment(MLFLOW_MODEL_NAME)

class SummarizerWrapper(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
        self.summarizer = pipeline("summarization", model=model, tokenizer=self.tokenizer, framework="pt")

    def predict(self, context, model_input):
        texts = model_input["text"].tolist()
        summaries = []
        for txt in texts:
            try:
                out = self.summarizer(txt, max_length=150, min_length=30, do_sample=False)
                summaries.append(out[0]["summary_text"])
            except Exception as e:
                summaries.append(f"Error: {str(e)}")
        return summaries

if __name__ == "__main__":
    with mlflow.start_run() as run:
        mlflow.pyfunc.log_model(
            artifact_path="model",
            python_model=SummarizerWrapper(),
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
    print(f"Model logged and registered in MLflow: {MLFLOW_MODEL_NAME}")