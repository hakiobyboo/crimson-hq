import streamlit as st

def apply_global_styles():
    """Applique le design complet Crimson Protocol à l'application"""
    st.markdown("""
        <style>
        @import url('https://fonts.cdnfonts.com/css/valorant');
        @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&display=swap');

        .stApp {
            background-color: #0f1923;
            background-image: radial-gradient(circle at 2px 2px, rgba(255, 70, 85, 0.05) 1px, transparent 0);
            background-size: 40px 40px;
            color: #ece8e1;
            font-family: 'Rajdhani', sans-serif;
        }

        .valo-title {
            font-family: 'VALORANT', sans-serif;
            color: #ff4655;
            font-size: 45px;
            text-align: center;
            margin-bottom: 20px;
            text-shadow: 0px 0px 20px rgba(255, 70, 85, 0.5);
        }

        div.stButton > button {
            background-color: transparent;
            color: #ece8e1;
            font-family: 'VALORANT', sans-serif;
            border: 2px solid #ff4655;
            clip-path: polygon(10% 0, 100% 0, 100% 70%, 90% 100%, 0 100%, 0 30%);
            transition: 0.3s;
            width: 100%;
            height: 45px;
        }

        div.stButton > button:hover {
            background-color: #ff4655;
            color: white;
            box-shadow: 0px 0px 15px #ff4655;
        }

        .stat-card {
            background: linear-gradient(135deg, rgba(255, 70, 85, 0.1) 0%, rgba(15, 25, 35, 0.9) 100%);
            border-left: 5px solid #ff4655;
            padding: 25px;
            border-radius: 0px 15px 15px 0px;
            margin: 10px 0px;
        }

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
    """FORCE le plein écran total et bloque le scroll du site principal"""
    st.markdown("""
        <style>
        /* Masquage des éléments Streamlit */
        header, [data-testid="stHeader"], [data-testid="stSidebar"], .valo-title {
            display: none !important;
        }

        /* Suppression des marges pour utiliser 100% de la largeur */
        [data-testid="stAppViewBlockContainer"] {
            padding: 0px !important;
            max-width: 100% !important;
            width: 100% !important;
        }

        /* BLOCAGE DU SCROLL DU SITE (Pour libérer la molette) */
        html, body, [data-testid="stAppViewContainer"] {
            overflow: hidden !important;
        }

        /* Conteneur Iframe Fixé aux bords de l'écran */
        .iframe-container {
            position: fixed;
            top: 50px; /* Laisse de la place pour le bouton Exit et les Radios */
            left: 0;
            width: 100vw;
            height: calc(100vh - 50px);
            z-index: 9999;
            background-color: #0f1923;
        }

        iframe {
            width: 100% !important;
            height: 100% !important;
            border: none !important;
        }
        </style>
    """, unsafe_allow_html=True)
