const chat = document.getElementById("chat");
const status = document.getElementById("status");
const input = document.getElementById("input");

function addMessage(text, cls) {
  const div = document.createElement("div");
  div.classList.add("msg", cls);
  div.textContent = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

async function send() {
  const text = input.value.trim();
  if (!text) return;

  addMessage(text, "user");
  input.value = "";
  status.innerText = "THINKING";

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });

    const data = await res.json();
    addMessage(data.reply, "jarvis");

    status.innerText = "SPEAKING";
    const audio = new Audio(data.audio);

    audio.onended = () => {
      status.innerText = "IDLE";
    };

    audio.onerror = () => {
      status.innerText = "IDLE";
    };

    await audio.play();

  } catch (e) {
    console.error(e);
    status.innerText = "IDLE";
  }
}

function startListening() {
  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    alert("Speech recognition not supported");
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.lang = "en-US";
  status.innerText = "LISTENING";
  recognition.start();

  recognition.onresult = (event) => {
    input.value = event.results[0][0].transcript;
    status.innerText = "IDLE";
    send();
  };

  recognition.onerror = () => {
    status.innerText = "IDLE";
  };
}
