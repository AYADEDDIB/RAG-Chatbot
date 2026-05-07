import streamlit as st
from rag import RAGChatbot

st.set_page_config(page_title="RAG Chatbot", page_icon="🤖")
st.title("🤖 RAG Chatbot")

# Initialiser le chatbot une seule fois
@st.cache_resource
def get_bot():
    bot = RAGChatbot()
    bot.initialize()
    return bot

bot = get_bot()

# Historique des messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Afficher l'historique
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input utilisateur
if question := st.chat_input("Pose ta question..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Recherche en cours..."):
            result = bot.ask(question)
        st.write(result["answer"])
        st.caption(f"📄 Sources : {', '.join(result['sources'])}")

    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"]
    })