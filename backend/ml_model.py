import pickle

# Load model and vectorizer together from model.pkl
with open("backend/model.pkl", "rb") as f:
    vectorizer, model = pickle.load(f)

def predict_news(text: str):
    X = vectorizer.transform([text])
    prediction = model.predict(X)[0]

    if hasattr(model, "predict_proba"):
        probability = model.predict_proba(X).max()
        probability = round(probability * 100, 2)
    elif hasattr(model, "decision_function"):
        margin = model.decision_function(X)
        probability = round(abs(margin[0]) / (1 + abs(margin[0])) * 100, 2)
    else:
        probability = "N/A"

    label = "Real News ✅" if prediction == 1 else "Fake News ❌"
    return label, probability
