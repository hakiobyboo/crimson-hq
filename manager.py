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

# --- GESTION DE LA SESSION (AVANT LE CSS) ---
if 'scrims_df' not in st.session_state: st.session_state['scrims_df'] = load_csv(SCRIMS_DB, ["Date", "Map", "Resultat", "Score", "Screenshot"])
if 'agent_data' not in st.session_state:
    if os.path.exists(AGENTS_DB):
        df_ag = pd.read_csv(AGENTS_DB)
        st.session_state['agent_data'] = dict(zip(df_ag.Key, df_ag.Val))
    else: st.session_state['agent_data'] = {}
if 'selected_strat_map' not in st.session_state: st.session_state['selected_strat_map'] = None
if 'archive_view' not in st.session_state: st.session_state['archive_view'] = False
if "logged_in" not in st.session_state: st.session_state["logged_in"] = False
if "current_page" not in st.session_state: st.session_state["current_page"] = "DASHBOARD"

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
    }

    div.stButton > button {
        background-color: transparent;
        color: #ece8e1;
        font-family: 'VALORANT', sans-serif;
        border: 2px solid #ff4655;
        clip-path: polygon(10% 0, 100% 0, 100% 70%, 90% 100%, 0 100%, 0 30%);
        transition: 0.3s;
        width: 100%;
    }

    div.stButton > button:hover {
        background-color: #ff4655;
        color: white;
        box-shadow: 0px 0px 15px #ff4655;
    }

    .iframe-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        height: 88vh;
    }

    .stat-card {
        background: linear-gradient(135deg, rgba(255, 70, 85, 0.1) 0%, rgba(15, 25, 35, 0.9) 100%);
        border-left: 5px solid #ff4655;
        padding: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. ECRAN DE CONNEXION ---
if not st.session_state["logged_in"]:
    st.markdown("<div style='margin-top:80px;'></div>", unsafe_allow_html=True)
    st.markdown("<h1 class='valo-title'>CRIMSON ACCESS</h1>", unsafe_allow_html=True)
    
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        u_id = st.text_input("UNIT ID", placeholder="Votre email...")
        u_key = st.text_input("ENCRYPTION KEY", type="password", placeholder="Mot de passe...")
        if st.button("INITIALIZE SYSTEM"):
            if u_id == "titi12012008@gmail.com" and u_key == "Tn12janv2008":
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error("ACCÈS REFUSÉ : Identifiants invalides.")

# --- 2. INTERFACE PRINCIPALE (UNIQUEMENT SI CONNECTÉ) ---
else:
    # --- GESTION DE L'IMMERSION ---
    is_immersive = (
        st.session_state["current_page"] == "STRATÉGIE" and 
        st.session_state['selected_strat_map'] is not None and 
        not st.session_state['archive_view']
    )

    if is_immersive:
        # On cache tout sauf le bouton retour personnalisé
        st.markdown("""
            <style>
            header, [data-testid="stHeader"], .valo-title, hr, .stDivider { display: none !important; }
            .main .block-container { padding-top: 0rem !important; padding-bottom: 0rem !important; max-width: 100% !important; }
            </style>
        """, unsafe_allow_html=True)
        
        if st.button("⬅ QUITTER LE MODE IMMERSIF"):
            st.session_state['selected_strat_map'] = None
            st.rerun()
    else:
        # Menu Standard
        st.markdown("<h1 class='valo-title'>CRIMSON HQ</h1>", unsafe_allow_html=True)
        m_cols = st.columns([1, 1, 1, 1, 1, 1, 0.5])
        pages = ["DASHBOARD", "INTEL TRACKER", "MATCH ARCHIVE", "TACTICAL POOL", "PLANNING", "STRATÉGIE"]
        
        for idx, p_name in enumerate(pages):
            if m_cols[idx].button(p_name, use_container_width=True):
                st.session_state["current_page"] = p_name
                st.session_state['selected_strat_map'] = None
                st.session_state['archive_view'] = False
                st.rerun()
        
        if m_cols[6].button("✖"):
            st.session_state["logged_in"] = False
            st.rerun()
        
        st.divider()

    menu = st.session_state["current_page"]

    # --- ROUTAGE DES PAGES ---
    if menu == "DASHBOARD":
        df = st.session_state['scrims_df']
        total = len(df); wins = len(df[df['Resultat'] == "WIN"])
        wr = f"{(wins/total)*100:.1f}%" if total > 0 else "0.0%"
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"<div class='stat-card'><h4>WINRATE</h4><h2 style='color:#ff4655;'>{wr}</h2></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='stat-card'><h4>TOTAL SCRIMS</h4><h2 style='color:#ff4655;'>{total}</h2></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='stat-card'><h4>STATUS</h4><h2 style='color:#00ff00;'>● ONLINE</h2></div>", unsafe_allow_html=True)

    elif menu == "INTEL TRACKER":
        players = [{"label": "Boo ツ", "n": "Boo%20%E3%83%84", "t": "1tpas"}, {"label": "Kuraime", "n": "kuraime", "t": "ezz"}]
        cols = st.columns(2)
        for i, pl in enumerate(players):
            with cols[i]:
                curr, peak, icon, status = get_intel(pl['n'], pl['t'], pl['label'])
                st.markdown(f"<div style='background:#1f2326; padding:20px; text-align:center; border-top: 3px solid #ff4655;'><h2>{pl['label']}</h2><p>RANK: <b style='color:#ff4655;'>{curr}</b></p></div>", unsafe_allow_html=True)
                if icon: st.image(icon, width=80)

    elif menu == "MATCH ARCHIVE":
        with st.expander("📝 ENREGISTRER UN SCRIM"):
            with st.form("scrim_form", clear_on_submit=True):
                m = st.selectbox("MAP", ["Abyss", "Ascent", "Bind", "Breeze", "Fracture", "Haven", "Icebox", "Lotus", "Pearl", "Split", "Sunset"])
                r = st.radio("RESULTAT", ["WIN", "LOSS"], horizontal=True)
                sc = st.text_input("SCORE (ex: 13-5)")
                m_file = st.file_uploader("CAPTURE D'ÉCRAN", type=['png', 'jpg'])
                if st.form_submit_button("SAUVEGARDER"):
                    img_path = "None"
                    if m_file:
                        img_path = f"match_proofs/match_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                        Image.open(m_file).save(img_path)
                    new_m = {"Date": datetime.now().strftime("%d/%m/%Y"), "Map": m, "Resultat": r, "Score": sc, "Screenshot": img_path}
                    st.session_state['scrims_df'] = pd.concat([pd.DataFrame([new_m]), st.session_state['scrims_df']], ignore_index=True)
                    st.session_state['scrims_df'].to_csv(SCRIMS_DB, index=False)
                    st.rerun()

        if not st.session_state['scrims_df'].empty:
            to_del = []
            st.write("### HISTORIQUE")
            for idx, row in st.session_state['scrims_df'].iterrows():
                c_sel, c1, c2, c3, c4 = st.columns([0.5, 1, 1, 1, 2])
                if c_sel.checkbox("", key=f"del_{idx}"): to_del.append(idx)
                c1.write(row['Date'])
                c2.write(f"**{row['Map']}**")
                c3.write(f"[{row['Resultat']}] {row['Score']}")
                if row['Screenshot'] != "None": c4.image(row['Screenshot'], width=150)
                st.divider()
            if to_del and st.button("🗑️ SUPPRIMER LES MATCHS SÉLECTIONNÉS"):
                st.session_state['scrims_df'] = st.session_state['scrims_df'].drop(to_del).reset_index(drop=True)
                st.session_state['scrims_df'].to_csv(SCRIMS_DB, index=False)
                st.rerun()

    elif menu == "TACTICAL POOL":
        p_sel = st.selectbox("SÉLECTIONNER L'OPÉRATEUR", ["BOO ツ", "KURAIME"])
        cats = {
            "SENTINEL": ["Chamber", "Cypher", "Killjoy", "Sage", "Vyse", "Deadlock"],
            "DUELIST": ["Jett", "Raze", "Neon", "Reyna", "Iso", "Phoenix", "Yoru"],
            "INITIATOR": ["Sova", "Skye", "Gekko", "Fade", "Breach", "KAY/O"],
            "CONTROLLER": ["Omen", "Clove", "Viper", "Brimstone", "Astra", "Harbor"]
        }
        cols = st.columns(4)
        for i, (role, agents) in enumerate(cats.items()):
            with cols[i]:
                st.markdown(f"### {role}")
                for a in agents:
                    k = f"{p_sel}_{a}"
                    st.session_state['agent_data'][k] = st.checkbox(a, value=st.session_state['agent_data'].get(k, False), key=k)
        
        if st.button("💾 SAUVEGARDER LA MAÎTRISE"):
            pd.DataFrame(list(st.session_state['agent_data'].items()), columns=['Key', 'Val']).to_csv(AGENTS_DB, index=False)
            st.success("Données sauvegardées.")

    elif menu == "PLANNING":
        st.markdown("### EMPLOI DU TEMPS")
        st.data_editor(pd.DataFrame({"JOUR": ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"], "BOO": [""]*7, "KURAIME": [""]*7}), use_container_width=True)

    elif menu == "STRATÉGIE":
        if st.session_state['selected_strat_map'] is None:
            # Choix de la map
            maps = ["Abyss", "Ascent", "Bind", "Breeze", "Fracture", "Haven", "Icebox", "Lotus", "Pearl", "Split", "Sunset"]
            cols = st.columns(4)
            for i, m_name in enumerate(maps):
                if cols[i % 4].button(m_name.upper(), use_container_width=True):
                    st.session_state['selected_strat_map'] = m_name
                    st.rerun()
        else:
            current_map = st.session_state['selected_strat_map']
            
            # Barre de contrôle
            if not is_immersive:
                c_nav1, c_nav2, c_nav3 = st.columns([1, 4, 1])
                with c_nav1:
                    if st.button("⬅ RETOUR"):
                        st.session_state['selected_strat_map'] = None
                        st.rerun()
                with c_nav2:
                    st.markdown(f"<h3 style='text-align:center; color:#ff4655;'>MISSION : {current_map.upper()}</h3>", unsafe_allow_html=True)
                with c_nav3:
                    st.session_state['archive_view'] = st.toggle("📁 DOSSIER", value=st.session_state['archive_view'])

            if st.session_state['archive_view']:
                # Mode Dossier de Stratégies
                map_path = f"images_scrims/{current_map}"
                for side in ["Attaque", "Defense"]:
                    if not os.path.exists(f"{map_path}/{side}"): os.makedirs(f"{map_path}/{side}")
                
                with st.expander("💾 AJOUTER UNE STRATÉGIE"):
                    col_u1, col_u2, col_u3 = st.columns([2, 1, 1])
                    uploaded_file = col_u1.file_uploader("Image", type=['png', 'jpg'])
                    custom_name = col_u2.text_input("Nom")
                    side_choice = col_u3.selectbox("Côté", ["Attaque", "Defense"])
                    if st.button("ENREGISTRER"):
                        if uploaded_file and custom_name:
                            Image.open(uploaded_file).save(f"{map_path}/{side_choice}/{custom_name}.png")
                            st.rerun()

                t1, t2 = st.tabs(["⚔️ ATTAQUE", "🛡️ DEFENSE"])
                for tab, side in zip([t1, t2], ["Attaque", "Defense"]):
                    with tab:
                        files = os.listdir(f"{map_path}/{side}")
                        if files:
                            cols_f = st.columns(3)
                            for idx, f in enumerate(files):
                                with cols_f[idx % 3]:
                                    st.image(f"{map_path}/{side}/{f}", caption=f.replace(".png", ""), use_container_width=True)
                                    if st.button("🗑️", key=f"del_{side}_{idx}"):
                                        os.remove(f"{map_path}/{side}/{f}")
                                        st.rerun()
                        else: st.info("Aucun document dans ce dossier.")
            else:
                # Mode Valoplant Plein Écran
                st.markdown(f"""
                    <div class="iframe-wrapper">
                        <iframe src="https://valoplant.gg" width="95%" height="100%" style="border: 2px solid #ff4655; border-radius: 15px; background: white;"></iframe>
                    </div>
                """, unsafe_allow_html=True)
