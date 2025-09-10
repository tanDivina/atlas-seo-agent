from fastapi import FastAPI
from src.analyzers.content_analyzer import analyze_qae_score, generate_embedding_for_long_text

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/analyze")
def analyze(content: str):
    score = analyze_qae_score(content)
    embedding = generate_embedding_for_long_text(content)
    return {"score": score, "embedding_shape": embedding.shape if embedding.size > 0 else 0}