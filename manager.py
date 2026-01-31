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
if not os.path.exists("match_proofs"):
    os.makedirs("match_proofs")

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
    except:
        pass
    
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
        background-image: radial-gradient(circle at 2px 2px, rgba(255, 70, 85, 0.05) 1px, transparent 0);
        background-size: 40px 40px;
        color: #ece8e1;
        font-family: 'Rajdhani', sans-serif;
    }

    .valo-title {
        font-family: 'VALORANT', sans-serif;
        color: #ff4655;
        font-size: 50px;
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 0px 0px 20px rgba(255, 70, 85, 0.5);
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

    .stat-card {
        background: linear-gradient(135deg, rgba(255, 70, 85, 0.1) 0%, rgba(15, 25, 35, 0.9) 100%);
        border-left: 5px solid #ff4655;
        padding: 20px;
        border-radius: 0px 10px 10px 0px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- GESTION DE LA SESSION ---
if 'scrims_df' not in st.session_state:
    st.session_state['scrims_df'] = load_csv(SCRIMS_DB, ["Date", "Map", "Resultat", "Score", "Screenshot"])
if 'agent_data' not in st.session_state:
    if os.path.exists(AGENTS_DB):
        df_ag = pd.read_csv(AGENTS_DB)
        st.session_state['agent_data'] = dict(zip(df_ag.Key, df_ag.Val))
    else:
        st.session_state['agent_data'] = {}
if 'selected_strat_map' not in st.session_state:
    st.session_state['selected_strat_map'] = None
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# --- LOGIQUE D'ACCÈS ---
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
    # --- NAVIGATION ---
    st.sidebar.markdown("<h2 style='text-align:center; color:#ff4655; font-family:VALORANT;'>CRIMSON HQ</h2>", unsafe_allow_html=True)
    menu = st.sidebar.radio("SQUAD TERMINAL", ["DASHBOARD", "INTEL TRACKER", "MATCH ARCHIVE", "TACTICAL POOL", "PLANNING", "STRATÉGIE"])
    
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

    # --- 2. INTEL TRACKER ---
    elif menu == "INTEL TRACKER":
        st.markdown("<h1 class='valo-title'>SQUAD INTEL</h1>", unsafe_allow_html=True)
        
        with st.expander("🛠️ ÉDITION MANUELLE DU RANG"):
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1: p_name = st.selectbox("Joueur", ["Boo ツ", "Kuraime"])
            with col_m2: new_curr = st.text_input("Actual Rank")
            with col_m3: new_peak = st.text_input("Peak Rank")
            if st.button("FORCER LA MISE À JOUR"):
                old_df = load_csv(RANKS_DB, ["Player", "Current", "Peak"])
                manual_data = pd.DataFrame([{"Player": p_name, "Current": new_curr, "Peak": new_peak}])
                pd.concat([old_df[old_df['Player'] != p_name], manual_data], ignore_index=True).to_csv(RANKS_DB, index=False)
                st.success("Données mises à jour !")
                st.rerun()

        players = [{"label": "Boo ツ", "n": "Boo%20%E3%83%84", "t": "1tpas"}, {"label": "Kuraime", "n": "kuraime", "t": "ezz"}]
        cols = st.columns(2)
        for i, pl in enumerate(players):
            with cols[i]:
                curr, peak, icon, status = get_intel(pl['n'], pl['t'], pl['label'])
                color = "#00ff00" if status == "LIVE" else "#ff4655"
                st.markdown(f"""
                    <div style='background:#1f2326; padding:20px; border-radius:4px; text-align:center; border-top: 3px solid #ff4655;'>
                        <p style='color:{color};'>● {status}</p>
                        <h2>{pl['label']}</h2>
                        <p>RANK: <b style='color:#ff4655;'>{curr}</b></p>
                        <p style='font-size:0.8em; opacity:0.6;'>PEAK: {peak}</p>
                    </div>
                """, unsafe_allow_html=True)
                if icon: st.image(icon, width=80)

    # --- 3. MATCH ARCHIVE (MISE À JOUR AVEC SUPPRESSION COCHÉE) ---
    elif menu == "MATCH ARCHIVE":
        st.markdown("<h1 class='valo-title'>MATCH LOGS</h1>", unsafe_allow_html=True)
        with st.expander("ADD NEW SCRIM"):
            with st.form("scrim_form", clear_on_submit=True):
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    m = st.selectbox("MAP", ["Abyss", "Ascent", "Bind", "Breeze", "Fracture", "Haven", "Icebox", "Lotus", "Pearl", "Split", "Sunset"])
                    r = st.radio("RESULT", ["WIN", "LOSS"], horizontal=True)
                with col_f2:
                    sc = st.text_input("SCORE (ex: 13-5)")
                    m_file = st.file_uploader("SCREENSHOT DU MATCH", type=['png', 'jpg', 'jpeg'])
                
                if st.form_submit_button("SAVE"):
                    img_path = "None"
                    if m_file:
                        img_path = f"match_proofs/match_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                        Image.open(m_file).save(img_path)
                    
                    new_m = {"Date": datetime.now().strftime("%d/%m/%Y"), "Map": m, "Resultat": r, "Score": sc, "Screenshot": img_path}
                    st.session_state['scrims_df'] = pd.concat([pd.DataFrame([new_m]), st.session_state['scrims_df']], ignore_index=True)
                    st.session_state['scrims_df'].to_csv(SCRIMS_DB, index=False)
                    st.rerun()

        st.write("### HISTORY")
        if not st.session_state['scrims_df'].empty:
            to_delete = []
            h_cols = st.columns([0.5, 1, 1, 1, 1, 2])
            h_cols[0].write("**SEL.**")
            h_cols[1].write("**DATE**")
            h_cols[2].write("**MAP**")
            h_cols[3].write("**RESULT**")
            h_cols[4].write("**SCORE**")
            h_cols[5].write("**SCREENSHOT**")
            st.markdown("---")

            for idx, row in st.session_state['scrims_df'].iterrows():
                c_sel, c1, c2, c3, c4, c5 = st.columns([0.5, 1, 1, 1, 1, 2])
                if c_sel.checkbox("", key=f"del_scrim_{idx}"):
                    to_delete.append(idx)
                c1.write(row['Date'])
                c2.write(row['Map'])
                res_color = "#00ff00" if row['Resultat'] == "WIN" else "#ff4655"
                c3.markdown(f"<b style='color:{res_color};'>{row['Resultat']}</b>", unsafe_allow_html=True)
                c4.write(row['Score'])
                if row['Screenshot'] != "None" and os.path.exists(str(row['Screenshot'])):
                    c5.image(row['Screenshot'], use_container_width=True)
                else:
                    c5.write("No image")
                st.divider()

            if to_delete:
                if st.button("🗑️ SUPPRIMER LES PRACCS SÉLECTIONNÉES"):
                    for i in to_delete:
                        path = st.session_state['scrims_df'].iloc[i]['Screenshot']
                        if path != "None" and os.path.exists(str(path)):
                            os.remove(path)
                    st.session_state['scrims_df'] = st.session_state['scrims_df'].drop(to_delete).reset_index(drop=True)
                    st.session_state['scrims_df'].to_csv(SCRIMS_DB, index=False)
                    st.rerun()
        else:
            st.info("Aucun match archivé.")

    # --- 4. TACTICAL POOL ---
    elif menu == "TACTICAL POOL":
        st.markdown("<h1 class='valo-title'>AGENT MASTERY</h1>", unsafe_allow_html=True)
        p_sel = st.selectbox("OPERATIVE", ["BOO ツ", "KURAIME"])
        cats = {
            "SENTINEL": ["Chamber", "Cypher", "Killjoy", "Sage", "Vyse", "Deadlock"], 
            "DUELIST": ["Iso", "Jett", "Neon", "Phoenix", "Raze", "Reyna", "Yoru"], 
            "INITIATOR": ["Breach", "Fade", "Gekko", "KAY/O", "Skye", "Sova"], 
            "CONTROLLER": ["Astra", "Brimstone", "Clove", "Omen", "Harbor", "Viper"]
        }
        cols = st.columns(4)
        for i, (role, agents) in enumerate(cats.items()):
            with cols[i]:
                st.markdown(f"<p style='color:#ff4655; border-bottom:1px solid #ff4655; font-weight:bold;'>{role}</p>", unsafe_allow_html=True)
                for a in agents:
                    k = f"{p_sel}_{a}"
                    res = st.checkbox(a, value=st.session_state['agent_data'].get(k, False), key=k)
                    if res != st.session_state['agent_data'].get(k, False):
                        st.session_state['agent_data'][k] = res
                        pd.DataFrame(list(st.session_state['agent_data'].items()), columns=['Key', 'Val']).to_csv(AGENTS_DB, index=False)

    # --- 5. PLANNING ---
    elif menu == "PLANNING":
        st.markdown("<h1 class='valo-title'>DEPLOYMENT</h1>", unsafe_allow_html=True)
        st.data_editor(pd.DataFrame({"DAY": ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"], "BOO": [""]*7, "KURAIME": [""]*7}), use_container_width=True)

    # --- 6. STRATÉGIE (MISE À JOUR NOMMAGE + SUPPRESSION) ---
    elif menu == "STRATÉGIE":
        map_list = {
            "Abyss": "https://cmsassets.rgpub.io/sanity/images/dsfx7636/news_live/53698d442a14b5a6be643d53eb970ac16442cb38-930x522.png?accountingTag=VAL&auto=format&fit=fill&q=80&w=930",
            "Ascent": "https://cmsassets.rgpub.io/sanity/images/dsfx7636/news/5cb7e65c04a489eccd725ce693fdc11e99982e10-3840x2160.png?accountingTag=VAL&auto=format&fit=fill&q=80&w=1240",
            "Bind": "https://cmsassets.rgpub.io/sanity/images/dsfx7636/news/7df1e6ee284810ef0cbf8db369c214a8cbf6578c-3840x2160.png?accountingTag=VAL&auto=format&fit=fill&q=80&w=1240",
            "Breeze": "https://cmsassets.rgpub.io/sanity/images/dsfx7636/news/a4a0374222f9cc79f97e03dbb1122056e794176a-3840x2160.png?accountingTag=VAL&auto=format&fit=fill&q=80&w=1240",
            "Fracture":"https://cmsassets.rgpub.io/sanity/images/dsfx7636/news/aecf502b1eea8824fd1fa9f8a2450bc5c13f6910-915x515.webp?accountingTag=VAL&auto=format&fit=fill&q=80&w=915",
            "Haven": "https://cmsassets.rgpub.io/sanity/images/dsfx7636/news/bccc7b5f8647a4f654d4bb359247bce6e82c77ab-3840x2160.png?accountingTag=VAL&auto=format&fit=fill&q=80&w=1240",
            "Icebox": "https://cmsassets.rgpub.io/sanity/images/dsfx7636/news/72853f583a0f6b25aed54870531756483a7b61de-3840x2160.png?accountingTag=VAL&auto=format&fit=fill&q=80&w=1240",
            "Lotus": "https://cmsassets.rgpub.io/sanity/images/dsfx7636/news/cad0b406c5924614083a8dc9846b0a8746a20bda-703x396.webp?accountingTag=VAL&auto=format&fit=fill&q=80&w=703",
            "Pearl": "https://cmsassets.rgpub.io/sanity/images/dsfx7636/news/34ba319c99d3d20ef8c6f7b6a61439e207b39247-915x515.webp?accountingTag=VAL&auto=format&fit=fill&q=80&w=915",
            "Split": "https://cmsassets.rgpub.io/sanity/images/dsfx7636/news/878d51688c0f9dd0de827162e80c40811668e0c6-3840x2160.png?accountingTag=VAL&auto=format&fit=fill&q=80&w=1240",
            "Sunset": "https://cmsassets.rgpub.io/sanity/images/dsfx7636/news/5101e4ee241fbfca261bf8150230236c46c8b991-3840x2160.png?accountingTag=VAL&auto=format&fit=fill&q=80&w=1240",
            "Corode": "https://cmsassets.rgpub.io/sanity/images/dsfx7636/news_live/6e3e66577519c8290d874aa94d82e28aec2ccc3e-915x515.jpg?accountingTag=VAL&auto=format&fit=fill&q=80&w=915"
        }

        if st.session_state['selected_strat_map'] is None:
            st.markdown("<h1 class='valo-title'>TACTICAL PLANNER</h1>", unsafe_allow_html=True)
            cols = st.columns(4)
            for i, (m_name, m_url) in enumerate(map_list.items()):
                with cols[i % 4]:
                    st.image(m_url, use_container_width=True)
                    if st.button(f"{m_name.upper()}", key=f"btn_{m_name}"):
                        st.session_state['selected_strat_map'] = m_name
                        st.rerun()
        else:
            st.markdown("<style>.block-container { padding-top: 0.5rem !important; max-width: 98% !important; } header { visibility: hidden; }</style>", unsafe_allow_html=True)
            
            col_L, col_M, col_R = st.columns([1, 3, 1])
            with col_L:
                if st.button("⬅ RETOUR"):
                    st.session_state['selected_strat_map'] = None
                    st.rerun()
            with col_M:
                current_map = st.session_state['selected_strat_map']
                st.markdown(f"<h3 style='text-align:center; color:#ff4655;'>MISSION : {current_map.upper()}</h3>", unsafe_allow_html=True)
            with col_R:
                deploy_mode = st.toggle("📂 ARCHIVES & DEPLOY")

            if deploy_mode:
                st.markdown(f"#### 📁 Dossier Tactique : {current_map}")
                map_folder = f"images_scrims/{current_map}"
                if not os.path.exists(map_folder):
                    os.makedirs(map_folder)

                # --- ZONE D'UPLOAD AVEC NOMMAGE ---
                with st.container(border=True):
                    col_u1, col_u2 = st.columns([2, 1])
                    with col_u1:
                        uploaded_file = st.file_uploader("Screenshot Valoplant", type=['png', 'jpg', 'jpeg'])
                    with col_u2:
                        custom_name = st.text_input("NOMMER LA STRAT", placeholder="ex: Execute A Rapide")
                    
                    if st.button("💾 ENREGISTRER LA STRATÉGIE"):
                        if uploaded_file and custom_name:
                            # Nettoyage du nom pour éviter les erreurs de fichier
                            clean_name = "".join(x for x in custom_name if x.isalnum() or x in "._- ")
                            img = Image.open(uploaded_file)
                            img.save(f"{map_folder}/{clean_name}.png")
                            st.success(f"Stratégie '{clean_name}' enregistrée !")
                            st.rerun()
                        else:
                            st.error("Veuillez remplir le nom et choisir un fichier.")

                # --- GALERIE AVEC BOUTON DE SUPPRESSION ---
                strats = os.listdir(map_folder)
                if strats:
                    st.write("---")
                    cols_img = st.columns(3)
                    for idx, s in enumerate(reversed(strats)):
                        with cols_img[idx % 3]:
                            st.image(f"{map_folder}/{s}", caption=s.replace(".png", ""), use_container_width=True)
                            if st.button("🗑️ Supprimer", key=f"del_strat_{idx}"):
                                os.remove(f"{map_folder}/{s}")
                                st.rerun()
            else:
                st.markdown(
                    f'<div style="display: flex; justify-content: center; width: 100%; height: 85vh;">'
                    f'<iframe src="https://valoplant.gg" width="100%" height="100%" style="border: 2px solid #ff4655; border-radius:10px;"></iframe>'
                    f'</div>', 
                    unsafe_allow_html=True
                )
