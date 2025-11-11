def recommend_tests(query: str, retriever, top_k: int = 10):
    results = retriever.retrieve(query=query, k=top_k)

    seen = set()
    output = []

    for r in results:
        meta = r["metadata"]
        url = meta.get("url")

        if not url or url in seen:
            continue
        seen.add(url)

        test_type_raw = meta.get("test_type", "")
        test_type = [t.strip() for t in test_type_raw.split(",") if t.strip()]

        item = {
            "url": url,
            "name": meta.get("assessment_name", ""),
            "description": meta.get("description", ""),
            "duration": meta.get("duration", None),
            "remote_support": "Yes",
            "adaptive_support": "No",
            "test_type": test_type
        }

        output.append(item)
        if len(output) == top_k:
            break

    return output