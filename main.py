import os
import requests
import chainlit as cl
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get the API key from environment
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("❌ API_KEY not found. Make sure your .env file contains GEMINI_API_KEY.")

# Correct Gemini Pro endpoint
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro-exp-03-25:generateContent?key={API_KEY}"

# Start of chat session
@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="👋 Hello! I'm Megabot powered by Gemini Pro. Ask me anything!").send()

# On user message
@cl.on_message
async def on_message(message: cl.Message):
    prompt = message.content

    # Format request payload
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
        # Make request to Gemini API
        response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        # Extract response text
        text = result["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        # Handle errors
        text = f"❌ Error: {str(e)}"

    # Send reply to user
    await cl.Message(content=text).send()
