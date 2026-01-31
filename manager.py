import streamlit as st
import pandas as pd
import requests
import os
from PIL import Image
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="CRIMSON PROTOCOL v2", layout="wide", page_icon="🩸")

# --- INITIALISATION DES RÉPERTOIRES ET FICHIERS ---
if not os.path.exists("images_scrims"): os.makedirs("images_scrims")
if not os.path.exists("match_proofs"): os.makedirs("match_proofs")

SCRIMS_DB = "scrims_database.csv"
AGENTS_DB = "agents_database.csv"
RANKS_DB = "ranks_database.csv"

def load_csv(file, columns):
    if os.path.exists(file):
        try: return pd.read_csv(file)
        except: return pd.DataFrame(columns=columns)
    return pd.DataFrame(columns=columns)

# --- SYSTÈME TRACKER RANGS (INTEL) ---
def get_intel(name, tag, label):
    try:
        url = f"https://api.henrikdev.xyz/valorant/v1/mmr/eu/{name}/{tag}"
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        if r.status_code == 200:
            d = r.json().get('data')
            if d:
                curr = d.get('currenttierpatched', 'Unknown')
                peak = d.get('highest_tier_patched', 'N/A')
                icon = d.get('images', {}).get('small')
                new_data = pd.DataFrame([{"Player": label, "Current": curr, "Peak": peak}])
                old_df = load_csv(RANKS_DB, ["Player", "Current", "Peak"])
                updated_df = pd.concat([old_df[old_df['Player'] != label], new_data], ignore_index=True)
                updated_df.to_csv(RANKS_DB, index=False)
                return curr, peak, icon, "LIVE"
    except: pass
    saved_df = load_csv(RANKS_DB, ["Player", "Current", "Peak"])
    player_data = saved_df[saved_df['Player'] == label]
    if not player_data.empty:
        return player_data['Current'].values[0], player_data['Peak'].values[0], None, "OFFLINE"
    return "Disconnected", "N/A", None, "ERROR"

# --- UI DESIGN GLOBAL ---
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
        margin-bottom: 20px;
    }

    /* Style des Boutons du Menu */
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
        box-shadow: 0px 0px 15px #ff4655;
    }

    /* Bouton Retour spécial pour le mode Strat */
    .stButton > button[kind="secondary"] {
        position: fixed;
        top: 15px;
        left: 15px;
        z-index: 9999;
        background-color: #ff4655 !important;
        color: white !important;
        border: none !important;
    }

    /* Centrage Valoplant */
    .iframe-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        height: 85vh;
        margin-top: 10px;
    }

    .stat-card {
        background: rgba(255, 70, 85, 0.1);
        border-left: 5px solid #ff4655;
        padding: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- GESTION DE LA SESSION ---
if 'scrims_df' not in st.session_state: st.session_state['scrims_df'] = load_csv(SCRIMS_DB, ["Date", "Map", "Resultat", "Score", "Screenshot"])
if 'agent_data' not in st.session_state:
    if os.path.exists(AGENTS_DB):
        df_ag = pd.read_csv(AGENTS_DB)
        st.session_state['agent_data'] = dict(zip(df_ag.Key, df_ag.Val))
    else: st.session_state['agent_data'] = {}
if 'selected_strat_map' not in st.session_state: st.session_state['selected_strat_map'] = None
if "logged_in" not in st.session_state: st.session_state["logged_in"] = False
if "current_page" not in st.session_state: st.session_state["current_page"] = "DASHBOARD"

# --- LOGIQUE D'ACCÈS ---
if not st.session_state["logged_in"]:
    st.markdown("<div style='text-align:center; margin-top:50px;'>", unsafe_allow_html=True)
    st.image("https://via.placeholder.com/150/ff4655/ffffff?text=LOGO", width=150)
    st.markdown("<h1 class='valo-title'>CRIMSON ACCESS</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        e = st.text_input("UNIT ID")
        p = st.text_input("ENCRYPTION KEY", type="password")
        if st.button("INITIALIZE SYSTEM"):
            if e == "titi12012008@gmail.com" and p == "Tn12janv2008":
                st.session_state["logged_in"] = True
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- LOGIQUE PLEIN ÉCRAN POUR VALOPLANT ---
    if st.session_state['selected_strat_map'] and st.session_state["current_page"] == "STRATÉGIE":
        if st.button("⬅ RETOUR", key="back_map"):
            st.session_state['selected_strat_map'] = None
            st.rerun()
            
        st.markdown(f"""
            <style>
                header, footer, [data-testid="stHeader"] {{ visibility: hidden; }}
                .block-container {{ padding: 0 !important; max-width: 100% !important; }}
                body {{ overflow: hidden !important; }}
            </style>
            <div class="iframe-wrapper">
                <iframe src="https://valoplant.gg" width="95%" height="100%" style="border: 2px solid #ff4655; border-radius: 15px; background: white;"></iframe>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        # --- INTERFACE CLASSIQUE (MENU VISIBLE) ---
        st.markdown("<h1 class='valo-title'>CRIMSON HQ</h1>", unsafe_allow_html=True)
        m_cols = st.columns([1, 1, 1, 1, 1, 1, 0.5])
        pages = ["DASHBOARD", "INTEL TRACKER", "MATCH ARCHIVE", "TACTICAL POOL", "PLANNING", "STRATÉGIE"]
        
        for idx, p_name in enumerate(pages):
            if m_cols[idx].button(p_name, use_container_width=True):
                st.session_state["current_page"] = p_name
                st.rerun()
        
        if m_cols[6].button("✖"):
            st.session_state["logged_in"] = False
            st.rerun()
        
        st.divider()
        menu = st.session_state["current_page"]

        # --- 1. DASHBOARD ---
        if menu == "DASHBOARD":
            df = st.session_state['scrims_df']
            total = len(df); wins = len(df[df['Resultat'] == "WIN"])
            wr = f"{(wins/total)*100:.1f}%" if total > 0 else "0.0%"
            c1, c2, c3 = st.columns(3)
            with c1: st.markdown(f"<div class='stat-card'><h4>WINRATE</h4><h2 style='color:#ff4655;'>{wr}</h2></div>", unsafe_allow_html=True)
            with c2: st.markdown(f"<div class='stat-card'><h4>TOTAL SCRIMS</h4><h2 style='color:#ff4655;'>{total}</h2></div>", unsafe_allow_html=True)
            with c3: st.markdown(f"<div class='stat-card'><h4>STATUS</h4><h2 style='color:#00ff00;'>● ONLINE</h2></div>", unsafe_allow_html=True)

        # --- 2. INTEL TRACKER ---
        elif menu == "INTEL TRACKER":
            players = [{"label": "Boo ツ", "n": "Boo%20%E3%83%84", "t": "1tpas"}, {"label": "Kuraime", "n": "kuraime", "t": "ezz"}]
            cols = st.columns(2)
            for i, pl in enumerate(players):
                with cols[i]:
                    curr, peak, icon, status = get_intel(pl['n'], pl['t'], pl['label'])
                    st.markdown(f"<div style='background:#1f2326; padding:20px; text-align:center; border-top: 3px solid #ff4655;'><h2>{pl['label']}</h2><p>RANK: {curr}</p></div>", unsafe_allow_html=True)
                    if icon: st.image(icon, width=80)

        # --- 3. MATCH ARCHIVE ---
        elif menu == "MATCH ARCHIVE":
            with st.expander("ADD NEW SCRIM"):
                with st.form("scrim_form"):
                    m = st.selectbox("MAP", ["Abyss", "Ascent", "Bind", "Breeze", "Fracture", "Haven", "Icebox", "Lotus", "Pearl", "Split", "Sunset"])
                    r = st.radio("RESULT", ["WIN", "LOSS"], horizontal=True)
                    sc = st.text_input("SCORE")
                    if st.form_submit_button("SAVE"):
                        new_m = {"Date": datetime.now().strftime("%d/%m/%Y"), "Map": m, "Resultat": r, "Score": sc, "Screenshot": "None"}
                        st.session_state['scrims_df'] = pd.concat([pd.DataFrame([new_m]), st.session_state['scrims_df']], ignore_index=True)
                        st.session_state['scrims_df'].to_csv(SCRIMS_DB, index=False)
                        st.rerun()
            st.dataframe(st.session_state['scrims_df'], use_container_width=True)

        # --- 4. TACTICAL POOL ---
        elif menu == "TACTICAL POOL":
            p_sel = st.selectbox("OPERATIVE", ["BOO ツ", "KURAIME"])
            st.info("Sélectionnez vos agents maîtrisés.")
            # ... (Logique agent_data comme avant)

        # --- 5. STRATÉGIE (SÉLECTION DE MAP) ---
        elif menu == "STRATÉGIE":
            maps = ["Abyss", "Ascent", "Bind", "Breeze", "Fracture", "Haven", "Icebox", "Lotus", "Pearl", "Split", "Sunset"]
            cols = st.columns(4)
            for i, m_name in enumerate(maps):
                if cols[i % 4].button(m_name.upper(), use_container_width=True):
                    st.session_state['selected_strat_map'] = m_name
                    st.rerun()
