import json
import pandas as pd

from pathlib import Path
from langchain_core.documents import Document

def prepare_rag_docs(csv_path="Data/assessments_cleaned.csv",
                     output_json="Data/RAG/rag_docs.json"):

    print("Loading CSV:", csv_path)
    df = pd.read_csv(csv_path)

    docs = []

    for idx, row in df.iterrows():

        # === Load all fields safely ===
        name      = row.get("assessment_name", "")
        desc      = row.get("description", "")
        levels    = row.get("job_levels", "")
        ttype     = row.get("test_type", "")
        url       = row.get("url", "")

        # engineered fields (if present)
        length_original = row.get("assessment_length", "")
        length_minutes  = row.get("assessment_length_minutes", "")
        word_count      = row.get("description_word_count", "")
        levels_list     = row.get("job_levels_list", "")

        # === Build final RAG string ===
        text = f"""
Assessment Name: {name}

Description:
{desc}

Test Type: {ttype}

Job Levels: {levels}
Job Levels List: {levels_list}

Assessment Length (raw): {length_original}
Assessment Length (minutes): {length_minutes}

Description Word Count: {word_count}

URL: {url}
""".strip()

        docs.append(
            Document(
                page_content=text,
                metadata={
                    "assessment_name": name,
                    "url": url,
                    "test_type": ttype,
                    "job_levels": levels,
                    "assessment_length_minutes": length_minutes,
                    "word_count": word_count,
                    "row_id": int(idx)
                }
            )
        )

    # === Serialize safely: avoid page_content=list bug ===
    serialized_docs = []
    for d in docs:
        serialized_docs.append({
            "page_content": d.page_content,   # ✅ always string
            "metadata": d.metadata
        })

    # Save
    Path(output_json).parent.mkdir(parents=True, exist_ok=True)
    with open(output_json, "w", encoding="utf-8") as f:
        for doc in serialized_docs:
            f.write(json.dumps(doc) + "\n")

    print(f"Saved {len(serialized_docs)} RAG documents → {output_json}")

    return serialized_docs

if __name__ == "__main__":
    prepare_rag_docs()