import streamlit as st
from styles import apply_global_styles, apply_immersive_mode
from database import init_folders, load_csv, SCRIMS_DB, AGENTS_DB
import logic

# --- CONFIGURATION INITIALE ---
st.set_page_config(
    page_title="CRIMSON PROTOCOL v2", 
    layout="wide", 
    page_icon="🩸",
    initial_sidebar_state="collapsed"
)

# Initialisation des dossiers (images, csv)
init_folders()

# Application du design global Valorant
apply_global_styles()

# --- GESTION DE LA SESSION (ÉTAT DE L'APP) ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "DASHBOARD"

if 'selected_strat_map' not in st.session_state:
    st.session_state['selected_strat_map'] = None

# Chargement des bases de données dans la session
if 'scrims_df' not in st.session_state:
    st.session_state['scrims_df'] = load_csv(SCRIMS_DB, ["Date", "Map", "Resultat", "Score", "Screenshot"])

if 'agent_data' not in st.session_state:
    import os
    import pandas as pd
    if os.path.exists(AGENTS_DB):
        df_ag = pd.read_csv(AGENTS_DB)
        st.session_state['agent_data'] = dict(zip(df_ag.Key, df_ag.Val))
    else:
        st.session_state['agent_data'] = {}

# --- SYSTÈME D'ACCÈS (LOGIN) ---
if not st.session_state["logged_in"]:
    st.markdown("<div style='margin-top:80px;'></div>", unsafe_allow_html=True)
    st.markdown("<h1 class='valo-title'>CRIMSON ACCESS</h1>", unsafe_allow_html=True)
    
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        u_id = st.text_input("UNIT ID", placeholder="Email...")
        u_key = st.text_input("ENCRYPTION KEY", type="password", placeholder="Password...")
        
        if st.button("INITIALIZE SYSTEM"):
            if u_id == "titi12012008@gmail.com" and u_key == "Tn12janv2008":
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error("ACCESS DENIED: Invalid Encryption Key")

# --- INTERFACE PRINCIPALE (SI CONNECTÉ) ---
else:
    # 1. Vérification du mode Immersif (Page Stratégie + Map sélectionnée)
    is_strat_page = st.session_state["current_page"] == "STRATÉGIE"
    has_map_selected = st.session_state['selected_strat_map'] is not None
    
    if is_strat_page and has_map_selected:
        # On applique le CSS qui cache tout l'UI Streamlit
        apply_immersive_mode()
        
        # On affiche uniquement le bouton de sortie en haut
        if st.button("⬅ EXIT IMMERSIVE MODE"):
            st.session_state['selected_strat_map'] = None
            st.rerun()
            
        # Affichage de Valoplant ou des Archives (via logic.py)
        logic.show_strategy_map(st.session_state['selected_strat_map'])

    else:
        # 2. Affichage du Menu Normal Crimson HQ
        st.markdown("<h1 class='valo-title'>CRIMSON HQ</h1>", unsafe_allow_html=True)
        
        # Barre de navigation horizontale
        m_cols = st.columns([1, 1, 1, 1, 1, 1, 0.5])
        pages = ["DASHBOARD", "INTEL TRACKER", "MATCH ARCHIVE", "TACTICAL POOL", "PLANNING", "STRATÉGIE"]
        
        for idx, p_name in enumerate(pages):
            if m_cols[idx].button(p_name, use_container_width=True):
                st.session_state["current_page"] = p_name
                st.session_state['selected_strat_map'] = None # Reset si on change de page
                st.rerun()
        
        # Bouton de déconnexion
        if m_cols[6].button("✖"):
            st.session_state["logged_in"] = False
            st.rerun()
        
        st.divider()

        # 3. Routage vers les fonctions de logic.py
        menu = st.session_state["current_page"]
        
        if menu == "DASHBOARD":
            logic.show_dashboard()
        
        elif menu == "INTEL TRACKER":
            logic.show_intel()
            
        elif menu == "MATCH ARCHIVE":
            logic.show_archive()
            
        elif menu == "TACTICAL POOL":
            logic.show_tactical_pool()
            
        elif menu == "PLANNING":
            logic.show_planning()
            
        elif menu == "STRATÉGIE":
            # Si aucune map n'est choisie, on affiche la sélection
            logic.show_map_selection()
