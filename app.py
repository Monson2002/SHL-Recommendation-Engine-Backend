import numpy as np

from dotenv import load_dotenv
from src.dataloader import load_data
from src.embedding import EmbeddingManager
from src.vector_store import VectorStore
from src.retrive import Retriever               
# from src.llm_infer import shl_rag  
from src.recommend_tests import recommend_tests
# from langchain_google_genai import ChatGoogleGenerativeAI

docs = load_data("Data/RAG")
print(f'\nLength of docs found: {len(docs)}')

# NOTE: since I am treating one docs as a chunk, (design decision) chunk_size and chunk_overlap dont have an effect here 
embedder = EmbeddingManager(model_name="all-MiniLM-L6-v2", chunk_size=400, chunk_overlap=0)

# chunks = embedder.split_docs(docs)
# print("\nChunks:", len(chunks))

# texts = [c.page_content for c in chunks]
texts = [d.page_content for d in docs]
embeddings = embedder.generate_embeddings(texts)

store = VectorStore(collection_name="shl_assessments", persist_dir='./Data/RAG/vector_store')

if store.count() == 0:
    store.add_docs(
        # docs=chunks,
        docs=docs,
        embeddings=np.array(embeddings)
    )
    print("\nNew embeddings. Adding to VectorStore.")
else:
    print("\nVector store already contains embeddings. Skipping add.\n")

retriever = Retriever(vector_store=store, embedding_manager=embedder)

# load_dotenv()
# llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

question = "Suggest me some data entry test that measures the ability to process receivables and invoices\n"
# llm_ans = shl_rag(question, retriever, llm, 10)
# print(f'\n{llm_ans}\n')

results = recommend_tests(question, retriever, top_k=10)

for i, r in enumerate(results, 1):
    name = r.get("name") or r.get("assessment_name")
    url  = r.get("url")  or r.get("assessment_url")
    print(f"{i}. {name} — {url}")