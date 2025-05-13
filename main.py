import os
import requests
import chainlit as cl
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="👋 Hello! I'm Megabot. Ask me anything.").send()

@cl.on_message
async def on_message(message: cl.Message):
    prompt = message.content

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(GEMINI_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        text = result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        text = f"❌ Error: {str(e)}"

    await cl.Message(content=text).send()
