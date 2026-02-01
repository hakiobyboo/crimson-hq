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
                    if not os.path.exists("match_proofs"): os.makedirs("match_proofs")
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
    st.markdown("<h2 class='valo-title' style='text-align:center;'>AGENT POOL PAR RÔLE</h2>", unsafe_allow_html=True)
    p_sel = st.selectbox("UNIT ID", ["BOO ツ", "KURAIME"])

    categories = {
        "🛡️ SENTINEL": {
            "Chamber": "https://media.valorant-api.com/agents/22697a3d-45bf-8dd7-4f03-10a07d64f12f/fullportrait.png",
            "Cypher": "https://media.valorant-api.com/agents/117ed9d3-4836-2473-3e7b-5d1073097510/fullportrait.png",
            "Deadlock": "https://media.valorant-api.com/agents/cc8b6900-45c0-11ff-3136-32a2405c56b4/fullportrait.png",
            "Killjoy": "https://media.valorant-api.com/agents/1e58de9d-4950-5125-93e9-a0aee9f97661/fullportrait.png",
            "Sage": "https://media.valorant-api.com/agents/569fdd95-4d0f-5d54-963f-8b1167b43f92/fullportrait.png",
            "Vyse": "https://media.valorant-api.com/agents/6c368297-4c4c-4740-4965-74892c9082fd/fullportrait.png",
            "Veto": "https://media.valorant-api.com/agents/6a928e08-466d-55e1-807e-9786a5df9b6e/fullportrait.png"
        },
        "☁️ CONTROLEUR": {
            "Astra": "https://media.valorant-api.com/agents/41fb69c1-4189-7b37-f117-bc3596b3a1c1/fullportrait.png",
            "Brimstone": "https://media.valorant-api.com/agents/9ad6e251-4199-1392-8a0a-559b9bb1b13a/fullportrait.png",
            "Clove": "https://media.valorant-api.com/agents/bb2a14ca-4614-4690-8805-776732644265/fullportrait.png",
            "Harbor": "https://media.valorant-api.com/agents/95b5b8d0-4c7a-b64d-7603-9ce1f6d4ad48/fullportrait.png",
            "Omen": "https://media.valorant-api.com/agents/8e253930-4c0d-4a5d-13a3-33318f73b981/fullportrait.png",
            "Viper": "https://media.valorant-api.com/agents/707eab51-4836-f488-046a-cda6bf348ad8/fullportrait.png",
            "Tejo": "https://media.valorant-api.com/agents/dad62021-4fec-586b-715a-b98a3330f69a/fullportrait.png"
        },
        "👁️ INITIATEUR": {
            "Breach": "https://media.valorant-api.com/agents/5f8d3a7f-467b-97f3-062c-13acf203c002/fullportrait.png",
            "Fade": "https://media.valorant-api.com/agents/dade69b4-4354-453d-9152-87569175927c/fullportrait.png",
            "Gekko": "https://media.valorant-api.com/agents/e370fa57-4757-3604-3644-49ba1543f2a8/fullportrait.png",
            "KAY/O": "https://media.valorant-api.com/agents/601db300-4316-2969-808b-ce5ad40616a1/fullportrait.png",
            "Skye": "https://media.valorant-api.com/agents/6f2a0491-44a3-42a3-274f-bc3596b3a1c1/fullportrait.png",
            "Sova": "https://media.valorant-api.com/agents/320b2a48-4d9b-a075-3bca-14ac10b24036/fullportrait.png",
            "Waylay": "https://media.valorant-api.com/agents/6a2b8e01-466a-55a1-807a-9786a5df9b6e/fullportrait.png"
        },
        "🔥 DUELISTER": {
            "Iso": "https://media.valorant-api.com/agents/0e314694-4c11-daa7-33d3-c99026774e44/fullportrait.png",
            "Jett": "https://media.valorant-api.com/agents/ad3e3391-4351-b13e-f117-bc3596b3a1c1/fullportrait.png",
            "Neon": "https://media.valorant-api.com/agents/bb2a14ca-4614-4690-8805-776732644265/fullportrait.png",
            "Phoenix": "https://media.valorant-api.com/agents/eb93336a-449b-9c1b-ce31-2924316e6d78/fullportrait.png",
            "Raze": "https://media.valorant-api.com/agents/f944b06d-4a4d-8170-9d11-bc3596b3a1c1/fullportrait.png",
            "Reyna": "https://media.valorant-api.com/agents/a3bc0630-404a-b565-d5b7-bc3596b3a1c1/fullportrait.png",
            "Yoru": "https://media.valorant-api.com/agents/7f94d92c-4234-8836-96ff-bc3596b3a1c1/fullportrait.png"
        }
    }

    for cat_name, agents in categories.items():
        st.markdown(f"#### {cat_name}")
        cols = st.columns(4)
        for i, (name, img_url) in enumerate(agents.items()):
            with cols[i % 4]:
                key = f"{p_sel}_{name}"
                is_mastered = st.session_state.get('agent_data', {}).get(key, False)
                
                border = "2px solid #ff4655" if is_mastered else "1px solid #333"
                bg_color = "rgba(255, 70, 85, 0.1)" if is_mastered else "transparent"
                
                st.markdown(f"""
                    <div style="border: {border}; background-color: {bg_color}; padding: 5px; border-radius: 5px; text-align: center; margin-bottom: 5px;">
                        <p style="margin: 0; font-weight: bold; font-size: 0.7em; color: white;">{name.upper()}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                st.image(img_url, use_container_width=True)
                
                if st.button("MASTER" if not is_mastered else "UNMARK", key=f"btn_{key}", use_container_width=True):
                    if 'agent_data' not in st.session_state: st.session_state['agent_data'] = {}
                    st.session_state['agent_data'][key] = not is_mastered
                    save_agents_mastery(st.session_state['agent_data'])
                    st.rerun()
        st.divider()

# --- 5. PLANNING ---
def show_planning():
    st.markdown("### DISPONIBILITÉS DE L'UNITÉ")
    df_plan = pd.DataFrame({
        "JOUR": ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"], 
        "BOO": [""]*7, 
        "KURAIME": [""]*7
    })
    st.data_editor(df_plan, use_container_width=True)

# --- 6. STRATÉGIE ---
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
    # --- BARRE DE NAVIGATION SUPÉRIEURE ---
    col_nav1, col_nav2, col_nav3 = st.columns([1, 1, 1])
    
    with col_nav1:
        if st.button("⬅ RETOUR", use_container_width=True):
            st.session_state['selected_strat_map'] = None
            st.rerun()
            
    # Initialisation du mode si non présent
    if 'strat_view_mode' not in st.session_state:
        st.session_state['strat_view_mode'] = "DOSSIER"

    with col_nav2:
        if st.button("📂 DOSSIER", use_container_width=True):
            st.session_state['strat_view_mode'] = "DOSSIER"
            st.rerun()

    with col_nav3:
        if st.button("🌐 VALOPLANT", use_container_width=True):
            st.session_state['strat_view_mode'] = "VALOPLANT"
            st.rerun()

    st.divider()

    # --- AFFICHAGE DU CONTENU ---
    if st.session_state['strat_view_mode'] == "VALOPLANT":
        # MODE LIVE : L'iframe Valoplant
        st.markdown(f"""
            <div class="iframe-container">
                <iframe src="https://valoplant.gg" 
                        allow="clipboard-read; clipboard-write" 
                        scrolling="yes" style="width:100%; height:80vh; border:none;">
                </iframe>
            </div>
        """, unsafe_allow_html=True)
    
    else:
        # MODE DOSSIER : Ton système de gestion de maps
        st.markdown(f"### 📍 ARCHIVES : {current_map.upper()}")
        
        map_path = f"images_scrims/{current_map}"
        # Création des dossiers si besoin
        for side in ["Attaque", "Defense"]:
            if not os.path.exists(f"{map_path}/{side}"): 
                os.makedirs(f"{map_path}/{side}")
        
        # Formulaire d'upload
        with st.expander("📤 AJOUTER UNE STRATÉGIE (IMAGE)"):
            col_u1, col_u2, col_u3 = st.columns([2, 1, 1])
            up_file = col_u1.file_uploader("Choisir l'image", type=['png', 'jpg'])
            up_name = col_u2.text_input("Nom (ex: Split A)")
            up_side = col_u3.selectbox("Côté", ["Attaque", "Defense"])
            if st.button("SAUVEGARDER"):
                if up_file and up_name:
                    Image.open(up_file).save(f"{map_path}/{up_side}/{up_name}.png")
                    st.success(f"Strat {up_name} enregistrée !")
                    st.rerun()

        # Onglets Attaque / Défense
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
                    st.info(f"Aucune stratégie enregistrée pour le côté {side}")
