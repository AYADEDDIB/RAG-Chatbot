# rag.py — Le cerveau RAG du chatbot (version Gemini gratuite)

import os
from dotenv import load_dotenv

# Pour lire les PDFs
from langchain_community.document_loaders import PyPDFLoader

# Pour découper les documents en chunks
from langchain_text_splitters import RecursiveCharacterTextSplitter
# Pour créer les vecteurs (embeddings) — GEMINI GRATUIT
from langchain_community.embeddings import HuggingFaceEmbeddings
# Pour stocker et chercher les vecteurs
from langchain_community.vectorstores import FAISS

# Pour appeler le LLM (Gemini) — GRATUIT
from langchain_groq import ChatGroq
# Pour construire le pipeline RAG
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Charger la clé API depuis le fichier .env
load_dotenv()


class RAGChatbot:
    """Chatbot RAG : cherche dans les documents puis répond."""

    def __init__(self, docs_folder="documents"):
        self.docs_folder = docs_folder
        self.vector_store = None
        self.qa_chain = None

    def load_documents(self):
        """Étape 1 : Lire tous les PDFs du dossier."""
        documents = []

        for filename in os.listdir(self.docs_folder):
            if filename.endswith(".pdf"):
                filepath = os.path.join(self.docs_folder, filename)
                loader = PyPDFLoader(filepath)
                documents.extend(loader.load())
                print(f"✓ Chargé : {filename}")

        print(f"\n→ {len(documents)} pages chargées au total")
        return documents

    def create_vector_store(self, documents):
        """Étape 2 : Découper en chunks et vectoriser."""

        # Découper les documents en morceaux de 500 caractères
        # avec un chevauchement de 50 pour ne pas couper les phrases
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = splitter.split_documents(documents)
        print(f"→ {len(chunks)} chunks créés")

        # Transformer chaque chunk en vecteur avec Gemini (GRATUIT)
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
    
        self.vector_store = FAISS.from_documents(chunks, embeddings)
        print("→ Base vectorielle FAISS créée ✓")

    def setup_qa_chain(self):
        """Étape 3 : Configurer le pipeline question-réponse."""

        # Le prompt qui dit au LLM comment répondre
        prompt_template = """Tu es un assistant intelligent.
Utilise UNIQUEMENT le contexte ci-dessous pour répondre.
Si tu ne trouves pas la réponse dans le contexte, dis-le honnêtement.
Réponds en français.

Contexte :
{context}

Question : {question}

Réponse :"""

        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )

        # Le LLM — Gemini 2.0 Flash (GRATUIT et rapide)
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.3
        )

        # Assembler le pipeline : retriever + LLM
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(
                search_kwargs={"k": 3}  # récupère 3 chunks pertinents
            ),
            chain_type_kwargs={"prompt": prompt},
            return_source_documents=True
        )
        print("→ Pipeline RAG prêt ✓\n")

    def initialize(self):
        """Lance tout le pipeline de préparation."""
        print("=" * 40)
        print("Initialisation du RAG Chatbot")
        print("=" * 40)

        documents = self.load_documents()
        if not documents:
            print("⚠ Aucun PDF trouvé dans le dossier documents/")
            return False

        self.create_vector_store(documents)
        self.setup_qa_chain()
        return True

    def ask(self, question):
        """Pose une question et retourne la réponse."""
        if not self.qa_chain:
            return {"answer": "Le chatbot n'est pas initialisé.", "sources": []}

        result = self.qa_chain.invoke({"query": question})

        # Extraire les sources
        sources = []
        for doc in result.get("source_documents", []):
            source = doc.metadata.get("source", "inconnu")
            page = doc.metadata.get("page", "?")
            sources.append(f"{os.path.basename(source)} (page {page + 1})")

        return {
            "answer": result["result"],
            "sources": list(set(sources))
        }


# Test rapide dans le terminal
if __name__ == "__main__":
    bot = RAGChatbot()
    if bot.initialize():
        while True:
            q = input("\n💬 Ta question (ou 'quit') : ")
            if q.lower() == "quit":
                break
            result = bot.ask(q)
            print(f"\n🤖 {result['answer']}")
            print(f"📄 Sources : {', '.join(result['sources'])}")