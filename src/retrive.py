from typing import List, Dict, Any
from src.vector_store import VectorStore
from src.embedding import EmbeddingManager

class Retriever:
    def __init__(self, vector_store: VectorStore, embedding_manager: EmbeddingManager):
        self.vector_store = vector_store
        self.embedding_manager = embedding_manager
    
    def retrieve(self, query: str, k: int = 5, score_threshold: float = 0.0) -> List[Dict[str, Any]]:
        # score_threshold: Minimum similarity score threshold
        
        print(f'Retrieving docs for query: {query}')
        print(f'Top k = {k} and score threshold {score_threshold}')

        query_embedding = self.embedding_manager.generate_embeddings([query])[0]
        # query_embedding = np.array(query_embedding)
        # query_embedding = query_embedding / np.linalg.norm(query_embedding, keepdims=True)
        
        try:
            results = self.vector_store.collection.query(
                query_embeddings=[query_embedding],
                n_results=k
            )

            retrieved_docs = []

            if results['documents'] and results['metadatas'] and results['distances'] and results['documents'][0]:
                documents = results['documents'][0]
                metadatas = results['metadatas'][0]
                distances = results['distances'][0]
                ids = results['ids'][0]

                for i, (id, document, metadata, distance) in enumerate(zip(ids, documents, metadatas, distances)):
                    similarity_score = 1 - distance
                    # print(i, similarity_score, distance)
                    if similarity_score > score_threshold:
                        retrieved_docs.append({
                            'id': id,
                            'document': document,
                            'metadata': metadata,
                            'similarity_score': similarity_score,
                            'distance': distance,
                            'rank': i+1
                        })
                print(f'Retrieved {len(retrieved_docs)} after filtering')
            else:
                print(f'No docs found --^^--')
            return retrieved_docs
        except Exception as e:
            raise ValueError(f'Could not retrieve documents : {e}')