import streamlit as st
import os
from PIL import Image
from database import load_csv, get_intel, SCRIMS_DB

def show_dashboard():
    df = st.session_state['scrims_df']
    total = len(df)
    wins = len(df[df['Resultat'] == "WIN"])
    wr = f"{(wins/total)*100:.1f}%" if total > 0 else "0.0%"
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='stat-card'><h4>WINRATE</h4><h2 style='color:#ff4655;'>{wr}</h2></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='stat-card'><h4>TOTAL SCRIMS</h4><h2 style='color:#ff4655;'>{total}</h2></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='stat-card'><h4>STATUS</h4><h2 style='color:#00ff00;'>● ONLINE</h2></div>", unsafe_allow_html=True)

def show_intel():
    players = [{"label": "Boo ツ", "n": "Boo%20%E3%83%84", "t": "1tpas"}, {"label": "Kuraime", "n": "kuraime", "t": "ezz"}]
    cols = st.columns(2)
    for i, pl in enumerate(players):
        with cols[i]:
            curr, peak, icon, status = get_intel(pl['n'], pl['t'], pl['label'])
            st.markdown(f"<div style='background:#1f2326; padding:20px; text-align:center;'><h2>{pl['label']}</h2><p>RANK: {curr}</p></div>", unsafe_allow_html=True)
            if icon: st.image(icon, width=80)

def show_strategy_map(current_map):
    # Sélecteur de mode (Archive ou Valoplant)
    deploy_mode = st.toggle("📂 ACCÉDER AUX ARCHIVES IMAGES", value=False)
    
    if deploy_mode:
        st.info(f"Dossier tactique : {current_map}")
        # (Le code des archives images ici)
    else:
        # VALOPLANT PLEIN ÉCRAN
        st.markdown(f"""
            <div style="display: flex; justify-content: center; align-items: center; width: 100%;">
                <iframe src="https://valoplant.gg" 
                    width="100%" 
                    height="850vh" 
                    style="border: 2px solid #ff4655; border-radius: 10px; background: white;">
                </iframe>
            </div>
        """, unsafe_allow_html=True)