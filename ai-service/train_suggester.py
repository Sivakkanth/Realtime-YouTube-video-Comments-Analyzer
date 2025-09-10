import os
import mlflow
import mlflow.pyfunc
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Hugging Face model
MODEL_NAME = "dilexsan/flan_t5_youtube_comments_suggestion"
MLFLOW_MODEL_NAME = "youtube_comment_suggestion"
MLFLOW_TRACKING_URI = "http://localhost:5000"

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment(MLFLOW_MODEL_NAME)

class SuggestionGeneratorWrapper(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
        self.generator = pipeline("text2text-generation", model=model, tokenizer=self.tokenizer)

    def predict(self, context, model_input):
        comments = model_input["text"].tolist()
        suggestions = []
        for comment in comments:
            try:
                input_text = "generate suggestion: " + comment
                out = self.generator(input_text, max_length=150, min_length=30, do_sample=False)
                suggestions.append(out[0]["generated_text"])
            except Exception as e:
                suggestions.append(f"Error: {str(e)}")
        return suggestions

if __name__ == "__main__":
    with mlflow.start_run() as run:
        mlflow.pyfunc.log_model(
            artifact_path="model",
            python_model=SuggestionGeneratorWrapper(),
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