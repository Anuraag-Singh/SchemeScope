from pathlib import Path
from .config import CHROMA, DOCS, MODEL, TOP_K
from .corpus import load_documents

class Index:
    def __init__(self):
        from fastembed import TextEmbedding
        import chromadb
        self.embedder=TextEmbedding(model_name=MODEL)
        self.client=chromadb.PersistentClient(path=str(CHROMA))
        self.collection=self.client.get_or_create_collection("scheme_facts", metadata={"hnsw:space":"cosine"})
        if self.collection.count()==0:
            self.build()
    def build(self):
        chunks=load_documents(DOCS)
        texts=[f"{c.scheme} {c.section}: {c.text}" for c in chunks]
        vecs=list(self.embedder.embed(texts))
        self.collection.upsert(ids=[c.id for c in chunks], embeddings=[v.tolist() for v in vecs], documents=texts, metadatas=[{"scheme":c.scheme,"section":c.section,"source_url":c.source_url,"updated":c.updated} for c in chunks])
    def search(self,q):
        qv=next(self.embedder.embed([q])).tolist()
        r=self.collection.query(query_embeddings=[qv], n_results=TOP_K, include=["documents","metadatas","distances"])
        out=[]
        from .models import Chunk, Hit
        for doc,meta,dist in zip(r["documents"][0],r["metadatas"][0],r["distances"][0]):
            score=1-float(dist)
            out.append(Hit(Chunk("",meta["scheme"],meta["section"],doc.split(": ",1)[-1],meta["source_url"],meta["updated"]),score))
        return out
