import pandas as pd
import numpy as np
from src.embedding import EmbeddingManager
from src.vector_store import VectorStore
from src.retrive import Retriever
from src.recommend_tests import recommend_tests


QUERY_FILE = "Gen_AI Dataset.xlsx"      # Excel file given by SHL
SHEET_NAME = "Test-Set"          # The sheet that contains queries
OUTPUT_FILE = "submission.csv"   # Required output file


def main():

    # Load only the Test-Set sheet
    df = pd.read_excel(QUERY_FILE, sheet_name=SHEET_NAME)

    if "Query" not in df.columns:
        raise ValueError(f"'Query' column not found in sheet: {SHEET_NAME}")

    queries = df["Query"].dropna().tolist()

    print(f"Loaded {len(queries)} queries from sheet '{SHEET_NAME}'")

    # Load recommender
    embedder = EmbeddingManager("all-MiniLM-L6-v2")
    store = VectorStore(collection_name="shl_assessments", persist_dir="./Data/RAG/vector_store")
    retriever = Retriever(store, embedder)

    rows = []

    for q in queries:
        print(f"\nProcessing query: {q}")
        
        recs = recommend_tests(query=q, retriever=retriever, top_k=10)

        if len(recs) == 0:
            rows.append({
                "Query": q,
                "Assessment_url": "NO MATCH FOUND"
            })
            continue

        # Insert multiple rows per query
        for r in recs:
            rows.append({
                "Query": q,
                "Assessment_url": r["url"]
            })

    # Save to CSV
    out_df = pd.DataFrame(rows)
    out_df.to_csv(OUTPUT_FILE, index=False)

    print(f"\n✅ Submission CSV generated successfully → {OUTPUT_FILE}")


if __name__ == "__main__":
    main()