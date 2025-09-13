async function sendMessage() {
  let userInput = document.getElementById("user-input");
  let message = userInput.value.trim();
  if (message === "") return;

  // Show user message
  let chatBox = document.getElementById("chat-box");
  chatBox.innerHTML += `<div class="user-message">You: ${message}</div>`;

  // Send to Flask backend
  let response = await fetch("/get", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({message: message})
  });

  let data = await response.json();

  // Show bot reply
  chatBox.innerHTML += `<div class="bot-message">Bot: ${data.reply}</div>`;

  // Scroll down
  chatBox.scrollTop = chatBox.scrollHeight;

  // Clear input
  userInput.value = "";
}