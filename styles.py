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
        /* 1. Cache le header, le menu et les titres */
        header, [data-testid="stHeader"], .valo-title, hr, .stDivider, [data-testid="stSidebar"] { 
            display: none !important; 
        }

        /* 2. Suppression des marges Streamlit pour coller aux bords */
        [data-testid="stAppViewBlockContainer"] {
            padding: 0px !important;
            max-width: 100% !important;
            width: 100% !important;
        }

        .main .block-container { 
            padding: 0px !important; 
            margin: 0px !important; 
            max-width: 100% !important; 
        }

        /* 3. BLOCAGE DU SCROLL DU SITE (Force la molette sur l'iframe) */
        html, body, [data-testid="stAppViewContainer"] {
            overflow: hidden !important;
        }

        /* 4. Conteneur Iframe FIXÉ pour ignorer les colonnes et centrer */
        .iframe-container {
            position: fixed;
            top: 45px; /* Laisse juste la place pour le bouton EXIT */
            left: 0;
            width: 100vw;
            height: calc(100vh - 45px);
            z-index: 9999;
            background-color: #0f1923;
        }

        iframe {
            width: 100% !important;
            height: 100% !important;
            border: none !important;
            scroll-behavior: smooth;
        }
        </style>

        <script>
        // Script pour forcer le focus de la molette dans l'iframe
        window.addEventListener('wheel', function(e) {
            if(e.target.tagName == 'IFRAME') { 
                e.stopPropagation(); 
            }
        }, {passive: false});
        </script>
    """, unsafe_allow_html=True)
