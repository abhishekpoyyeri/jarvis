import ollama

SYSTEM_PROMPT = """
You are JARVIS.
You are calm, concise, intelligent, and precise.
Respond naturally like an assistant.
"""

conversation_memory = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

def ask_jarvis(user_text: str) -> dict:
    """
    Returns:
    {
      "type": "command" | "chat",
      "text": assistant_reply
    }
    """

    conversation_memory.append({
        "role": "user",
        "content": user_text
    })

    response = ollama.chat(
        model="llama3:8b",
        messages=conversation_memory
    )

    reply = response["message"]["content"].strip()

    conversation_memory.append({
        "role": "assistant",
        "content": reply
    })

    return {
        "type": "chat",
        "text": reply
    }
