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
        </style>
    """, unsafe_allow_html=True)

def apply_immersive_mode():
    """Cache toute l'interface Streamlit pour Valoplant"""
    st.markdown("""
        <style>
        /* Cache le header, le menu et les titres */
        header, [data-testid="stHeader"], .valo-title, hr, .stDivider { display: none !important; }
        .main .block-container { padding-top: 0rem !important; padding-bottom: 0rem !important; max-width: 98% !important; }
        /* Permet le scroll interne de l'iframe */
        iframe { scroll-behavior: smooth; }
        </style>
        <script>
        // Script pour aider la molette dans les iframes
        window.addEventListener('wheel', function(e) {
            if(e.target.tagName == 'IFRAME') { e.stopPropagation(); }
        }, {passive: false});
        </script>
    """, unsafe_allow_html=True)