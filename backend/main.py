from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uuid
import os
import pyttsx3

from ai_brain import ask_jarvis
from tools import open_app, shutdown, restart

# ---------------- APP ----------------
app = FastAPI(title="JARVIS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- PATHS ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

os.makedirs(AUDIO_DIR, exist_ok=True)

# ---------------- STATIC FILES ----------------
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")
app.mount("/audio", StaticFiles(directory=AUDIO_DIR), name="audio")

# ---------------- DATA MODEL ----------------
class Query(BaseModel):
    text: str

# ---------------- SAFE TTS ----------------
def speak_to_file(text: str, path: str):
    engine = pyttsx3.init(driverName="sapi5")
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)
    engine.setProperty("rate", 165)
    engine.save_to_file(text, path)
    engine.runAndWait()
    engine.stop()

# ---------------- COMMAND DETECTION ----------------
def detect_command(user_text: str):
    text = user_text.lower()

    if "open" in text:
        if "chrome" in text:
            return ("open_app", "chrome")
        if "notepad" in text:
            return ("open_app", "notepad")
        if "calculator" in text or "calc" in text:
            return ("open_app", "calculator")
        if "vs code" in text or "vscode" in text:
            return ("open_app", "vs code")

    if "shutdown" in text:
        return ("shutdown", None)

    if "restart" in text:
        return ("restart", None)

    return (None, None)

# ---------------- CHAT ENDPOINT ----------------
@app.post("/chat")
def chat(query: Query):
    user_text = query.text

    # 1️⃣ Detect system command
    action, target = detect_command(user_text)

    if action == "open_app":
        reply = open_app(target)

    elif action == "shutdown":
        reply = shutdown(False)

    elif action == "restart":
        reply = restart(False)

    else:
        # 2️⃣ Normal AI conversation (with memory)
        result = ask_jarvis(user_text)
        reply = result["text"]

    # 3️⃣ Speak reply
    file_id = str(uuid.uuid4())
    audio_path = os.path.join(AUDIO_DIR, f"{file_id}.wav")
    speak_to_file(reply, audio_path)

    return {
        "reply": reply,
        "audio": f"/audio/{file_id}.wav"
    }

# ---------------- ROOT ----------------
@app.get("/")
def root():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))
