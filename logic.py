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

# --- 2. INTEL TRACKER ---
def show_intel():
    # Définition de la liste des joueurs en haut pour qu'elle soit accessible partout
    players = [
        {"label": "Boo ツ", "n": "Boo ツ", "t": "1tpas"}, 
        {"label": "Kuraime", "n": "kuraime", "t": "ezz"}, 
        {"label": "turboS", "n": "turboS", "t": "SPEED"}, 
        {"label": "Nef", "n": "Nef", "t": "SPK"},
    ]

    with st.expander("🛠️ ADMINISTRATION : MISE À JOUR MANUELLE DES RANGS"):
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            # On utilise la liste players pour remplir automatiquement le choix
            p_name = st.selectbox("Sélectionner l'unité", [p['label'] for p in players])
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

    # Affichage des cartes
    cols = st.columns(2)
    
    for i, pl in enumerate(players):
        # Utilisation du modulo % 2 pour répartir sur les 2 colonnes
        with cols[i % 2]:
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
            
            if icon: 
                st.image(icon, width=80)

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
    
    # 1. Sélection du joueur
    players_list = ["BOO ツ", "KURAIME", "TURBOS", "NEF"]
    p_sel = st.selectbox("UNIT ID", players_list)

    # 2. STYLE CSS (Glow total : Texte + Image)
    st.markdown("""
        <style>
        .agent-card {
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            transition: all 0.3s ease;
            background-color: rgba(15, 25, 35, 0.8);
            margin-bottom: 15px;
        }
        /* Couleurs demandées */
        .g-never { border: 2px solid #ffffff !important; box-shadow: 0 0 10px rgba(255,255,255,0.5); opacity: 0.5; }
        .g-test { border: 2px solid #ff4655 !important; box-shadow: 0 0 15px rgba(255,70,85,0.6); }
        .g-ok { border: 2px solid #00ff00 !important; box-shadow: 0 0 15px rgba(0,255,0,0.6); }
        .g-star { border: 2px solid #ffb000 !important; box-shadow: 0 0 20px rgba(255,176,0,0.8); }

        .agent-name-label {
            font-family: 'VALORANT', sans-serif;
            font-size: 0.85em;
            margin-bottom: 8px;
            color: white;
            font-weight: bold;
        }
        .agent-card img { border-radius: 5px; width: 100%; height: auto; display: block; object-fit: cover; }
        </style>
    """, unsafe_allow_html=True)

    # 3. Définition des catégories
    categories = {
        "🛡️ SENTINEL": {
            "Chamber": "https://images.wallpapersden.com/image/wxl-chamber-valorant-hd-cool_91233.jpg",
            "Cypher": "https://images.wallpapersden.com/image/wxl-cypher-background-valorant-art_82069.jpg",
            "Deadlock": "https://images5.alphacoders.com/139/thumb-1920-1399745.jpg",
            "Killjoy": "https://images8.alphacoders.com/114/thumb-1920-1149389.jpg",
            "Sage": "https://i.pinimg.com/1200x/fa/8d/6b/fa8d6b6cec9210cc126a947681b3077c.jpg",
            "Vyse": "https://images6.alphacoders.com/137/thumb-1920-1373943.png",
            "Veto": "https://i.ytimg.com/vi/I4T-7Kw6jKQ/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLDkzKWLj2MKubuILXFmd6avfe_1PA"
        },
        "☁️ CONTROLEUR": {
            "Astra": "https://i.pinimg.com/736x/52/96/d9/5296d9245052e767cedac9b5e100dd90.jpg",
            "Brimstone": "https://images.wallpapersden.com/image/wxl-brimstone-new-valorant-poster_72344.jpg",
            "Clove": "https://images.wallpapersden.com/image/wxl-cool-clove-4k-valorant_92740.jpg",
            "Harbor": "https://images8.alphacoders.com/128/thumb-1920-1282950.png",
            "Omen": "https://images.wallpapersden.com/image/wxl-cool-omen-valorant-2023_89545.jpg",
            "Viper": "https://images.wallpapersden.com/image/wxl-viper-4k-valorant-2020_73350.jpg"
        },
        "👁️ INITIATEUR": {
            "Breach": "https://images3.alphacoders.com/114/1149735.jpg",
            "Fade": "https://images.wallpapersden.com/image/wxl-fade-valorant-gaming-character-digital-art_91742.jpg",
            "Gekko": "https://i.pinimg.com/1200x/e8/ff/46/e8ff46efa78a7203b47f5976f72d31fb.jpg",
            "KAY/O": "https://i.pinimg.com/1200x/ef/0f/b8/ef0fb88954b5176e3c05c4811a42604e.jpg",
            "Skye": "https://images.wallpapersden.com/image/wxl-skye-art-cool-valorant_77564.jpg",
            "Sova": "https://images.wallpapersden.com/image/wxl-sova-cool-art-valorant_81600.jpg",
            "Tejo": "https://i.pinimg.com/736x/30/51/37/305137a6f4c69f7ed72d37d398fa2510.jpg"
        },
        "🔥 DUELISTER": {
            "Iso": "https://images.wallpapersden.com/image/wxl-iso-valorant-x-overwatch-2-style_91783.jpg",
            "Jett": "https://images.wallpapersden.com/image/wxl-hd-valorant-gaming-2022_85588.jpg",
            "Neon": "https://images.wallpapersden.com/image/wxl-neon-hd-valorant-nightmare_84224.jpg",
            "Phoenix": "https://images2.alphacoders.com/132/thumb-1920-1328732.png",
            "Raze": "https://images.wallpapersden.com/image/wxl-raze-new-valorant_77567.jpg",
            "Reyna": "https://i.pinimg.com/736x/c5/d1/4b/c5d14b3aa7f75ede4b527f7040556f84.jpg",
            "Yoru": "https://images.wallpapersden.com/image/wxl-yoru-fan-art-valorant_83634.jpg",
            "Waylay": "https://i.pinimg.com/736x/e0/36/37/e0363703adc24fc3b2e1dded3b563259.jpg"
        }
    }

    # Sécurité pour le stockage
    if 'agent_data' not in st.session_state:
        st.session_state['agent_data'] = {}

    # 4. LOGIQUE D'AFFICHAGE (Boucles imbriquées)
    for cat_name, agents in categories.items():
        st.markdown(f"### {cat_name}")
        cols = st.columns(4)
        
        for i, (name, img_url) in enumerate(agents.items()):
            with cols[i % 4]:
                key = f"{p_sel}_{name}"
                
                # Récupération sécurisée du niveau (0 à 3)
                raw_val = st.session_state['agent_data'].get(key, 0)
                try:
                    current_level = min(max(int(raw_val), 0), 3)
                except:
                    current_level = 0
                
                options = ["⚪ JAMAIS", "🔴 À TESTER", "🟢 OK", "🟡 MAIN"]
                classes = ["g-never", "g-test", "g-ok", "g-star"]

                # Rendu HTML de la carte
                st.markdown(f"""
                    <div class='agent-card {classes[current_level]}'>
                        <div class='agent-name-label'>{name.upper()}</div>
                        <img src="{img_url}">
                    </div>
                """, unsafe_allow_html=True)

                # Sélecteur (menu déroulant)
                new_val = st.selectbox(f"lvl_{key}", options, index=current_level, key=f"sel_{key}", label_visibility="collapsed")
                new_idx = options.index(new_val)

                # Sauvegarde si changement
                if new_idx != current_level:
                    st.session_state['agent_data'][key] = new_idx
                    save_agents_mastery(st.session_state['agent_data'])
                    st.rerun()
        st.divider()

def show_planning():
    # --- STYLE CSS AMÉLIORÉ ---
    st.markdown("""
        <style>
        .valo-card {
            background: rgba(15, 25, 35, 0.8);
            border-radius: 10px;
            border: 1px solid rgba(255, 70, 85, 0.3);
            padding: 15px;
            margin-bottom: 15px;
        }
        .player-name {
            font-family: 'VALORANT', sans-serif;
            color: #ff4655;
            font-size: 1.1em;
            margin-bottom: 5px;
        }
        .availability-text {
            color: #00ff00;
            font-family: monospace;
            font-size: 1em;
            background: rgba(0, 0, 0, 0.3);
            padding: 5px 10px;
            border-radius: 5px;
            border-left: 3px solid #00ff00;
        }
        .mission-entry {
            background: linear-gradient(90deg, rgba(255,70,85,0.05) 0%, rgba(15,25,35,0.9) 100%);
            border-left: 4px solid #ff4655;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 0 10px 10px 0;
        }
        .day-badge {
            background: #ff4655;
            color: white;
            padding: 2px 8px;
            font-size: 0.7em;
            font-weight: bold;
            border-radius: 3px;
            margin-right: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📅 OPÉRATIONS (PLANNING)", "👥 DISPONIBILITÉS SQUAD"])

    # --- ONGLET 1 : PLANNING ---
    with tab1:
        st.markdown("<h3 style='color:white; text-align:center;'>MISSION LOG</h3>", unsafe_allow_html=True)
        
        if 'planning_data' not in st.session_state: st.session_state['planning_data'] = []

        with st.expander("➕ PLANIFIER UNE OPÉRATION"):
            with st.form("new_mission_form", clear_on_submit=True):
                c1, c2, c3 = st.columns(3)
                with c1:
                    # AJOUT DU JOUR DE LA SEMAINE
                    jour_semaine = st.selectbox("JOUR", ["LUNDI", "MARDI", "MERCREDI", "JEUDI", "VENDREDI", "SAMEDI", "DIMANCHE"])
                    date_in = st.date_input("DATE")
                with c2:
                    time_in = st.text_input("HEURE", "21:00")
                    opp = st.text_input("ADVERSAIRE")
                with c3:
                    map_in = st.selectbox("MAP", ["ASCENT", "BIND", "HAVEN", "SPLIT", "ICEBOX", "BREEZE", "FRACTURE", "PEARL", "LOTUS", "SUNSET", "ABYSS", "TBD"])
                    m_type = st.selectbox("TYPE", ["SCRIM", "MATCH", "STRAT", "PRACTICE"])
                
                if st.form_submit_button("DÉPLOYER L'OPÉRATION"):
                    st.session_state['planning_data'].append({
                        "jour": jour_semaine,
                        "date": date_in.strftime("%d/%m"), 
                        "time": time_in, 
                        "opp": opp if opp else "TBD", 
                        "map": map_in, 
                        "type": m_type
                    })
                    st.rerun()

        # Affichage du planning
        if not st.session_state['planning_data']:
            st.info("Aucune mission programmée.")
        else:
            for idx, m in enumerate(st.session_state['planning_data']):
                col_m, col_d = st.columns([0.9, 0.1])
                color = "#ff4655" if m['type'] in ["MATCH", "SCRIM"] else "#00eeff"
                
                with col_m:
                    st.markdown(f"""
                        <div class="mission-entry" style="border-left-color: {color}">
                            <div style="display:flex; align-items:center; margin-bottom:5px;">
                                <span class="day-badge">{m['jour']}</span>
                                <span style="color:white; font-size:0.9em; opacity:0.8;">{m['date']} — {m['time']}</span>
                            </div>
                            <div style="color:white; font-weight:bold; font-size:1.1em;">VS {m['opp']}</div>
                            <div style="color:{color}; font-family:monospace; font-size:0.9em;">TYPE: {m['type']} | MAP: {m['map']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                with col_d:
                    st.write("##") # Calage vertical
                    if st.button("🗑️", key=f"del_{idx}"):
                        st.session_state['planning_data'].pop(idx)
                        st.rerun()

    # --- ONGLET 2 : DISPONIBILITÉS ---
    with tab2:
        st.markdown("<h3 style='color:white; text-align:center;'>SQUAD AVAILABILITY</h3>", unsafe_allow_html=True)
        
        players = ["BOO ツ", "KURAIME", "TURBOS", "NEF"]
        
        if 'dispos' not in st.session_state:
            st.session_state['dispos'] = {p: "Non renseigné" for p in players}

        cols = st.columns(2)
        for i, p in enumerate(players):
            with cols[i % 2]:
                st.markdown(f"""
                    <div class="valo-card">
                        <div class="player-name">{p}</div>
                        <div class="availability-text">{st.session_state['dispos'][p]}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                new_val = st.text_input(f"Update {p}", key=f"in_{p}", label_visibility="collapsed", placeholder="Ex: Dispo 21h...")
                if st.button(f"Confirmer {p}", key=f"btn_{p}"):
                    if new_val:
                        st.session_state['dispos'][p] = new_val.upper()
                        st.rerun()

        st.divider()
        if st.button("EFFACER TOUTES LES DISPOS", use_container_width=True):
            st.session_state['dispos'] = {p: "Non renseigné" for p in players}
            st.rerun()
def show_map_selection():
    """Affiche la grille des maps"""
    st.markdown("<h2 class='valo-title' style='text-align:center;'>SÉLECTION DE LA ZONE D'OPÉRATION</h2>", unsafe_allow_html=True)

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
        "Corrode": "https://cmsassets.rgpub.io/sanity/images/dsfx7636/news_live/6e3e66577519c8290d874aa94d82e28aec2ccc3e-915x515.jpg"
    }

    cols = st.columns(3)
    for i, (m_name, m_url) in enumerate(map_list.items()):
        with cols[i % 3]:
            st.image(m_url, use_container_width=True)
            if st.button(f"SÉLECTIONNER {m_name.upper()}", key=f"select_{m_name}", use_container_width=True):
                st.session_state['selected_strat_map'] = m_name
                st.session_state['strat_view_mode'] = "VALOPLANT"
                st.rerun()

def show_strategy_map(current_map):
    """Vue avec navigation propre et Iframe plein écran"""
    
    # Barre de navigation avec 2 colonnes pour les boutons
    nav_c1, nav_c2 = st.columns(2)
    
    if st.session_state.get('strat_view_mode') == "VALOPLANT":
        # --- MODE VALOPLANT ---
        with nav_c1:
            if st.button("⬅ QUITTER (MENU MAPS)", use_container_width=True):
                st.session_state['selected_strat_map'] = None
                st.rerun()
        with nav_c2:
            if st.button("📂 VOIR LE DOSSIER", use_container_width=True):
                st.session_state['strat_view_mode'] = "DOSSIER"
                st.rerun()
        
        # L'iframe Valoplant (la molette fonctionnera ici car le scroll global est bloqué par styles.py)
        st.components.v1.iframe("https://valoplant.gg", height=620, scrolling=True)
    
    else:
        # --- MODE DOSSIER ---
        # On débloque le scroll pour voir les images du dossier
        st.markdown("<style>.main { overflow: auto !important; }</style>", unsafe_allow_html=True)
        
        with nav_c1:
            if st.button("⬅ RETOUR MENU MAPS", use_container_width=True):
                st.session_state['selected_strat_map'] = None
                st.rerun()
        with nav_c2:
            if st.button("🌐 RETOUR VALOPLANT", use_container_width=True):
                st.session_state['strat_view_mode'] = "VALOPLANT"
                st.rerun()
        
        st.divider()
        st.markdown(f"### 📁 DOSSIER TACTIQUE : {current_map.upper()}")
        
        map_path = f"images_scrims/{current_map}"
        for side in ["Attaque", "Defense"]:
            if not os.path.exists(f"{map_path}/{side}"): 
                os.makedirs(f"{map_path}/{side}")

        with st.expander("📤 AJOUTER UNE STRATÉGIE"):
            c1, c2, c3 = st.columns([2, 1, 1])
            up_f = c1.file_uploader("Image", type=['png', 'jpg'])
            up_n = c2.text_input("Nom")
            up_s = c3.selectbox("Côté", ["Attaque", "Defense"])
            if st.button("💾 ENREGISTRER"):
                if up_f and up_n:
                    Image.open(up_f).save(f"{map_path}/{up_s}/{up_n}.png")
                    st.rerun()

        t1, t2 = st.tabs(["⚔️ ATTAQUE", "🛡️ DEFENSE"])
        for tab, side in zip([t1, t2], ["Attaque", "Defense"]):
            with tab:
                path = f"{map_path}/{side}"
                files = [f for f in os.listdir(path) if f.endswith(('.png', '.jpg'))]
                if files:
                    cols = st.columns(3)
                    for idx, f in enumerate(files):
                        with cols[idx % 3]:
                            st.image(f"{path}/{f}", use_container_width=True, caption=f.replace(".png", ""))
                            if st.button("🗑️", key=f"del_{side}_{idx}"):
                                os.remove(f"{path}/{f}")
                                st.rerun()





















