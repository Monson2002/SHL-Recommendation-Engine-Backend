from typing import List
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

class EmbeddingManager:
    # model_name is the Hugggingface one
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2', chunk_size: int = 500, chunk_overlap: int = 200):
        # all-MiniLM-L6-v2 : 384 dim
        self.model_name = model_name
        self.model = None
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self._load_model()

    def _load_model(self):
        try:
            print(f'Loading model: {self.model_name}')
            self.model = SentenceTransformer(self.model_name)
            print(f'Loaded model: {self.model.get_sentence_embedding_dimension()} dimensional')
        except Exception as e:
            print(f'Error loading model {self.model_name}, {e}')
            raise

    def split_docs(self, docs):
        enriched_docs = []
        for doc in docs:
            meta = doc.metadata
            content = doc.page_content

            # Try to enrich with author/title if available
            title = meta.get("title", "")
            authors = meta.get("authors", "")
            if title or authors:
                enriched_text = f"Title: {title}\nAuthors: {authors}\n\n{content}"
            else:
                enriched_text = content

            doc.page_content = enriched_text
            enriched_docs.append(doc)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=['\n\n', ' ', '\n', '']
        )

        all_chunks = text_splitter.split_documents(enriched_docs)
        print(f"Formed {len(all_chunks)} chunks from {len(docs)} docs")
        return all_chunks

    def generate_embeddings(self, chunks: List[str]):
        if not self.model:
            raise ValueError('Model not loaded !!!')
        print(f'Generating embeddings for {self.model_name}')
        embeddings = self.model.encode(chunks)
        print(f'Generated (with shape) {embeddings.shape} dimensional embeddings')
        return embeddings.tolist()

    def get_sentence_embedding_dimension(self):
        if not self.model:
            raise ValueError('Model not loaded !!!')
        return self.model.get_sentence_embedding_dimension()