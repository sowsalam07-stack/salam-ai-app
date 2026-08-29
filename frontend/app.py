import os
import requests
import streamlit as st

# ---------------------------------------------------------
# Configuration de la page Streamlit
# ---------------------------------------------------------
st.set_page_config(
    page_title="Salam AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# URL du backend FastAPI (locale par défaut, remplacée automatiquement sur Render)
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# ---------------------------------------------------------
# Design personnalisé (Haute lisibilité + Alignements)
# ---------------------------------------------------------
CUSTOM_CSS = """
<style>
    /* Application et arrière-plan général */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #0b0b0e !important;
        color: #ffffff !important;
    }
    #MainMenu, footer, header { visibility: hidden; }

    /* Suppression de la bande blanche en bas */
    [data-testid="stBottom"], [data-testid="stBottom"] > div, footer {
        background-color: #0b0b0e !important;
        border-top: none !important;
    }

    /* En-tête */
    .salam-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 10px 16px 10px;
        border-bottom: 0.5px solid #1a1a22;
        margin-bottom: 30px;
    }
    .salam-header .left-side {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .salam-header .logo {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: #3C3489;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        color: #EEEDFE;
    }
    .salam-header .title {
        font-size: 18px;
        font-weight: 600;
        color: #ffffff;
    }

    /* Hero section / Accueil */
    .salam-hero {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        margin-top: 40px;
        margin-bottom: 30px;
    }
    .salam-hero .icon-box {
        width: 64px;
        height: 64px;
        border-radius: 20px;
        background: #15151c;
        border: 1px solid #23232f;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        color: #7F77DD;
        margin-bottom: 20px;
    }
    .salam-hero .greet {
        font-size: 26px;
        font-weight: 700;
        color: #ffffff;
        margin: 0 0 8px 0;
    }
    .salam-hero .sub {
        font-size: 15px;
        color: #a0a0b0;
        margin: 0;
    }

    /* Style global du texte dans les messages */
    div[data-testid="stChatMessage"] * {
        color: #ffffff !important;
    }

    /* Bulle Utilisateur (à GAUCHE) */
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
        flex-direction: row !important;
        background-color: #1a1a24 !important;
        border: 1px solid #2e2e3e !important;
        border-radius: 14px !important;
        padding: 14px 18px !important;
        margin-right: auto !important;
        max-width: 70% !important;
        margin-bottom: 16px !important;
    }

    /* Bulle Assistant / Chatbot (à DROITE) */
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) {
        flex-direction: row-reverse !important;
        text-align: left !important;
        background-color: #26224e !important;
        border: 1px solid #4f46e5 !important;
        border-radius: 14px !important;
        padding: 14px 18px !important;
        margin-left: auto !important;
        max-width: 70% !important;
        margin-bottom: 16px !important;
    }

    /* Zone de saisie (Chat Input) */
    div.stChatInput {
        max-width: 850px !important;
        margin: 0 auto !important;
    }
    div[data-testid="stChatInput"], 
    div[data-testid="stChatInput"] > div,
    div[data-testid="stChatInput"] textarea {
        background-color: #15151c !important;
        color: #ffffff !important;
        border-color: #23232f !important;
    }
    div[data-testid="stChatInput"] {
        border: 1px solid #2e2e3e !important;
        border-radius: 16px !important;
    }
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #808095 !important;
    }
    div[data-testid="stChatInput"] button {
        background-color: transparent !important;
        color: #7F77DD !important;
        border: none !important;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------
# En-tête "Salam AI"
# ---------------------------------------------------------
st.markdown(
    """
    <div class="salam-header">
        <div class="left-side">
            <div class="logo">✨</div>
            <div class="title">Salam AI</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# Initialisation des variables d'état
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------------------------
# Vue initiale
# ---------------------------------------------------------
if not st.session_state.messages:
    st.markdown(
        """
        <div class="salam-hero">
            <div class="icon-box">✨</div>
            <h1 class="greet">Assalamu alaikum, Salam</h1>
            <p class="sub">Que puis-je faire pour toi aujourd'hui ?</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------------------------------------------------
# Affichage de l'historique de discussion
# ---------------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------------------------------------
# Saisie utilisateur & Requête vers le Backend
# ---------------------------------------------------------
prompt = st.chat_input("Écris un message à Salam AI...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        with st.spinner("Salam AI réfléchit..."):
            try:
                messages_api = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                
                # Appel HTTP POST au Backend FastAPI
                res = requests.post(
                    f"{BACKEND_URL}/api/chat",
                    json={"messages": messages_api},
                    timeout=60
                )
                
                if res.status_code == 200:
                    full_response = res.json().get("response", "Aucune réponse reçue.")
                else:
                    full_response = f"Erreur backend ({res.status_code}) : {res.text}"

            except Exception as e:
                full_response = f"Erreur de connexion au backend. Détails : {e}"

        response_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})