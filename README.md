# 🤖 RAG Chatbot

Chatbot intelligent qui répond à vos questions à partir de vos documents PDF,
grâce à une architecture RAG (Retrieval-Augmented Generation).

## Architecture

1. **Ingestion** : Les PDFs sont découpés en chunks et vectorisés
2. **Recherche** : FAISS trouve les passages les plus pertinents
3. **Génération** : GPT-4o-mini génère une réponse basée sur les sources

## Stack technique

- **Python** — Backend
- **LangChain** — Orchestration du pipeline RAG
- **FAISS** — Base vectorielle (recherche sémantique)
- **OpenAI** — Embeddings + LLM (GPT-4o-mini)
- **Flask** — Serveur web
- **HTML/CSS/JS** — Interface chat

## Installation

```bash
git clone https://github.com/TON-USERNAME/rag-chatbot.git
cd rag-chatbot
pip install -r requirements.txt
```

Crée un fichier `.env` :
```
OPENAI_API_KEY=ta-cle-ici
```

Ajoute tes PDFs dans le dossier `documents/`.

## Lancer

```bash
python app.py
```

Ouvre http://localhost:5000

## Comment ça marche

Le chatbot utilise le pattern RAG :
- Les documents sont transformés en vecteurs (embeddings OpenAI)
- À chaque question, FAISS cherche les passages les plus similaires
- Ces passages sont donnés comme contexte au LLM
- Le LLM répond uniquement à partir des sources (pas d'hallucination)
