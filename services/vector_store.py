import faiss
import numpy as np
import os
from config import VECTOR_DB_PATH


class VectorStore:
    def __init__(self, dim=1536):
        self.dim = dim
        if os.path.exists(VECTOR_DB_PATH):
            self.index = faiss.read_index(VECTOR_DB_PATH)
        else:
            self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

    def add(self, vector, payload):
        v = np.array([vector]).astype("float32")
        self.index.add(v)
        self.metadata.append(payload)
        faiss.write_index(self.index, VECTOR_DB_PATH)

    def search(self, vector, k=5):
        v = np.array([vector]).astype("float32")
        d, i = self.index.search(v, k)
        return [self.metadata[idx] for idx in i[0] if idx < len(self.metadata)]