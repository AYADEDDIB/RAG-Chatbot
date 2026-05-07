from flask import Flask, render_template, request, jsonify
from rag import RAGChatbot

app = Flask(__name__)

# Initialiser le chatbot au démarrage
print("Chargement du chatbot...")
bot = RAGChatbot()
bot.initialize()
print("Chatbot prêt !")


@app.route("/")
def home():
    """Page principale."""
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    """API qui reçoit une question et retourne la réponse."""
    data = request.get_json()

    question = data.get("question", "")

    if not question:
        return jsonify({"error": "Pas de question"}), 400

    result = bot.ask(question)

    return jsonify({
        "answer": result["answer"],
        "sources": result["sources"]
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)