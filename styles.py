import streamlit as st

def apply_global_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.cdnfonts.com/css/valorant');
        @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&display=swap');
        /* Import de la police Valorant (ou similaire via Google Fonts) */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

        /* Background global sombre avec texture */
        .stApp {
            background-color: #0f1923;
            color: #ece8e1;
            font-family: 'Rajdhani', sans-serif;
            background: radial-gradient(circle at top, #1f2326 0%, #0f1923 100%);
        }

        /* Titre Crimson avec effet de lueur */
        .valo-title {
            font-family: 'VALORANT', sans-serif;
            font-family: 'Orbitron', sans-serif;
            color: #ff4655;
            font-size: 45px;
            text-align: center;
            text-shadow: 0px 0px 20px rgba(255, 70, 85, 0.5);
        }
        div.stButton > button {
            background-color: transparent;
            color: #ece8e1;
            font-family: 'VALORANT', sans-serif;
            border: 2px solid #ff4655;
            clip-path: polygon(10% 0, 100% 0, 100% 70%, 90% 100%, 0 100%, 0 30%);
            transition: 0.3s;
        }
        div.stButton > button:hover {
            background-color: #ff4655;
            color: white;
        }
        /* Style pour les cartes de stats */
        .stat-card {
            background: linear-gradient(135deg, rgba(255, 70, 85, 0.1) 0%, rgba(15, 25, 35, 0.9) 100%);
            border-left: 5px solid #ff4655;
            padding: 20px;
            font-size: 3.5rem;
            font-weight: bold;
            letter-spacing: 5px;
            text-shadow: 0 0 20px rgba(255, 70, 85, 0.5);
            margin-bottom: 30px;
        }

        /* Style pour les cartes de l'Intel Tracker */
        .player-card {
            background: #1f2326;
            padding: 20px;
            border-radius: 4px;
            text-align: center;
            border-top: 4px solid #ff4655;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)
    
def apply_immersive_mode():
    """Force le mode plein écran absolu sans aucun scroll possible"""
    st.markdown("""
        <style>
        /* 1. Supprime le header, le footer et les menus */
        header, [data-testid="stHeader"], footer { 
            display: none !important; 
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

        /* 2. Bloque la page au niveau du navigateur */
        html, body, .main {
            overflow: hidden !important;
            height: 100vh !important;
            width: 100vw !important;
            position: fixed !important;
            top: 0; left: 0;
        div.stButton > button:hover {
            background: #ff4655 !important;
            color: white !important;
            border: 1px solid #ff4655 !important;
            box-shadow: 0 0 15px rgba(255, 70, 85, 0.4);
            transform: translateY(-2px);
        }

        /* 3. Supprime les marges de Streamlit qui créent le scroll */
        [data-testid="stAppViewBlockContainer"] {
            padding: 0 !important;
            max-width: 100% !important;
        /* Cartes et conteneurs */
        .stSelectbox, .stTextArea {
            background: rgba(15, 25, 35, 0.8);
            border-radius: 5px;
        }

        /* 4. On s'assure que les boutons flottent au-dessus de l'iframe */
        .stColumn {
            padding: 5px !important;
        /* Barre de séparation rouge fine */
        hr {
            border: 0;
            height: 1px;
            background: linear-gradient(to right, transparent, #ff4655, transparent);
            margin: 20px 0;
        }
        </style>
    """, unsafe_allow_html=True)
