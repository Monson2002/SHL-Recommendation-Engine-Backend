import csv
import json
import pandas as pd

from pathlib import Path
from langchain_core.documents import Document

def prepare_rag_docs(csv_path="Data/assessments_cleaned.csv",
                     output_json="Data/RAG/rag_docs.json"):

    Path("Data/RAG").mkdir(parents=True, exist_ok=True)

    with open(csv_path, "r", encoding="utf-8") as f_in, \
         open(output_json, "w", encoding="utf-8") as f_out:

        reader = csv.DictReader(f_in)

        for row in reader:
            duration = None
            if "=" in row["assessment_length"]:
                try:
                    duration = int(row["assessment_length"].split("=")[-1].strip())
                except:
                    duration = None

            test_type = [
                t.strip() for t in row["test_type"].split(",") 
                if t.strip()
            ]
            test_type_str = ", ".join(test_type)  

            # JSONL document
            doc = {
                "text": (
                    f"{row['assessment_name']}\n"
                    f"{row['description']}\n"
                ),
                "metadata": {
                    "assessment_name": row["assessment_name"],
                    "url": row["url"],
                    "description": row.get("description", "") or "",
                    "duration": duration if duration is not None else -1,
                    "test_type": test_type_str
                }
            }

            # Write each object as NEW LINE JSON — THIS IS JSONL
            f_out.write(json.dumps(doc) + "\n")

    print(f"✅ Successfully created {output_json}")

if __name__ == "__main__":
    prepare_rag_docs()