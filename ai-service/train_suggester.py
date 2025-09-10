import json
import torch
import mlflow
import mlflow.transformers
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    DataCollatorForSeq2Seq,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback,
)

# ==============================
# Load your dataset
# ==============================
with open("/content/data_feedback.json", "r") as f:
    data_feedback = json.load(f)

with open("/content/data_suggestion.json", "r") as f:
    data_suggestion = json.load(f)

# Combine feedback and improvement suggestions
examples = []
for fb, imp in zip(data_feedback["feedback"], data_suggestion["improvement"]):
    examples.append({"input_text": fb, "target_text": imp})

dataset = Dataset.from_list(examples)
dataset = dataset.train_test_split(test_size=0.1)

# ==============================
# Load BART model & tokenizer
# ==============================
model_name = "facebook/bart-large-cnn"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# ==============================
# Preprocess function
# ==============================
def preprocess(batch):
    model_inputs = tokenizer(batch["input_text"], max_length=256, truncation=True, padding="max_length")
    labels = tokenizer(batch["target_text"], max_length=256, truncation=True, padding="max_length")

    # Replace padding token id with -100 to ignore in loss
    labels["input_ids"] = [
        [(token if token != tokenizer.pad_token_id else -100) for token in label]
        for label in labels["input_ids"]
    ]

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

tokenized_dataset = dataset.map(preprocess, batched=True, remove_columns=["input_text", "target_text"])

# ==============================
# Data Collator
# ==============================
data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

training_args = TrainingArguments(
    output_dir="./bart-feedback",
    eval_strategy="epoch",
    save_strategy="epoch",
    learning_rate=3e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=30,
    weight_decay=0.01,
    save_total_limit=2,
    logging_dir="./logs",
    logging_steps=50,
    push_to_hub=False,
    report_to="none",
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    greater_is_better=False,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"],
    tokenizer=tokenizer,
    data_collator=data_collator,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=3)],
)

# ==============================
# MLflow Experiment Tracking
# ==============================
mlflow.set_experiment("suggester-model")

with mlflow.start_run():
    # Log hyperparameters
    mlflow.log_params({
        "model_name": model_name,
        "learning_rate": training_args.learning_rate,
        "batch_size": training_args.per_device_train_batch_size,
        "epochs": training_args.num_train_epochs,
    })

    # Train model
    trainer.train()

    # Log final loss
    eval_metrics = trainer.evaluate()
    mlflow.log_metrics(eval_metrics)

    # Log and register the trained model in MLflow
    mlflow.transformers.log_model(
        transformers_model={
            "model": model,
            "tokenizer": tokenizer,
        },
        artifact_path="suggester-model",
        registered_model_name="youtube-suggester-model"
    )

# ==============================
# Example Inference
# ==============================
test_text = "Your video felt like a collection of random clips with no clear direction."
inputs = tokenizer(test_text, return_tensors="pt", truncation=True).to(model.device)

with torch.no_grad():
    outputs = model.generate(**inputs, max_length=128)
    print("Suggestion:", tokenizer.decode(outputs[0], skip_special_tokens=True))