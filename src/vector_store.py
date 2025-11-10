import os
import uuid
import chromadb
import numpy as np

from typing import List, Any

class VectorStore:
    def __init__(self, collection_name: str, persist_dir: str='./Data/RAG/vector_store'):
        self.collection_name = collection_name
        self.persist_dir = persist_dir
        self.client = None
        self.collection = None
        self._initialize_store()

    def _initialize_store(self):
        try:
            os.makedirs(self.persist_dir, exist_ok=True)
            self.client = chromadb.PersistentClient(path=self.persist_dir)

            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={'hnsw:space': 'cosine'}
            )
            print(f'VectorStore for {self.collection_name} initialized successfully')
            print(f'Existing numner of docs in the colelction: {self.collection.count()}')
        
        except Exception as e:
            print(f'Error in initializing Vector Store {e}')
            raise 

    def add_docs(self, docs: List[Any], embeddings: np.ndarray):
        if len(docs) != len(embeddings):
            raise ValueError(f'Number of docs ({len(docs)}) must match number of embeddings ({len(embeddings)})...')
        
        print(f'Adding {len(docs)} docs to vectorStore')
    
        ids = []
        metadatas = []
        doc_list = []
        embedding_list = []
        for i, (doc, embedding) in enumerate(zip(docs, embeddings)):
            id = f'doc_{uuid.uuid4().hex[:8]}_{i}'
            ids.append(id)

            doc_list.append(doc.page_content)
            
            embedding_list.append(embedding)
            
            metadata = dict(doc.metadata)
            metadata['doc_index'] = i
            metadata['context_length'] = len(doc.page_content)
            metadatas.append(metadata)

        try:
            print(f'Adding docs and embeddings to collection {self.collection_name}')
            self.collection.add(
                ids=ids,
                embeddings=embedding_list,
                metadatas=metadatas,
                documents=doc_list
            )
            print(f'Successfuly added {len(docs)} documents and embeddings to the collection.')
            print(f'Total docs and embeddings in {self.collection_name} is {self.collection.count()}')
        
        except Exception as e:
            raise ValueError(f'Could not add docs and embeds to collection {self.collection_name}')
        