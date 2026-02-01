import streamlit as st

def apply_global_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.cdnfonts.com/css/valorant');
        @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&display=swap');

        .stApp {
            background-color: #0f1923;
            color: #ece8e1;
            font-family: 'Rajdhani', sans-serif;
        }
        .valo-title {
            font-family: 'VALORANT', sans-serif;
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
    """Cache toute l'interface Streamlit et FORCE le plein écran pour Valoplant"""
    st.markdown("""
        <style>
        /* 1. Cache les éléments inutiles */
        header, [data-testid="stHeader"], .valo-title, hr, .stDivider, [data-testid="stSidebar"] { 
            display: none !important; 
        }

        /* 2. On s'assure que le bouton RETOUR est visible par-dessus l'iframe */
        /* On cible le bouton dans la première colonne de la page de strat */
        div.stButton > button {
            position: relative;
            z-index: 10001 !important; /* Plus haut que l'iframe */
            margin-bottom: 10px;
        }

        /* 3. Suppression des marges pour coller aux bords */
        [data-testid="stAppViewBlockContainer"] {
            padding: 10px !important; /* On laisse un peu de place en haut pour le bouton */
            max-width: 100% !important;
        }

        /* 4. L'iframe est placée juste en dessous du bouton */
        .iframe-container {
            position: fixed;
            top: 60px; /* On descend l'iframe pour laisser de la place au bouton RETOUR */
            left: 0;
            width: 100vw;
            height: calc(100vh - 60px);
            z-index: 9999;
            background-color: #0f1923;
        }

        iframe {
            width: 100% !important;
            height: 100% !important;
            border: none !important;
        }

        /* Bloque le scroll du site pour focus l'iframe */
        html, body, [data-testid="stAppViewContainer"] {
            overflow: hidden !important;
        }
        </style>
    """, unsafe_allow_html=True)
