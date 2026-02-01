import streamlit as st

def apply_global_styles():
    """Applique le design complet Crimson Protocol à l'application"""
    st.markdown("""
        <style>
        /* Importation des polices Valorant et Tech */
        @import url('https://fonts.cdnfonts.com/css/valorant');
        @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&display=swap');

        /* Fond de l'application avec motif de grille subtil */
        .stApp {
            background-color: #0f1923;
            background-image: radial-gradient(circle at 2px 2px, rgba(255, 70, 85, 0.05) 1px, transparent 0);
            background-size: 40px 40px;
            color: #ece8e1;
            font-family: 'Rajdhani', sans-serif;
        }

        /* Titre Principal Style Valorant */
        .valo-title {
            font-family: 'VALORANT', sans-serif;
            color: #ff4655;
            font-size: 45px;
            text-align: center;
            margin-bottom: 20px;
            text-shadow: 0px 0px 20px rgba(255, 70, 85, 0.5);
        }

        /* Style des Boutons (Forme biseautée Valorant) */
        div.stButton > button {
            background-color: transparent;
            color: #ece8e1;
            font-family: 'VALORANT', sans-serif;
            border: 2px solid #ff4655;
            clip-path: polygon(10% 0, 100% 0, 100% 70%, 90% 100%, 0 100%, 0 30%);
            transition: 0.3s;
            width: 100%;
            height: 45px;
            font-size: 14px !important;
        }

        div.stButton > button:hover {
            background-color: #ff4655;
            color: white;
            box-shadow: 0px 0px 15px #ff4655;
            transform: translateY(-2px);
        }

        /* Cartes de statistiques (Dashboard) */
        .stat-card {
            background: linear-gradient(135deg, rgba(255, 70, 85, 0.1) 0%, rgba(15, 25, 35, 0.9) 100%);
            border-left: 5px solid #ff4655;
            padding: 25px;
            border-radius: 0px 15px 15px 0px;
            margin: 10px 0px;
            box-shadow: 5px 5px 15px rgba(0,0,0,0.3);
        }

        /* Conteneur pour le Tracker de rang */
        .player-card {
            background: #1f2326;
            padding: 20px;
            border-radius: 4px;
            text-align: center;
            border-top: 4px solid #ff4655;
            margin-bottom: 20px;
        }

        /* Style pour les Data Editors (Tableaux) */
        .stDataEditor {
            background-color: #1f2326 !important;
            border-radius: 8px !important;
        }

        /* Custom scrollbar pour tout le site */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #0f1923; }
        ::-webkit-scrollbar-thumb { background: #ff4655; border-radius: 4px; }
        </style>
    """, unsafe_allow_html=True)

def apply_immersive_mode():
    """Mode spécial pour Valoplant : Full screen total, centrage forcé et molette"""
    st.markdown("""
        <style>
        /* 1. Suppression totale des éléments d'interface */
        header, [data-testid="stHeader"], .valo-title, hr, .stDivider { 
            display: none !important; 
        }
        
        /* 2. Éclatement des marges Streamlit pour le mode Full Width */
        [data-testid="stAppViewBlockContainer"] {
            padding: 0px !important;
            max-width: 100% !important;
            width: 100% !important;
        }
        
        .main .block-container { 
            padding: 0rem !important; 
            max-width: 100% !important;
            margin-left: 0px !important;
            margin-right: 0px !important;
        }

        /* 3. Conteneur Iframe pour occuper tout l'écran */
        .iframe-container {
            display: flex;
            justify-content: center;
            align-items: flex-start;
            width: 100vw;
            height: 98vh;
            background-color: #0f1923;
            margin: 0 !important;
            padding: 0 !important;
        }

        iframe {
            width: 100% !important;
            height: 100% !important;
            border: none !important;
        }
        </style>
        
        <script>
        // Gestion de la molette pour Valoplant
        const mapFrame = document.querySelector('iframe');
        if (mapFrame) {
            mapFrame.addEventListener('mouseenter', () => {
                document.body.style.overflow = 'hidden';
            });
            mapFrame.addEventListener('mouseleave', () => {
                document.body.style.overflow = 'auto';
            });
        }
        </script>
    """, unsafe_allow_html=True)
