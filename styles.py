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
    """Verrouillage total du scroll pour forcer l'usage de la molette dans l'iframe uniquement"""
    st.markdown("""
        <style>
        /* 1. Cache les éléments parasites de Streamlit */
        header, [data-testid="stHeader"], footer { 
            display: none !important;
        }

        /* 2. Verrouille le conteneur principal à la taille de l'écran */
        html, body, [data-testid="stAppViewBlockContainer"] {
            overflow: hidden !important;
            height: 100vh !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        /* 3. On s'assure que la zone de contenu ne peut pas scroller */
        .main {
            overflow: hidden !important;
            height: 100vh !important;
        }

        /* 4. Ajustement des boutons de navigation pour qu'ils ne créent pas de scroll */
        div.stButton > button {
            margin-bottom: 10px !important;
        }

        /* 5. On retire les paddings de Streamlit qui poussent le contenu vers le bas */
        [data-testid="stAppViewBlockContainer"] {
            padding-top: 10px !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

