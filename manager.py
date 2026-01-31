import streamlit as st
import pandas as pd
import requests
import os
from PIL import Image
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="CRIMSON PROTOCOL v2", layout="wide", page_icon="🩸")

# --- INITIALISATION DES RÉPERTOIRES ET FICHIERS ---
if not os.path.exists("images_scrims"):
    os.makedirs("images_scrims")

SCRIMS_DB = "scrims_database.csv"
AGENTS_DB = "agents_database.csv"
RANKS_DB = "ranks_database.csv"

def load_csv(file, columns):
    if os.path.exists(file):
        try:
            return pd.read_csv(file)
        except:
            return pd.DataFrame(columns=columns)
    return pd.DataFrame(columns=columns)

# --- UI DESIGN (CSS CRIMSON HQ) ---
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
        font-size: 60px; 
        text-align: center; 
        margin-bottom: 30px;
        text-shadow: 0px 0px 20px rgba(255, 70, 85, 0.5);
    }

    .stat-card {
        background: linear-gradient(135deg, rgba(255, 70, 85, 0.1) 0%, rgba(15, 25, 35, 0.9) 100%);
        border-left: 5px solid #ff4655;
        padding: 25px;
        border-radius: 0px 15px 15px 0px;
        box-shadow: 10px 10px 20px rgba(0,0,0,0.3);
    }

    .player-card {
        background: #1f2326;
        border: 1px solid rgba(236, 232, 225, 0.1);
        padding: 20px;
        border-radius: 4px;
        text-align: center;
        position: relative;
    }

    div.stButton > button {
        background-color: transparent;
        color: #ece8e1;
        font-family: 'VALORANT', sans-serif;
        border: 2px solid #ff4655;
        clip-path: polygon(10% 0, 100% 0, 100% 70%, 90% 100%, 0 100%, 0 30%);
        transition: 0.4s;
        width: 100%;
    }

    div.stButton > button:hover {
        background-color: #ff4655;
        color: white;
        box-shadow: 0px 0px 15px #ff4655;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SYSTÈME TRACKER HYBRIDE (API + LOCAL) ---
def get_intel(name, tag, label):
    """Tente l'API avec timeout, sinon charge le cache local"""
    try:
        url = f"https://api.henrikdev.xyz/valorant/v1/mmr/eu/{name}/{tag}"
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=3)
        if r.status_code == 200:
            d = r.json().get('data')
            if d:
                curr = d.get('currenttierpatched', 'Unknown')
                peak = d.get('highest_tier_patched', 'N/A')
                icon = d.get('images', {}).get('small')
                # Sauvegarde auto pour le mode offline
                new_data = pd.DataFrame([{"Player": label, "Current": curr, "Peak": peak}])
                old_df = load_csv(RANKS_DB, ["Player", "Current", "Peak"])
                pd.concat([old_df[old_df['Player'] != label], new_data]).to_csv(RANKS_DB, index=False)
                return curr, peak, icon, "LIVE"
    except:
        pass
    
    # Mode Secours : Lecture du CSV
    saved_df = load_csv(RANKS_DB, ["Player", "Current", "Peak"])
    player_data = saved_df[saved_df['Player'] == label]
    if not player_data.empty:
        return player_data['Current'].values[0], player_data['Peak'].values[0], None, "OFFLINE (CACHED)"
    return "Disconnected", "N/A", None, "ERROR"

# --- GESTION DE LA SESSION ---
if 'scrims_df' not in st.session_state:
    st.session_state['scrims_df'] = load_csv(SCRIMS_DB, ["Date", "Map", "Resultat", "Score", "Image_Path"])

if 'agent_data' not in st.session_state:
    if os.path.exists(AGENTS_DB):
        df_ag = pd.read_csv(AGENTS_DB)
        st.session_state['agent_data'] = dict(zip(df_ag.Key, df_ag.Val))
    else:
        st.session_state['agent_data'] = {}

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# --- APPLICATION ---
if not st.session_state["logged_in"]:
    st.markdown("<h1 class='valo-title'>CRIMSON ACCESS</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        e = st.text_input("UNIT ID")
        p = st.text_input("ENCRYPTION KEY", type="password")
        if st.button("INITIALIZE SYSTEM"):
            if e == "titi12012008@gmail.com" and p == "Tn12janv2008":
                st.session_state["logged_in"] = True
                st.rerun()
else:
    # --- SIDEBAR NAVIGATION ---
    st.sidebar.markdown("<h2 style='text-align:center; color:#ff4655; font-family:VALORANT;'>CRIMSON HQ</h2>", unsafe_allow_html=True)
    menu = st.sidebar.radio("SQUAD TERMINAL", ["DASHBOARD", "INTEL TRACKER", "MATCH ARCHIVE", "TACTICAL POOL", "PLANNING"])
    
    if st.sidebar.button("SHUTDOWN"):
        st.session_state["logged_in"] = False
        st.rerun()

    # --- 1. DASHBOARD ---
    if menu == "DASHBOARD":
        st.markdown("<h1 class='valo-title'>COMMAND CENTER</h1>", unsafe_allow_html=True)
        df = st.session_state['scrims_df']
        total = len(df)
        wins = len(df[df['Resultat'] == "WIN"])
        wr = f"{(wins/total)*100:.1f}%" if total > 0 else "0.0%"
        
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"<div class='stat-card'><h4>WINRATE</h4><h2 style='color:#ff4655;'>{wr}</h2></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='stat-card'><h4>TOTAL SCRIMS</h4><h2 style='color:#ff4655;'>{total}</h2></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='stat-card'><h4>STATUS</h4><h2 style='color:#00ff00;'>● ONLINE</h2></div>", unsafe_allow_html=True)

    # --- 2. INTEL TRACKER (HYBRIDE) ---
    elif menu == "INTEL TRACKER":
        st.markdown("<h1 class='valo-title'>SQUAD INTEL</h1>", unsafe_allow_html=True)
        players = [
            {"label": "Boo ツ", "n": "Boo%20%E3%83%84", "t": "1tpas"},
            {"label": "Kuraime", "n": "kuraime", "t": "ezz"}
        ]
        
        cols = st.columns(2)
        for i, pl in enumerate(players):
            with cols[i]:
                curr, peak, icon, status = get_intel(pl['n'], pl['t'], pl['label'])
                st.markdown(f"""
                <div class='player-card'>
                    <p style='color:{"#00ff00" if status=="LIVE" else "#ffb400"}; font-size:12px;'>STATUS: {status}</p>
                    <h2 style='color:#ff4655;'>{pl['label']}</h2>
                    <hr style='border-color:rgba(255,70,85,0.2)'>
                    <p style='font-size:14px; margin-bottom:0;'>ACTUAL RANK</p>
                    <p style='font-size:28px; color:#ece8e1;'><b>{curr.upper()}</b></p>
                    <p style='font-size:14px; margin-top:10px; margin-bottom:0;'>PEAK RANK</p>
                    <p style='font-size:20px; color:#ffb400;'>{peak}</p>
                </div>
                """, unsafe_allow_html=True)
                if icon: st.image(icon, width=80)
                
                with st.expander("MANUAL OVERRIDE"):
                    mc = st.text_input("Rank Actuel", value=curr, key=f"c_{pl['label']}")
                    mp = st.text_input("Peak Rank", value=peak, key=f"p_{pl['label']}")
                    if st.button("SAVE INTEL", key=f"b_{pl['label']}"):
                        upd = pd.DataFrame([{"Player": pl['label'], "Current": mc, "Peak": mp}])
                        old_df = load_csv(RANKS_DB, ["Player", "Current", "Peak"])
                        pd.concat([old_df[old_df['Player'] != pl['label']], upd]).to_csv(RANKS_DB, index=False)
                        st.success("Données sauvegardées !")
                        st.rerun()

    # --- 3. MATCH ARCHIVE ---
    elif menu == "MATCH ARCHIVE":
        st.markdown("<h1 class='valo-title'>MATCH LOGS</h1>", unsafe_allow_html=True)
        with st.expander("ADD NEW SCRIM DATA"):
            with st.form("scrim_form", clear_on_submit=True):
                c_u1, c_u2 = st.columns(2)
                with c_u1: f = st.file_uploader("VISUAL INTEL", type=['png', 'jpg'])
                with c_u2:
                    m = st.selectbox("ZONE", ["Abyss", "Ascent", "Bind", "Haven", "Icebox", "Lotus", "Pearl", "Split", "Sunset"])
                    r = st.radio("STATUS", ["WIN", "LOSS"], horizontal=True)
                    sc = st.text_input("SCORE")
                if st.form_submit_button("SUBMIT LOG"):
                    if f:
                        path = f"images_scrims/scrim_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                        Image.open(f).save(path)
                        new_m = {"Date": datetime.now().strftime("%d/%m/%Y"), "Map": m, "Resultat": r, "Score": sc, "Image_Path": path}
                        st.session_state['scrims_df'] = pd.concat([pd.DataFrame([new_m]), st.session_state['scrims_df']], ignore_index=True)
                        st.session_state['scrims_df'].to_csv(SCRIMS_DB, index=False)
                        st.success("Log Archivé !")

        for _, row in st.session_state['scrims_df'].iterrows():
            st.markdown(f"""
            <div style='background:rgba(31,35,38,0.8); border-left:4px solid {"#00ff00" if row["Resultat"]=="WIN" else "#ff4655"}; padding:15px; margin-bottom:10px;'>
                <span style='font-size:20px; font-weight:bold;'>{row['Map'].upper()}</span> | 
                <span style='color:{"#00ff00" if row["Resultat"]=="WIN" else "#ff4655"};'>{row['Resultat']}</span> | 
                <span>SCORE: {row['Score']}</span>
            </div>
            """, unsafe_allow_html=True)

    # --- 4. TACTICAL POOL ---
    elif menu == "TACTICAL POOL":
        st.markdown("<h1 class='valo-title'>AGENT MASTERY</h1>", unsafe_allow_html=True)
        p_sel = st.selectbox("OPERATIVE", ["BOO ツ", "KURAIME"])
        cats = {
            "SENTINEL": ["Chamber", "Cypher", "Killjoy", "Sage", "Vyse", "Veto", "Deadlock"],
            "DUELIST": ["Iso", "Jett", "Neon", "Phoenix", "Raze", "Reyna", "Yoru", "Waylay"],
            "INITIATOR": ["Breach", "Fade", "Gekko", "KAY/O", "Skye", "Sova"],
            "CONTROLLER": ["Astra", "Brimstone", "Clove", "Omen", "Harbor", "Viper"]
        }
        cols = st.columns(4)
        for i, (role, agents) in enumerate(cats.items()):
            with cols[i]:
                st.markdown(f"<p style='color:#ff4655; font-weight:bold; border-bottom:1px solid #ff4655;'>{role}</p>", unsafe_allow_html=True)
                for a in agents:
                    k = f"{p_sel}_{a}"
                    cv = st.session_state['agent_data'].get(k, False)
                    res = st.checkbox(a, value=cv, key=k)
                    if res != cv:
                        st.session_state['agent_data'][k] = res
                        pd.DataFrame(list(st.session_state['agent_data'].items()), columns=['Key', 'Val']).to_csv(AGENTS_DB, index=False)

    # --- 5. PLANNING ---
    elif menu == "PLANNING":
        st.markdown("<h1 class='valo-title'>DEPLOYMENT</h1>", unsafe_allow_html=True)
        st.data_editor(pd.DataFrame({"DAY": ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"], "BOO": [""]*7, "KURAIME": [""]*7}), use_container_width=True)