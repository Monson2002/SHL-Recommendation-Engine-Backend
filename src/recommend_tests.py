from typing import List, Dict
from src.retrive import Retriever

def recommend_tests(
    query: str,
    retriever: Retriever,
    top_k: int = 10,
    min_results: int = 5,
    filter_packaged: bool = True
) -> List[Dict]:
    """
    Pure similarity-based recommendation engine.
    Returns top_k most similar SHL assessments (name + URL only).

    Args:
        query (str): Natural language query or job description.
        retriever (Retriever): Your Retriever object.
        top_k (int): Maximum number of results to return.
        min_results (int): Minimum required results (assignment requires ≥5).
        filter_packaged (bool): Remove "Pre-packaged Job Solutions".
                                These usually have words like 'Solution' or are multi-assessment bundles.

    Returns:
        List[Dict]: List of assessments with {assessment_name, assessment_url}.
    """

    results = retriever.retrieve(query=query, k=top_k)

    recommendations = []
    for r in results:
        name = r["metadata"].get("assessment_name", "")
        url = r["metadata"].get("url", "")

        if not name or not url:
            continue

        # Optional: filter pre-packaged job solutions
        if filter_packaged:
            # If the name includes "Solution" → exclude
            if "solution" in name.lower():
                continue

        recommendations.append({
            "assessment_name": name,
            "assessment_url": url
        })

    # Ensure minimum results (fallback: allow packaged if needed)
    if len(recommendations) < min_results:
        # re-add packaged solutions to fill gaps
        for r in results:
            name = r["metadata"].get("assessment_name", "")
            url = r["metadata"].get("url", "")
            if {"assessment_name": name, "assessment_url": url} not in recommendations:
                recommendations.append({
                    "assessment_name": name,
                    "assessment_url": url
                })
            if len(recommendations) >= min_results:
                break

    # respect maximum k
    return recommendations[:top_k]
