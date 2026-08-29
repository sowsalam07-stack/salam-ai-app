import os
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from huggingface_hub import InferenceClient

app = FastAPI(title="Salam AI Backend API")

# Récupération du token Hugging Face configuré sur Render
HF_TOKEN = os.getenv("HF_TOKEN")

# Identifiant de ton modèle personnalisé expédié au format Safetensors
MODEL_ID = "Abdoul0/mistral-7b-francais"

# Initialisation du client d'inférence avec ton token Read
if HF_TOKEN:
    client = InferenceClient(model=MODEL_ID, token=HF_TOKEN)
else:
    client = InferenceClient(model=MODEL_ID)

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