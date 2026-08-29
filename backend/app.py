import os
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from huggingface_hub import InferenceClient

# C'est cette variable "app" que Render / Uvicorn cherche
app = FastAPI(title="Salam AI Backend API")

HF_TOKEN = os.getenv("HF_TOKEN")
# Ton propre dépôt Hugging Face :
MODEL_ID = "Abdoul0/mistral-7b-français-gguf"

client = InferenceClient(model=MODEL_ID, token=HF_TOKEN)

class Message(BaseModel):
    role: str
    content: str

class ChatPayload(BaseModel):
    messages: List[Message]

@app.get("/")
def root():
    return {"status": "ok", "message": "Backend Salam AI (Mistral-7B Français) opérationnel"}

@app.post("/api/chat")
def chat_endpoint(payload: ChatPayload):
    try:
        formatted_messages = [{"role": msg.role, "content": msg.content} for msg in payload.messages]
        
        response = client.chat_completion(
            messages=formatted_messages,
            max_tokens=512,
            temperature=0.7
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))