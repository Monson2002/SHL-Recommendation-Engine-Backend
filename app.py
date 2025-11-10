import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.embedding import EmbeddingManager
from src.vector_store import VectorStore
from src.retrive import Retriever
from src.recommend_tests import recommend_tests

# Load components ONCE at startup
embedder = EmbeddingManager("all-MiniLM-L6-v2")
store = VectorStore(collection_name="shl_assessments", persist_dir="./Data/RAG/vector_store")
retriever = Retriever(store, embedder)

app = FastAPI(title="SHL Assessment Recommender")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Recommendation(BaseModel):
    assessment_name: str
    assessment_url: str

class HealthResponse(BaseModel):
    status: str

class RecommendRequest(BaseModel):
    query: str
    top_k: int = 10

@app.get("/")
def root():
    return {"message": "SHL Assessment Recommender API is running"}

@app.get('/health', status_code=200)
def get_health():
    return {
        "status": 'healthy'
    }

@app.post("/recommend")
def get_recommendations(request: RecommendRequest):
    if not request.query.strip():
        raise HTTPException(400, "Query cannot be empty.")

    if request.top_k < 1 or request.top_k > 10:
        raise HTTPException(400, "top_k must be between 1 and 10.")

    recs = recommend_tests(
        query=request.query,
        retriever=retriever,
        top_k=request.top_k
    )

    if len(recs) == 0:
        raise HTTPException(404, "No relevant assessments found.")

    return {"recommended_assessments": recs}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
