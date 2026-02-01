import streamlit as st
import pandas as pd
import os
from PIL import Image
from datetime import datetime
from database import get_intel, load_csv, save_agents_mastery, save_scrim_db, SCRIMS_DB, AGENTS_DB, update_intel_manual

# --- 1. DASHBOARD ---
def show_dashboard():
    df = st.session_state['scrims_df']
    total = len(df)
    wins = len(df[df['Resultat'] == "WIN"])
    wr = f"{(wins/total)*100:.1f}%" if total > 0 else "0.0%"
    
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f"<div class='stat-card'><h4>WINRATE</h4><h2 style='color:#ff4655;'>{wr}</h2></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='stat-card'><h4>TOTAL SCRIMS</h4><h2 style='color:#ff4655;'>{total}</h2></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='stat-card'><h4>STATUS</h4><h2 style='color:#00ff00;'>● ONLINE</h2></div>", unsafe_allow_html=True)

# --- 2. INTEL TRACKER ---
def show_intel():
    # --- AJOUT MANUEL DES RANGS ---
    with st.expander("🛠️ ADMINISTRATION : MISE À JOUR MANUELLE DES RANGS"):
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            p_name = st.selectbox("Sélectionner l'unité", ["Boo ツ", "Kuraime"])
        with col_m2:
            new_curr = st.text_input("Rang Actuel (ex: Gold 2)")
        with col_m3:
            new_peak = st.text_input("Peak Rank (ex: Platinum 1)")
        
        if st.button("FORCER LA MISE À JOUR"):
            if new_curr and new_peak:
                update_intel_manual(p_name, new_curr, new_peak)
                st.success(f"Données de {p_name} synchronisées !")
                st.rerun()
            else:
                st.error("Veuillez remplir les deux champs.")

    st.divider()

    # --- AFFICHAGE DES CARTES ---
    players = [
        {"label": "Boo ツ", "n": "Boo%20%E3%83%84", "t": "1tpas"}, 
        {"label": "Kuraime", "n": "kuraime", "t": "ezz"}
    ]
    cols = st.columns(2)
    for i, pl in enumerate(players):
        with cols[i]:
            curr, peak, icon, status = get_intel(pl['n'], pl['t'], pl['label'])
            color = "#00ff00" if "LIVE" in status else "#ff4655"
            st.markdown(f"""
                <div class='player-card'>
                    <p style='color:{color}; font-weight:bold;'>● {status}</p>
                    <h2 style='font-family:VALORANT;'>{pl['label']}</h2>
                    <p>RANK: <b style='color:#ff4655;'>{curr}</b></p>
                    <p style='font-size:0.8em; opacity:0.6;'>PEAK: {peak}</p>
                </div>
            """, unsafe_allow_html=True)
            if icon: st.image(icon, width=80)

# --- 3. MATCH ARCHIVE ---
def show_archive():
    with st.expander("➕ ENREGISTRER UN NOUVEAU SCRIM"):
        with st.form("scrim_form", clear_on_submit=True):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                m = st.selectbox("MAP", ["Abyss", "Ascent", "Bind", "Breeze", "Fracture", "Haven", "Icebox", "Lotus", "Pearl", "Split", "Sunset"])
                r = st.radio("RÉSULTAT", ["WIN", "LOSS"], horizontal=True)
            with col_f2:
                sc = st.text_input("SCORE (ex: 13-5)")
                m_file = st.file_uploader("SCREENSHOT", type=['png', 'jpg', 'jpeg'])
            
            if st.form_submit_button("SAUVEGARDER DANS LA DB"):
                img_path = "None"
                if m_file:
                    img_path = f"match_proofs/match_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    Image.open(m_file).save(img_path)
                
                new_m = {"Date": datetime.now().strftime("%d/%m/%Y"), "Map": m, "Resultat": r, "Score": sc, "Screenshot": img_path}
                st.session_state['scrims_df'] = pd.concat([pd.DataFrame([new_m]), st.session_state['scrims_df']], ignore_index=True)
                save_scrim_db(st.session_state['scrims_df'])
                st.rerun()

    if not st.session_state['scrims_df'].empty:
        to_delete = []
        st.write("### HISTORIQUE DES MISSIONS")
        for idx, row in st.session_state['scrims_df'].iterrows():
            c_sel, c1, c2, c3, c4 = st.columns([0.5, 1, 1, 1, 2])
            if c_sel.checkbox("", key=f"del_{idx}"): to_delete.append(idx)
            c1.write(row['Date'])
            c2.write(f"**{row['Map']}**")
            res_col = "#00ff00" if row['Resultat'] == "WIN" else "#ff4655"
            c3.markdown(f"<b style='color:{res_col};'>{row['Resultat']} ({row['Score']})</b>", unsafe_allow_html=True)
            if row['Screenshot'] != "None" and os.path.exists(str(row['Screenshot'])):
                c4.image(row['Screenshot'], width=200)
            st.divider()
        
        if to_delete and st.button("🗑️ SUPPRIMER LA SÉLECTION"):
            st.session_state['scrims_df'] = st.session_state['scrims_df'].drop(to_delete).reset_index(drop=True)
            save_scrim_db(st.session_state['scrims_df'])
            st.rerun()

# --- 4. TACTICAL POOL ---
def show_tactical_pool():
    p_sel = st.selectbox("AGENT OPÉRATIONNEL", ["BOO ツ", "KURAIME"])
    cats = {
        "SENTINEL": ["Chamber", "Cypher", "Killjoy", "Sage", "Vyse", "Deadlock", "Veto"], 
        "DUELIST": ["Iso", "Jett", "Neon", "Phoenix", "Raze", "Reyna", "Yoru" , "Waylay"], 
        "INITIATOR": ["Breach", "Fade", "Gekko", "KAY/O", "Skye", "Sova"], 
        "CONTROLLER": ["Astra", "Brimstone", "Clove", "Omen", "Harbor", "Viper"]
    }
    cols = st.columns(4)
    for i, (role, agents) in enumerate(cats.items()):
        with cols[i]:
            st.markdown(f"<p style='color:#ff4655; font-weight:bold; border-bottom:1px solid #ff4655;'>{role}</p>", unsafe_allow_html=True)
            for a in agents:
                k = f"{p_sel}_{a}"
                checked = st.checkbox(a, value=st.session_state['agent_data'].get(k, False), key=k)
                if checked != st.session_state['agent_data'].get(k, False):
                    st.session_state['agent_data'][k] = checked
                    save_agents_mastery(st.session_state['agent_data'])

# --- 5. PLANNING ---
def show_planning():
    st.markdown("### DISPONIBILITÉS DE L'UNITÉ")
    df_plan = pd.DataFrame({
        "JOUR": ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"], 
        "BOO": [""]*7, 
        "KURAIME": [""]*7
    })
    st.data_editor(df_plan, use_container_width=True)

# --- 6. STRATÉGIE (SÉLECTION ET AFFICHAGE) ---
def show_map_selection():
    map_list = {
        "Abyss": "https://cmsassets.rgpub.io/sanity/images/dsfx7636/news_live/53698d442a14b5a6be643d53eb970ac16442cb38-930x522.png",
        "Ascent": "https://cmsassets.rgpub.io/sanity/images/dsfx7636/news/5cb7e65c04a489eccd725ce693fdc11e99982e10-3840x2160.png",
        "Bind": "https://cmsassets.rgpub.io/sanity/images/dsfx7636/news/7df1e6ee284810ef0cbf8db369c214a8cbf6578c-3840x2160.png",
        "Breeze": "https://cmsassets.rgpub.io/sanity/images/dsfx7636/news/a4a0374222f9cc79f97e03dbb1122056e794176a-3840x2160.png",
        "Fracture": "https://cmsassets.rgpub.io/sanity/images/dsfx7636/news/aecf502b1eea8824fd1fa9f8a2450bc5c13f6910-915x515.webp",
        "Haven": "https://cmsassets.rgpub.io/sanity/images/dsfx7636/news/bccc7b5f8647a4f654d4bb359247bce6e82c77ab-3840x2160.png",
        "Icebox": "https://cmsassets.rgpub.io/sanity/images/dsfx7636/news/72853f583a0f6b25aed54870531756483a7b61de-3840x2160.png",
        "Lotus": "https://cmsassets.rgpub.io/sanity/images/dsfx7636/news/cad0b406c5924614083a8dc9846b0a8746a20bda-703x396.webp",
        "Pearl": "https://cmsassets.rgpub.io/sanity/images/dsfx7636/news/34ba319c99d3d20ef8c6f7b6a61439e207b39247-915x515.webp",
        "Split": "https://cmsassets.rgpub.io/sanity/images/dsfx7636/news/878d51688c0f9dd0de827162e80c40811668e0c6-3840x2160.png",
        "Sunset": "https://cmsassets.rgpub.io/sanity/images/dsfx7636/news/5101e4ee241fbfca261bf8150230236c46c8b991-3840x2160.png",
        "Corrode": "https://cmsassets.rgpub.io/sanity/images/dsfx7636/news_live/6e3e66577519c8290d874aa94d82e28aec2ccc3e-915x515.jpg?accountingTag=VAL&auto=format&fit=fill&q=80&w=915"
        }
    cols = st.columns(3)
    for i, (m_name, m_url) in enumerate(map_list.items()):
        with cols[i % 3]:
            st.image(m_url, use_container_width=True)
            if st.button(f"SÉLECTIONNER {m_name.upper()}", key=f"select_{m_name}"):
                st.session_state['selected_strat_map'] = m_name
                st.rerun()

def show_strategy_map(current_map):
    # 1. On affiche le bouton RETOUR en premier
    # Le CSS dans styles.py (top: 10px) s'occupera de le placer tout en haut à gauche
    if st.button("⬅ RETOUR"):
        st.session_state['selected_strat_map'] = None
        st.rerun()

    # 2. Sélecteur de mode (toujours visible pour pouvoir switcher vers les archives)
    view_mode = st.radio("INTERFACE", ["VALOPLANT LIVE", "ARCHIVES TACTIQUES"], horizontal=True, label_visibility="collapsed")
    
    if view_mode == "VALOPLANT LIVE":
        # --- MODE LIVE : On affiche uniquement l'iframe ---
        # L'iframe commence à 65px du haut grâce au CSS de styles.py pour laisser la place au bouton
        st.markdown(f"""
            <div class="iframe-container">
                <iframe src="https://valoplant.gg" 
                        allow="clipboard-read; clipboard-write" 
                        scrolling="yes">
                </iframe>
            </div>
        """, unsafe_allow_html=True)
    else:
        # --- MODE ARCHIVES : On affiche l'interface normale avec scroll ---
        st.markdown(f"### MISSION ACTIVE : {current_map.upper()}")
        
        # On réactive le scroll car les archives peuvent être longues
        st.markdown("<style>html, body, [data-testid='stAppViewContainer'] { overflow: auto !important; }</style>", unsafe_allow_html=True)
        
        map_path = f"images_scrims/{current_map}"
        for side in ["Attaque", "Defense"]:
            if not os.path.exists(f"{map_path}/{side}"): 
                os.makedirs(f"{map_path}/{side}")
        
        with st.expander("📤 AJOUTER UN DOCUMENT TACTIQUE"):
            col_u1, col_u2, col_u3 = st.columns([2, 1, 1])
            up_file = col_u1.file_uploader("Image", type=['png', 'jpg'])
            up_name = col_u2.text_input("Nom de la strat")
            up_side = col_u3.selectbox("Côté", ["Attaque", "Defense"])
            if st.button("ENREGISTRER STRAT"):
                if up_file and up_name:
                    Image.open(up_file).save(f"{map_path}/{up_side}/{up_name}.png")
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
                else: 
                    st.info(f"Aucune archive pour {side}")

