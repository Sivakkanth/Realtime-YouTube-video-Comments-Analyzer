import mlflow
import mlflow.pytorch
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
import torch
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

data = {
    "train": [
        {"text": "I love this product!", "label": 1},
        {"text": "This is the worst experience ever.", "label": 0},
        {"text": "Absolutely fantastic performance!", "label": 1},
        {"text": "I hate the way it works.", "label": 0},
        {"text": "Great value for the price.", "label": 1},
        {"text": "Horrible quality, very disappointing.", "label": 0},
        {"text": "Best purchase I've made all year.", "label": 1},
        {"text": "Terrible service, never coming back.", "label": 0},
        {"text": "I feel so happy with this!", "label": 1},
        {"text": "What a waste of money!", "label": 0},
        {"text": "Totally worth it, would buy again!", "label": 1},
        {"text": "The product broke after a week.", "label": 0},
        {"text": "Highly recommended, exceeded expectations!", "label": 1},
        {"text": "I can't believe how bad this is.", "label": 0},
        {"text": "Such a wonderful experience!", "label": 1},
        {"text": "This item is complete garbage.", "label": 0},
        {"text": "Incredible quality, I'm impressed.", "label": 1},
        {"text": "Never buying this again.", "label": 0},
        {"text": "I adore this product, it's amazing.", "label": 1},
        {"text": "Complete waste of time and money.", "label": 0},
        {"text": "Very satisfying, will buy again.", "label": 1},
        {"text": "This product is a scam.", "label": 0},
        {"text": "Absolutely love it!", "label": 1},
        {"text": "The worst purchase I've ever made.", "label": 0},
        {"text": "Totally worth the price!", "label": 1},
        {"text": "Awful product, do not buy.", "label": 0},
        {"text": "Fantastic quality, highly recommend.", "label": 1},
        {"text": "Very disappointed with this product.", "label": 0},
        {"text": "The best product in its category.", "label": 1},
        {"text": "I regret buying this, it's terrible.", "label": 0},
        {"text": "I'm very happy with this purchase.", "label": 1},
        {"text": "This is by far the worst experience.", "label": 0},
        {"text": "This product is top-notch.", "label": 1},
        {"text": "Very poor quality, do not recommend.", "label": 0},
        {"text": "Couldn't be happier with my purchase!", "label": 1},
        {"text": "Absolutely dreadful, would not recommend.", "label": 0},
        {"text": "I love this, it works perfectly.", "label": 1},
        {"text": "It broke down after one use.", "label": 0},
        {"text": "I am thoroughly impressed!", "label": 1},
        {"text": "Very unsatisfactory, wouldn't buy again.", "label": 0},
        {"text": "So happy with this, 5 stars!", "label": 1},
        {"text": "Waste of money, extremely disappointing.", "label": 0},
        {"text": "Amazing product, totally worth it.", "label": 1},
        {"text": "Worst purchase ever, do not buy.", "label": 0},
        {"text": "Great product for the price.", "label": 1},
        {"text": "Not worth the money, very bad.", "label": 0},
        {"text": "Absolutely fantastic!", "label": 1},
        {"text": "I will never buy this again.", "label": 0},
        {"text": "Best decision I ever made!", "label": 1},
        {"text": "Awful, this is junk.", "label": 0},
        {"text": "Incredible performance, highly recommended.", "label": 1},
        {"text": "Very unsatisfactory, don't waste your money.", "label": 0},
        {"text": "Perfect for my needs, I'm so happy.", "label": 1},
        {"text": "It did not live up to my expectations.", "label": 0},
        {"text": "Great quality and excellent value.", "label": 1},
        {"text": "Horrible quality, wouldn't recommend.", "label": 0},
        {"text": "I'm so pleased with this purchase.", "label": 1},
        {"text": "This is not what I expected, very poor.", "label": 0},
        {"text": "A fantastic experience overall!", "label": 1},
        {"text": "I am highly disappointed with this.", "label": 0},
        {"text": "Love this! Works perfectly.", "label": 1},
        {"text": "Terrible, don't waste your money.", "label": 0},
        {"text": "Highly recommend this, fantastic quality.", "label": 1},
        {"text": "Very bad, doesn't work as advertised.", "label": 0},
        {"text": "I am absolutely satisfied with my purchase.", "label": 1},
        {"text": "The worst item I have bought.", "label": 0},
        {"text": "This is absolutely perfect for me!", "label": 1},
        {"text": "I would not suggest this to anyone.", "label": 0}
    ],
    "test": [
        {"text": "The quality is amazing.", "label": 1},
        {"text": "Terrible product. Do not buy.", "label": 0},
        {"text": "I absolutely love this product!", "label": 1},
        {"text": "Waste of money, very disappointed.", "label": 0},
        {"text": "Fantastic value for the price!", "label": 1},
        {"text": "This is the worst experience ever.", "label": 0},
        {"text": "Highly recommend, works great.", "label": 1},
        {"text": "Never again, terrible product.", "label": 0},
        {"text": "Very happy with my purchase!", "label": 1},
        {"text": "I regret buying this, not worth it.", "label": 0},
        {"text": "Totally worth it, would buy again!", "label": 1},
        {"text": "This is an awful product, don't buy it.", "label": 0},
        {"text": "I love how this works, so happy!", "label": 1},
        {"text": "This is a scam, do not buy.", "label": 0},
        {"text": "Great product, will purchase again.", "label": 1},
        {"text": "Horrible, don't waste your time or money.", "label": 0},
        {"text": "Totally worth the price, amazing quality.", "label": 1},
        {"text": "Very disappointing, wouldn't recommend.", "label": 0},
        {"text": "Superb quality, highly recommended.", "label": 1},
        {"text": "This is junk, don't buy it.", "label": 0},
        {"text": "I'm so happy with this, thank you!", "label": 1},
        {"text": "Worst experience ever, horrible product.", "label": 0},
        {"text": "Very satisfied with my purchase.", "label": 1},
        {"text": "This is garbage, don't waste your money.", "label": 0},
        {"text": "Incredible, will buy more for sure.", "label": 1},
        {"text": "This product is a fraud, stay away.", "label": 0},
        {"text": "I can't recommend this enough, love it.", "label": 1},
        {"text": "The quality is terrible, regret this purchase.", "label": 0},
        {"text": "Absolutely fantastic, highly recommend.", "label": 1},
        {"text": "Waste of time and money, very bad.", "label": 0},
        {"text": "So happy with this, works perfectly.", "label": 1},
        {"text": "Very poor quality, I don't recommend it.", "label": 0},
        {"text": "Excellent purchase, 5 stars!", "label": 1},
        {"text": "I'm so upset with this purchase, very poor.", "label": 0},
        {"text": "Incredible product, worth every penny.", "label": 1},
        {"text": "Horrible, doesn't work at all.", "label": 0},
        {"text": "Best decision ever, I love this!", "label": 1},
        {"text": "This product is a disaster.", "label": 0},
        {"text": "Very pleased, exactly what I needed.", "label": 1},
        {"text": "This was a total mistake, not recommended.", "label": 0},
        {"text": "This product is exactly what I expected!", "label": 1},
        {"text": "This is a scam, avoid it.", "label": 0}
    ],
}

train_data = Dataset.from_list(data["train"])
test_data = Dataset.from_list(data["test"])

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)

train_data = train_data.map(tokenize_function, batched=True)
test_data = test_data.map(tokenize_function, batched=True)

model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = torch.argmax(torch.tensor(logits), dim=1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, predictions, average="binary")
    acc = accuracy_score(labels, predictions)
    return {"accuracy": acc, "f1": f1, "precision": precision, "recall": recall}

training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_data,
    eval_dataset=test_data,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

mlflow.set_tracking_uri("file:./mlruns")
mlflow.set_experiment("sentiment-analysis")

with mlflow.start_run():
    mlflow.log_params({
        "learning_rate": training_args.learning_rate,
        "batch_size": training_args.per_device_train_batch_size,
        "num_train_epochs": training_args.num_train_epochs,
    })

    trainer.train()
    results = trainer.evaluate()
    mlflow.log_metrics(results)
    

    model.save_pretrained("./my_model")
    tokenizer.save_pretrained("./my_model")

    mlflow.pytorch.log_model(model, artifact_path="sentiment_model")
    print("Sentiment Model Training Completed ✅")