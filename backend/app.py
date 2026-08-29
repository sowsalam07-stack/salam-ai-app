import os
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from huggingface_hub import InferenceClient

app = FastAPI(title="Salam AI Backend API")

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_ID = "Abdoul0/mistral-7b-francais"

# Configuration du client Hugging Face
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
        # Conversion du format de messages pour l'InferenceClient
        formatted_messages = [{"role": msg.role, "content": msg.content} for msg in payload.messages]
        
        # Appel via chat_completion
        response = client.chat_completion(
            messages=formatted_messages,
            max_tokens=512,
            temperature=0.7
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        # Si chat_completion est en attente de chargement du modèle (Warmup)
        try:
            # Fallback direct en génération de texte
            user_prompt = payload.messages[-1].content
            prompt = f"<s>[INST] {user_prompt} [/INST]"
            res = client.text_generation(prompt, max_new_tokens=512, temperature=0.7)
            return {"response": res}
        except Exception as inner_e:
            raise HTTPException(status_code=500, detail=str(e))