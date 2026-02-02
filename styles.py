import streamlit as st

import streamlit as st

def apply_global_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

        .stApp {
            background: radial-gradient(circle at top, #1f2326 0%, #0f1923 100%);
        }

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

        div.stButton > button {
            background: rgba(255, 255, 255, 0.05) !important;
            color: #ece8e1 !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 0px !important;
            transition: all 0.3s ease !important;
            font-family: 'Orbitron', sans-serif !important;
            text-transform: uppercase;
        }

        div.stButton > button:hover {
            background: #ff4655 !important;
            box-shadow: 0 0 15px rgba(255, 70, 85, 0.4);
            transform: translateY(-2px);
        }

        hr {
            border: 0;
            height: 1px;
            background: linear-gradient(to right, transparent, #ff4655, transparent);
        }
        </style>
    """, unsafe_allow_html=True)

def apply_immersive_mode():
    st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>", unsafe_allow_html=True)

