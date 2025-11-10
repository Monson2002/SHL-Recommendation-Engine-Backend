from src.retrive import Retriever
from langchain_google_genai import ChatGoogleGenerativeAI

def shl_rag(query: str, retriever: Retriever, llm: ChatGoogleGenerativeAI, top_k: int = 5):
    results = retriever.retrieve(query=query, k=top_k)
    context = "\n\n".join([i['document'] for i in results])

    if not context:
        return "No relevant SHL assessment found."

    template = """
            You are an expert assistant answering questions about SHL assessments.
            Use the provided context to answer accurately. Do NOT hallucinate.
            If the answer is not in the context, say "The dataset does not contain this information."

            Keep the answer concise and factual.

            Context:
            {context}

            Question:
            {query}

            Answer:
    """

    response = llm.invoke([template.format(context=context, query=query)])
    return response.content
