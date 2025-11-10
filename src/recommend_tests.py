from typing import List, Dict
from src.retrive import Retriever

def recommend_tests(query: str, retriever, top_k: int = 10):
    results = retriever.retrieve(query=query, k=50)  
    
    seen_urls = set()
    recommendations = []

    for r in results:
        meta = r["metadata"]
        url = meta.get("url", "")

        if not url or url in seen_urls:
            continue
        seen_urls.add(url)

        # convert test_type to list
        test_type_raw = meta.get("test_type", "")
        test_type = [t.strip() for t in test_type_raw.split(",") if t.strip()]

        # extract duration as an integer
        length_raw = meta.get("assessment_length", "")
        duration = None
        if "=" in length_raw:
            try:
                duration = int(length_raw.split("=")[-1].strip())
            except:
                duration = None

        item = {
            "url": url,
            "name": meta.get("assessment_name", ""),
            "description": meta.get("description", ""),
            "duration": duration,
            "remote_support": "Yes",
            "adaptive_support": "No",
            "test_type": test_type
        }

        recommendations.append(item)

        if len(recommendations) >= top_k:
            break

    return recommendations