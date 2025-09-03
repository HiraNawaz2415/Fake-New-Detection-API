from fastapi import FastAPI
from backend.schemas import NewsInput
from backend.ml_model import predict_news
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Fake News Detection API",
    description="An API to detect Fake vs Real news using ML model",
    version="1.0.0",
    docs_url="/docs",     # Swagger UI
    redoc_url="/redoc"    # ReDoc UI
)

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Fake News Detection API is working!"}

@app.post("/predict")
def predict(news: NewsInput):
    label, probability = predict_news(news.text)
    return {
        "prediction": label,
        "probability": probability
    }
