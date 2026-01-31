import streamlit as st
import pd as pd
import pandas as pd
import requests
import os
from PIL import Image
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="CRIMSON PROTOCOL v2", layout="wide", page_icon="🩸")

# --- INITIALISATION DES RÉPERTOIRES ---
folders = ["images_scrims", "match_proofs"]
for f in folders:
    if not os.path.exists(f): os.makedirs(f)

SCRIMS_DB = "scrims_database.csv"
AGENTS_DB = "agents_database.csv"
RANKS_DB = "ranks_database.csv"

def load_csv(file, columns):
    if os.path.exists(file):
        try: return pd.read_csv(file)
        except: return pd.DataFrame(columns=columns)
    return pd.DataFrame(columns=columns)

# --- SYSTÈME TRACKER RANGS ---
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

# --- UI DESIGN & CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.cdnfonts.com/css/valorant');
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&display=swap');

    .stApp { background-color: #0f1923; color: #ece8e1; font-family: 'Rajdhani', sans-serif; }
    
    .valo-title {
        font-family: 'VALORANT', sans-serif;
        color: #ff4655; font-size: 45px; text-align: center;
        text-shadow: 0px 0px 20px rgba(255, 70, 85, 0.5);
    }

    /* Style des boutons du menu */
    div.stButton > button {
        background-color: transparent; color: #ece8e1;
        font-family: 'VALORANT', sans-serif; border: 2px solid #ff4655;
        clip-path: polygon(10% 0, 100% 0, 100% 70%, 90% 100%, 0 100%, 0 30%);
        transition: 0.3s; width: 100%;
    }
    div.stButton > button:hover { background-color: #ff4655; color: white; box-shadow: 0px 0px 15px #ff4655; }

    /* Bouton RETOUR Flottant */
    .stButton > button[kind="secondary"] {
        position: fixed; top: 15px; left: 15px; z-index: 9999;
        background: #ff4655 !important; color: white !important; border: none;
    }

    /* Centrage Valoplant */
    .iframe-container {
        display: flex; justify-content: center; align-items: center;
        width: 100%; height: 92vh; margin: 0; padding: 0;
    }

    .stat-card {
        background: rgba(255, 70, 85, 0.1); border-left: 5px solid #ff4655;
        padding: 20px; border-radius: 0 10px 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- GESTION DE SESSION ---
if 'scrims_df' not in st.session_state: st.session_state['scrims_df'] = load_csv(SCRIMS_DB, ["Date", "Map", "Resultat", "Score", "Screenshot"])
if 'agent_data' not in st.session_state:
    if os.path.exists(AGENTS_DB):
        df_ag = pd.read_csv(AGENTS_DB)
        st.session_state['agent_data'] = dict(zip(df_ag.Key, df_ag.Val))
    else: st.session_state['agent_data'] = {}
if 'selected_strat_map' not in st.session_state: st.session_state['selected_strat_map'] = None
if "logged_in" not in st.session_state: st.session_state["logged_in"] = False
if "current_page" not in st.session_state: st.session_state["current_page"] = "DASHBOARD"

# --- ACCÈS SÉCURISÉ ---
if not st.session_state["logged_in"]:
    st.markdown("<div style='text-align:center; margin-top:50px;'>", unsafe_allow_html=True)
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
    # --- MODE IMMERSIF (VALOPLANT SANS INTERFACE) ---
    if st.session_state["current_page"] == "STRATÉGIE" and st.session_state['selected_strat_map'] is not None:
        # Masquage CSS total de l'interface Streamlit
        st.markdown("""<style>header, [data-testid="stHeader"], .valo-title, hr, .stTabs { visibility: hidden; height: 0; padding: 0; margin: 0; } .main .block-container { padding: 0 !important; max-width: 100% !important; } body { overflow: hidden !important; }</style>""", unsafe_allow_html=True)
        
        if st.button("⬅ RETOUR", key="back_immersion"):
            st.session_state['selected_strat_map'] = None
            st.rerun()
        
        st.markdown(f"""
            <div class="iframe-container">
                <iframe src="https://valoplant.gg" width="95%" height="100%" style="border: 2px solid #ff4655; border-radius: 15px; background: white;"></iframe>
            </div>
            """, unsafe_allow_html=True)

    else:
        # --- INTERFACE CLASSIQUE ---
        st.markdown("<h1 class='valo-title'>CRIMSON HQ</h1>", unsafe_allow_html=True)
        m_cols = st.columns([1, 1, 1, 1, 1, 1, 0.5])
        pages = ["DASHBOARD", "INTEL TRACKER", "MATCH ARCHIVE", "TACTICAL POOL", "PLANNING", "STRATÉGIE"]
        
        for idx, p_name in enumerate(pages):
            if m_cols[idx].button(p_name):
                st.session_state["current_page"] = p_name
                st.session_state['selected_strat_map'] = None
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
                    st.markdown(f"<div style='background:#1f2326; padding:20px; text-align:center; border-top: 3px solid #ff4655;'><h2>{pl['label']}</h2><p>RANK: <b style='color:#ff4655;'>{curr}</b></p><p style='font-size:12px; opacity:0.6;'>PEAK: {peak}</p></div>", unsafe_allow_html=True)
                    if icon: st.image(icon, width=80)

        # --- 3. MATCH ARCHIVE ---
        elif menu == "MATCH ARCHIVE":
            with st.expander("📝 AJOUTER UN MATCH"):
                with st.form("match_form", clear_on_submit=True):
                    m = st.selectbox("MAP", ["Abyss", "Ascent", "Bind", "Breeze", "Fracture", "Haven", "Icebox", "Lotus", "Pearl", "Split", "Sunset"])
                    r = st.radio("RESULTAT", ["WIN", "LOSS"], horizontal=True)
                    sc = st.text_input("SCORE (ex: 13-5)")
                    img = st.file_uploader("SCREENSHOT", type=['png', 'jpg'])
                    if st.form_submit_button("SAUVEGARDER"):
                        path = "None"
                        if img:
                            path = f"match_proofs/match_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                            Image.open(img).save(path)
                        new_data = pd.DataFrame([{"Date": datetime.now().strftime("%d/%m/%Y"), "Map": m, "Resultat": r, "Score": sc, "Screenshot": path}])
                        st.session_state['scrims_df'] = pd.concat([new_data, st.session_state['scrims_df']], ignore_index=True)
                        st.session_state['scrims_df'].to_csv(SCRIMS_DB, index=False)
                        st.rerun()

            if not st.session_state['scrims_df'].empty:
                to_del = []
                for idx, row in st.session_state['scrims_df'].iterrows():
                    c1, c2, c3, c4, c5 = st.columns([0.5, 1, 1, 1, 2])
                    if c1.checkbox("", key=f"del_{idx}"): to_del.append(idx)
                    c2.write(row['Date']); c3.write(row['Map']); c4.write(row['Score'])
                    if row['Screenshot'] != "None": c5.image(row['Screenshot'], width=150)
                    st.divider()
                if to_del and st.button("🗑️ SUPPRIMER LA SÉLECTION"):
                    st.session_state['scrims_df'] = st.session_state['scrims_df'].drop(to_del).reset_index(drop=True)
                    st.session_state['scrims_df'].to_csv(SCRIMS_DB, index=False)
                    st.rerun()

        # --- 4. TACTICAL POOL ---
        elif menu == "TACTICAL POOL":
            p_sel = st.selectbox("OPÉRATIVE", ["BOO ツ", "KURAIME"])
            cats = {"SENTINEL": ["Chamber", "Cypher", "Killjoy", "Sage", "Vyse"], "DUELIST": ["Jett", "Raze", "Neon", "Reyna", "Iso"], "INITIATOR": ["Sova", "Skye", "Gekko", "Fade", "Breach"], "CONTROLLER": ["Omen", "Clove", "Viper", "Brimstone", "Astra"]}
            cols = st.columns(4)
            for i, (role, agents) in enumerate(cats.items()):
                with cols[i]:
                    st.markdown(f"**{role}**")
                    for a in agents:
                        k = f"{p_sel}_{a}"
                        st.session_state['agent_data'][k] = st.checkbox(a, value=st.session_state['agent_data'].get(k, False), key=k)
            if st.button("SAVE MASTERY"):
                pd.DataFrame(list(st.session_state['agent_data'].items()), columns=['Key', 'Val']).to_csv(AGENTS_DB, index=False)
                st.success("Maitrises mises à jour.")

        # --- 5. PLANNING ---
        elif menu == "PLANNING":
            st.info("Éditez votre emploi du temps hebdomadaire.")
            st.data_editor(pd.DataFrame({"JOUR": ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"], "BOO": [""]*7, "KURAIME": [""]*7}), use_container_width=True)

        # --- 6. STRATÉGIE (SÉLECTION MAP) ---
        elif menu == "STRATÉGIE":
            maps = ["Abyss", "Ascent", "Bind", "Breeze", "Fracture", "Haven", "Icebox", "Lotus", "Pearl", "Split", "Sunset"]
            cols = st.columns(4)
            for i, m_name in enumerate(maps):
                if cols[i % 4].button(m_name.upper(), use_container_width=True):
                    st.session_state['selected_strat_map'] = m_name
                    st.rerun()
