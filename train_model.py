from datasets import load_dataset
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
import pickle

print("Loading liar2 dataset from Hugging Face...")
dataset = load_dataset("chengxuphd/liar2")

# Convert splits to DataFrames
df_train = dataset["train"].to_pandas()
df_test = dataset["test"].to_pandas()

# Merge train + test
df = pd.concat([df_train, df_test], ignore_index=True)

X = df["statement"]
y = df["label"]

# Convert 6-class labels → binary
y = y.apply(lambda x: 1 if x <= 2 else 0)  # 1 = Fake, 0 = Real

# Train-test split
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Vectorizer
vectorizer = TfidfVectorizer(stop_words="english", max_df=0.7, max_features=10000)
X_train_vec = vectorizer.fit_transform(X_train)
X_val_vec = vectorizer.transform(X_val)

# Model
model = PassiveAggressiveClassifier(max_iter=50, random_state=42)
model.fit(X_train_vec, y_train)

# Evaluate
y_pred = model.predict(X_val_vec)
acc = accuracy_score(y_val, y_pred)
print(f"✅ Accuracy on liar2 dataset: {acc*100:.2f}%")

# Save
with open("model.pkl", "wb") as f:
    pickle.dump((vectorizer, model), f)

print("🎉 Model trained & saved to model.pkl")
