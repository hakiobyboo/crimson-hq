import streamlit as st

def apply_global_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@500;700&display=swap');

        .stApp {
            background: radial-gradient(circle at center, #1a242f 0%, #0f1923 100%);
            color: #ece8e1;
            font-family: 'Rajdhani', sans-serif;
        }

        .valo-title {
            font-family: 'Orbitron', sans-serif;
            color: #ff4655;
            text-align: center;
            font-size: 5rem;
            font-weight: 900;
            letter-spacing: 12px;
            text-transform: uppercase;
            background: linear-gradient(to bottom, #ff4655 0%, #8b1e28 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            filter: drop-shadow(0 0 15px rgba(255, 70, 85, 0.5));
            animation: floating 3s ease-in-out infinite;
        }

        @keyframes floating {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }

        div.stButton > button {
            background: rgba(255, 70, 85, 0.05) !important;
            color: #ff4655 !important;
            border: 2px solid #ff4655 !important;
            border-radius: 0px !important;
            font-family: 'Orbitron', sans-serif !important;
            text-transform: uppercase;
            letter-spacing: 2px;
            transition: all 0.4s ease !important;
            clip-path: polygon(10% 0, 100% 0, 90% 100%, 0% 100%);
        }

        div.stButton > button:hover {
            background: #ff4655 !important;
            color: white !important;
            box-shadow: 0 0 30px rgba(255, 70, 85, 0.8);
            transform: scale(1.05);
        }

        .stat-card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 25px;
            border-radius: 15px;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

def apply_immersive_mode():
    st.markdown("<style>#MainMenu, footer, header {visibility: hidden;}</style>", unsafe_allow_html=True)
