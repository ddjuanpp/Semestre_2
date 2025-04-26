# faiss_manager.py

import faiss
import numpy as np
import cohere
import os
from dotenv import load_dotenv

class FAISSManager:
    def __init__(self, api_key):
        self.api_key = api_key
        self.cohere_client = cohere.Client(api_key)
        self.index = None
        self.chunks = []
        self.dim = None

    def chunk_text(self, text, max_length=2048):
        chunks = []
        start = 0
        while start < len(text):
            end = start + max_length
            chunk = text[start:end]
            chunks.append(chunk)
            start = end
        return chunks

    def generate_embeddings(self, texts):
        response = self.cohere_client.embed(
            texts=texts,
            model="embed-multilingual-v3.0",
            input_type="search_document"
        )
        if not response.embeddings:
            raise Exception(f"Error al obtener embeddings: {response}")
        return np.array(response.embeddings, dtype=np.float32)

    def create_faiss_index(self, docs):
        # 1) Partir documentos en chunks
        all_chunks = []
        for doc in docs:
            doc_chunks = self.chunk_text(doc, max_length=2048)
            all_chunks.extend(doc_chunks)
        self.chunks = all_chunks

        # 2) Generar embeddings por lotes
        embeddings = []
        batch_size = 16
        for i in range(0, len(all_chunks), batch_size):
            batch = all_chunks[i:i+batch_size]
            emb_batch = self.generate_embeddings(batch)
            embeddings.append(emb_batch)

        if not embeddings:
            return

        embeddings = np.concatenate(embeddings, axis=0)
        self.dim = embeddings.shape[1]

        # 3) Crear el índice FAISS
        self.index = faiss.IndexFlatIP(self.dim)
        faiss.normalize_L2(embeddings)
        self.index.add(embeddings)

    def search_similar_chunks(self, query, k=2):
        """
        Dado un query en texto, retorna los k chunks más similares del índice FAISS.
        """
        # Generar embedding del query
        query_emb = self.generate_embeddings([query])
        faiss.normalize_L2(query_emb)

        # Hacer búsqueda en FAISS
        distances, indices = self.index.search(query_emb, k)

        # Obtener los chunks correspondientes a los índices
        top_chunks = []
        for idx in indices[0]:
            top_chunks.append(self.chunks[idx])

        return top_chunks
