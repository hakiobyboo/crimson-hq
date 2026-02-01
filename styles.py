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
    """Version épurée : masque le header mais laisse les boutons de logic.py libres"""
    st.markdown("""
        <style>
        /* Masque le header Streamlit pour gagner de la place */
        header, [data-testid="stHeader"] { 
            visibility: hidden !important;
            height: 0px !important;
        }

        /* Supprime le padding inutile en haut */
        [data-testid="stAppViewBlockContainer"] {
            padding-top: 1rem !important;
        }

        /* Bloque le scroll principal pour Valoplant */
        .main { overflow: hidden !important; }
        
        /* On s'assure que les boutons ne sont PLUS figés en haut à gauche */
        div.stButton > button {
            position: static !important;
        }
        </style>
    """, unsafe_allow_html=True)


