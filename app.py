import streamlit as st
from styles import apply_global_styles, apply_immersive_mode
from database import init_folders, load_csv, SCRIMS_DB, AGENTS_DB
import logic
import pandas as pd
import os

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="CRIMSON PROTOCOL v2", 
    layout="wide", 
    page_icon="🩸",
    initial_sidebar_state="collapsed"
)

# Initialisation des systèmes
init_folders()
apply_global_styles()

# --- 2. GESTION DE LA SESSION ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = True

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "DASHBOARD"

if 'selected_strat_map' not in st.session_state:
    st.session_state['selected_strat_map'] = None

if 'strat_view_mode' not in st.session_state:
    st.session_state['strat_view_mode'] = "VALOPLANT"

if 'scrims_df' not in st.session_state:
    st.session_state['scrims_df'] = load_csv(SCRIMS_DB, ["Date", "Map", "Resultat", "Score", "Screenshot"])

if 'agent_data' not in st.session_state:
    if os.path.exists(AGENTS_DB):
        df_ag = pd.read_csv(AGENTS_DB)
        st.session_state['agent_data'] = dict(zip(df_ag.Key, df_ag.Val))
    else:
        st.session_state['agent_data'] = {}

# --- 3. SYSTÈME D'ACCÈS (LOGIN) ---
if not st.session_state["logged_in"]:
    st.markdown("<div style='margin-top:80px;'></div>", unsafe_allow_html=True)
    st.markdown("<h1 class='valo-title'>CRIMSON ACCESS</h1>", unsafe_allow_html=True)
    
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        u_id = st.text_input("UNIT ID", placeholder="Email...")
        u_key = st.text_input("ENCRYPTION KEY", type="password", placeholder="Password...")
        
        if st.button("INITIALIZE SYSTEM", use_container_width=True):
            if u_id == "La Twin Sparks" and u_key == "Crimson":
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error("ACCESS DENIED: Invalid Encryption Key")

# --- 4. INTERFACE PRINCIPALE (SI CONNECTÉ) ---
else:
    # Variables de contrôle
    is_strat_page = st.session_state["current_page"] == "STRATÉGIE"
    has_map_selected = st.session_state['selected_strat_map'] is not None
    
    # --- CAS A : NAVIGATION DANS UNE MAP (MODE IMMERSIF) ---
    if is_strat_page and has_map_selected:
        if st.session_state.get('strat_view_mode') == "VALOPLANT":
            apply_immersive_mode() 
        
        logic.show_strategy_map(st.session_state['selected_strat_map'])

    # --- CAS B : INTERFACE HQ NORMALE ---
    else:
        st.markdown("<h1 class='valo-title'>CRIMSON HQ</h1>", unsafe_allow_html=True)
        
        # Barre de Menu (Navigation)
        m_cols = st.columns([1, 1, 1, 1, 1, 1, 0.5])
        pages = ["DASHBOARD", "MAPS & COMPOS", "MATCH ARCHIVE", "TACTICAL POOL", "PLANNING", "STRATÉGIE"]
        
        for idx, p_name in enumerate(pages):
            if m_cols[idx].button(p_name, key=f"nav_{p_name}", use_container_width=True):
                st.session_state["current_page"] = p_name
                st.session_state['selected_strat_map'] = None
                st.session_state['strat_view_mode'] = "VALOPLANT"
                st.rerun()
        
# --- ROUTAGE VERS LES PAGES ---
        menu = st.session_state["current_page"]
        
        if menu == "DASHBOARD":
            logic.show_dashboard()
        elif menu == "MAPS & COMPOS":
            logic.show_team_builder()  # Appelle la nouvelle interface avec les agents
        elif menu == "MATCH ARCHIVE":
            logic.show_archive()
        elif menu == "TACTICAL POOL":
            logic.show_tactical_pool()
        elif menu == "PLANNING":
            logic.show_planning()
        elif menu == "STRATÉGIE":
            if st.session_state['selected_strat_map'] is None:
                logic.show_map_selection()










