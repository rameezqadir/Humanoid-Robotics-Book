---
title: AI Assistant Demo
sidebar_position: 2
---

# AI Assistant Demo  
**Retrieval-Augmented Learning for Physical AI & Humanoid Robotics**

This project includes an **AI-powered assistant** that can answer questions directly from the *Humanoid Robotics Book* using a **Retrieval-Augmented Generation (RAG)** pipeline.

---

## 🎯 Purpose

The AI assistant is designed to:

- Help students query complex robotics concepts
- Retrieve precise explanations from the book
- Assist researchers with fast knowledge access
- Demonstrate AI-native learning for Physical AI

---

## 🧠 How It Works (Architecture)

1. **Book Content Ingestion**
   - All chapters are converted into semantic embeddings
   - Stored inside a **Qdrant vector database**

2. **User Question**
   - User asks a natural language question
   - Example: *“Explain kinematics in humanoid robots”*

3. **Retrieval (RAG)**
   - Relevant book sections are retrieved
   - Only trusted textbook content is used

4. **Answer Generation**
   - LLM generates a grounded response
   - Citations come from book chapters

---

## 🧩 Technology Stack

- **LLM**: Claude / GPT-compatible models  
- **Vector DB**: Qdrant  
- **Backend**: FastAPI (Python)  
- **Frontend**: Docusaurus (this book)  

---

## 💬 Example Questions

- What is Physical AI?
- Explain humanoid robot kinematics
- How does Isaac Sim support robotics?
- Difference between ROS2 and URDF
- What is Vision-Language-Action (VLA)?

---

## 🧪 Demo Flow (Conceptual)

```text
User Question
      ↓
Embedding Search (Qdrant)
      ↓
Relevant Book Sections
      ↓
LLM Answer (Grounded)
