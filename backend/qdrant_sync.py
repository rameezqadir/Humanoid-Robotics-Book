import os
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
from uuid import uuid4
from dotenv import load_dotenv
load_dotenv()

openai = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
qclient = QdrantClient(url=os.environ.get("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"))

COLLECTION = os.environ.get("QDRANT_COLLECTION", "physical_ai_docs")

def ensure_collection():
    existing = qclient.get_collections().collections
    names = [c.name for c in existing]
    if COLLECTION not in names:
        qclient.recreate_collection(
            collection_name=COLLECTION,
            vectors_config=rest.VectorParams(size=1536, distance=rest.Distance.COSINE)
        )

def embed_text(text: str):
    r = openai.embeddings.create(model=os.environ.get("EMBED_MODEL","text-embedding-3-small"), input=text)
    return r.data[0].embedding

def chunk_text(text, chunk_size=800, overlap=100):
    words = text.split()
    chunks=[]
    i=0
    while i < len(words):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def upsert_doc(doc_id: str, title: str, text: str):
    ensure_collection()
    chunks = chunk_text(text, chunk_size=250, overlap=30)
    payloads=[]
    vectors=[]
    ids=[]
    for idx, chunk in enumerate(chunks):
        emb = embed_text(chunk)
        uid = f"{doc_id}_{idx}_{uuid4().hex[:6]}"
        ids.append(uid)
        vectors.append(emb)
        payloads.append({"doc_id": doc_id, "title": title, "chunk": chunk, "chunk_index": idx})
    qclient.upsert(collection_name=COLLECTION, points=rest.Batch.create(points=[
        rest.PointStruct(id=ids[i], vector=vectors[i], payload=payloads[i]) for i in range(len(ids))
    ]))
    return len(chunks)
