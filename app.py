import streamlit as st
import pandas as pd
import os

# --- 1. CONFIGURATION DE LA PAGE (DOIT ÊTRE EN PREMIER) ---
st.set_page_config(
    page_title="CRIMSON PROTOCOL v2", 
    layout="wide", 
    page_icon="🩸",
    initial_sidebar_state="collapsed"
)

# --- 2. IMPORTS DES MODULES ---
# Assure-toi que ces fonctions existent dans tes fichiers respectifs
from styles import apply_global_styles, apply_immersive_mode
from database import init_folders, load_csv, SCRIMS_DB, AGENTS_DB
import logic

# --- 3. INITIALISATION DES SYSTÈMES ---
init_folders()
apply_global_styles() # Applique le look "Cyber-Esport"

# --- 4. GESTION DE LA SESSION ---
# Accès automatique (On saute le login)
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = True

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "DASHBOARD"

if 'selected_strat_map' not in st.session_state:
    st.session_state['selected_strat_map'] = None

if 'strat_view_mode' not in st.session_state:
    st.session_state['strat_view_mode'] = "VALOPLANT"

# Chargement des données
if 'scrims_df' not in st.session_state:
    st.session_state['scrims_df'] = load_csv(SCRIMS_DB, ["Date", "Map", "Resultat", "Score", "Screenshot"])

if 'agent_data' not in st.session_state:
    if os.path.exists(AGENTS_DB):
        df_ag = pd.read_csv(AGENTS_DB)
        st.session_state['agent_data'] = dict(zip(df_ag.Key, df_ag.Val))
    else:
        st.session_state['agent_data'] = {}

# --- 5. INTERFACE HQ ---

# Variables de contrôle pour le mode stratégie immersif
is_strat_page = st.session_state["current_page"] == "STRATÉGIE"
has_map_selected = st.session_state['selected_strat_map'] is not None

# CAS A : MODE STRATÉGIE IMMERSIF (Sans menu)
if is_strat_page and has_map_selected:
    if st.session_state.get('strat_view_mode') == "VALOPLANT":
        apply_immersive_mode() 
    logic.show_strategy_map(st.session_state['selected_strat_map'])

# CAS B : INTERFACE HQ NORMALE
else:
    # Grand Titre Crimson
    st.markdown("<h1 class='valo-title'>CRIMSON</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; letter-spacing:10px; color:#666; margin-top:-40px; margin-bottom:40px;'>ELITE TACTICAL INTERFACE</p>", unsafe_allow_html=True)
    
    # Barre de Menu (Navigation)
    pages = ["DASHBOARD", "MAPS & COMPOS", "MATCH ARCHIVE", "TACTICAL POOL", "PLANNING", "STRATÉGIE"]
    m_cols = st.columns(len(pages))
    
    for idx, p_name in enumerate(pages):
        if m_cols[idx].button(p_name, key=f"nav_{p_name}", use_container_width=True):
            st.session_state["current_page"] = p_name
            st.session_state['selected_strat_map'] = None # Reset si on quitte la strat
            st.rerun()
    
    st.divider() # Ligne stylisée rouge
    
    # Routage vers les pages
    menu = st.session_state["current_page"]
    
    if menu == "DASHBOARD":
        logic.show_dashboard()
    elif menu == "MAPS & COMPOS":
        logic.show_team_builder() 
    elif menu == "MATCH ARCHIVE":
        logic.show_archive()
    elif menu == "TACTICAL POOL":
        logic.show_tactical_pool()
    elif menu == "PLANNING":
        logic.show_planning()
    elif menu == "STRATÉGIE":
        logic.show_map_selection()
