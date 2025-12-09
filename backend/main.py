import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from qdrant_client import QdrantClient
from openai import OpenAI
from dotenv import load_dotenv
from typing import Optional
from qdrant_sync import upsert_doc, embed_text
load_dotenv()

app = FastAPI(title="PhysicalAI RAG Backend")
qclient = QdrantClient(url=os.environ.get("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"))
openai = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
COLLECTION = os.environ.get("QDRANT_COLLECTION", "physical_ai_docs")

class DocIn(BaseModel):
    doc_id: str
    title: str
    text: str

class QueryIn(BaseModel):
    question: str
    selected_text: Optional[str] = None
    top_k: int = 4

@app.post("/ingest")
async def ingest(doc: DocIn):
    try:
        count = upsert_doc(doc.doc_id, doc.title, doc.text)
        return {"status":"ok","chunks_upserted": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/answer")
async def answer(q: QueryIn):
    if q.selected_text:
        ctx = q.selected_text
        prompt = f"Use the following user-selected text as the only source. Answer the question concisely. If the answer isn't present, say 'Not found in selected text'.\n\nSelected text:\n{ctx}\n\nQuestion: {q.question}\n\nAnswer:"
        resp = openai.chat.completions.create(model=os.environ.get("OPENAI_CHAT_MODEL"), messages=[{"role":"user","content":prompt}], max_tokens=512)
        return {"answer":resp.choices[0].message.content, "source":"selected_text"}
    query_emb = embed_text(q.question)
    hits = qclient.search(collection_name=COLLECTION, query_vector=query_emb, limit=q.top_k)
    contexts = [h.payload.get("chunk") for h in hits]
    source_meta = [{"doc_id": h.payload.get("doc_id"), "title":h.payload.get("title")} for h in hits]
    prompt = "You are an assistant answering from provided context. Use only the context to answer.\n\n"
    for i,c in enumerate(contexts):
        prompt += f"Context {i+1}:\n{c}\n\n"
    prompt += f"Question: {q.question}\nAnswer concisely and cite which context chunk you used."
    resp = openai.chat.completions.create(model=os.environ.get("OPENAI_CHAT_MODEL"), messages=[{"role":"user","content":prompt}], max_tokens=512)
    return {"answer": resp.choices[0].message.content, "sources": source_meta}
