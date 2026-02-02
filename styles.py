import streamlit as st

def apply_global_styles():
    st.markdown("""
        <style>
        /* Import de la police Valorant (ou similaire via Google Fonts) */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

        /* Background global sombre avec texture */
        .stApp {
            background: radial-gradient(circle at top, #1f2326 0%, #0f1923 100%);
        }

        /* Titre Crimson avec effet de lueur */
        .valo-title {
            font-family: 'Orbitron', sans-serif;
            color: #ff4655;
            text-align: center;
            font-size: 3.5rem;
            font-weight: bold;
            letter-spacing: 5px;
            text-shadow: 0 0 20px rgba(255, 70, 85, 0.5);
            margin-bottom: 30px;
        }

        /* Boutons de navigation stylisés */
        div.stButton > button {
            background: rgba(255, 255, 255, 0.05) !important;
            color: #ece8e1 !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 0px !important; /* Look angulaire Valorant */
            transition: all 0.3s ease !important;
            font-family: 'Orbitron', sans-serif !important;
            text-transform: uppercase;
            font-size: 0.8rem !important;
        }

        div.stButton > button:hover {
            background: #ff4655 !important;
            color: white !important;
            border: 1px solid #ff4655 !important;
            box-shadow: 0 0 15px rgba(255, 70, 85, 0.4);
            transform: translateY(-2px);
        }

        /* Cartes et conteneurs */
        .stSelectbox, .stTextArea {
            background: rgba(15, 25, 35, 0.8);
            border-radius: 5px;
        }

        /* Barre de séparation rouge fine */
        hr {
            border: 0;
            height: 1px;
            background: linear-gradient(to right, transparent, #ff4655, transparent);
            margin: 20px 0;
        }
        </style>
    """, unsafe_allow_html=True)
