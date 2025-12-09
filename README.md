# Physical AI & Humanoid Robotics — AI-Native Textbook

This repo contains a Spec-driven textbook for Physical AI & Humanoid Robotics built with Spec-Kit Plus, Claude Code and Docusaurus. Includes a Retrieval-Augmented Generation assistant.

## Quick Start (dev)
1. Start Qdrant: `docker run -p 6333:6333 qdrant/qdrant`
2. Activate backend venv, install deps and run:
   ```
   pip install -r backend/requirements.txt
   uvicorn backend.main:app --reload --port 8000
   ```
3. Build & run site:
   ```
   cd docs-site
   npm install
   npm start
   ```
4. Ingest docs: POST /ingest with doc content (see examples in scripts/README)

## Notes
- Replace keys in backend/.env
- Use `scripts/spec_to_md.py` to convert specs -> docs (CI step)
