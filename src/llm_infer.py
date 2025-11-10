from src.retrive import Retriever
from langchain_google_genai import ChatGoogleGenerativeAI

def shl_rag(query: str, retriever: Retriever, llm: ChatGoogleGenerativeAI, top_k: int = 5):
    results = retriever.retrieve(query=query, k=top_k)
    context_blocks = []
    for r in results:
        name = r["metadata"].get("assessment_name", "")
        url  = r["metadata"].get("url", "")
        text = r["document"]

        block = f"""
                Assessment Name: {name}
                URL: {url}

                {text}
        """
        context_blocks.append(block.strip())

    context = "\n\n---\n\n".join(context_blocks)

    if not context:
        return "No relevant SHL assessment found."

    template = """
                You are an expert assistant answering questions about SHL assessments.

                Use ONLY the provided context. Do NOT hallucinate.
                If the answer is not in the context, say:
                "The dataset does not contain this information."

                Your answer MUST include:
                - Assessment name
                - Assessment URL
                - Suggest a minimum of 5 (max {top_k}) assessments when possible.

                Context:
                {context}

                Question:
                {query}

                Answer (include assessment names and URLs):
            """

    response = llm.invoke([template.format(context=context, query=query, top_k=top_k)])
    return response.content
