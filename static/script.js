async function sendMessage() {
  const input = document.getElementById("input");
  const chat = document.getElementById("chat");
  const question = input.value.trim();

  if (!question) return;

  // Afficher la question de l'utilisateur
  chat.innerHTML += `
    <div class="message user">
      <div class="bubble">${question}</div>
    </div>`;

  input.value = "";
  input.disabled = true;

  // Afficher "en train d'écrire..."
  chat.innerHTML += `
    <div class="message bot typing" id="typing">
      <div class="bubble">Recherche en cours...</div>
    </div>`;

  chat.scrollTop = chat.scrollHeight;

  try {
    // Appeler l'API Flask
    const response = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: question })
    });

    const data = await response.json();

    // Supprimer le "typing"
    document.getElementById("typing").remove();

    // Afficher la réponse
    const sourcesHtml = data.sources.length
      ? `<div class="sources">📄 ${data.sources.join(", ")}</div>`
      : "";

    chat.innerHTML += `
      <div class="message bot">
        <div class="bubble">${data.answer}</div>
        ${sourcesHtml}
      </div>`;

  } catch (error) {
    document.getElementById("typing").remove();
    chat.innerHTML += `
      <div class="message bot">
        <div class="bubble">Erreur de connexion. Vérifie que le serveur tourne.</div>
      </div>`;
  }

  input.disabled = false;
  input.focus();
  chat.scrollTop = chat.scrollHeight;
}