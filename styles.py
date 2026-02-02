import streamlit as st

def apply_global_styles():
    st.markdown("""
        <style>
        /* Import de la police futuriste */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

        /* Fond dégradé immersif */
        .stApp {
            background: linear-gradient(135deg, #0f1923 0%, #080c10 100%);
        }

        /* Titre CRIMSON HQ avec effet de lueur pulsante */
        .valo-title {
            font-family: 'Orbitron', sans-serif;
            color: #ff4655;
            text-align: center;
            font-size: 4rem;
            font-weight: 900;
            letter-spacing: 7px;
            text-shadow: 0 0 30px rgba(255, 70, 85, 0.6);
            margin-bottom: 50px;
            animation: pulseGlow 3s infinite alternate;
        }

        @keyframes pulseGlow {
            from { text-shadow: 0 0 20px rgba(255, 70, 85, 0.4); }
            to { text-shadow: 0 0 50px rgba(255, 70, 85, 0.8); }
        }

        /* Boutons de menu stylisés */
        div.stButton > button {
            background: rgba(255, 255, 255, 0.05) !important;
            color: #ece8e1 !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 0px !important;
            font-family: 'Orbitron', sans-serif !important;
            transition: all 0.3s ease !important;
        }

        div.stButton > button:hover {
            background: #ff4655 !important;
            color: white !important;
            box-shadow: 0 0 20px rgba(255, 70, 85, 0.5);
            transform: translateY(-3px);
        }
        </style>
    """, unsafe_allow_html=True)

def apply_immersive_mode():
    st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>", unsafe_allow_html=True)
