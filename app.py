import streamlit as st
import pandas as pd
import os

# 1. CONFIGURATION (UNIQUE ET EN PREMIER)
st.set_page_config(
    page_title="CRIMSON HQ", 
    layout="wide", 
    page_icon="🩸",
    initial_sidebar_state="collapsed"
)

# 2. IMPORTS DES MODULES
try:
    from styles import apply_global_styles, apply_immersive_mode
    from database import init_folders, load_csv, SCRIMS_DB, AGENTS_DB, PLANNING_DB
    import logic
except ImportError as e:
    st.error(f"Erreur d'importation : {e}. Vérifiez que database.py contient bien 'PLANNING_DB'.")

# 3. INITIALISATION DU SYSTÈME
init_folders()
apply_global_styles()

# Initialisation des variables de session (évite les KeyError)
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = True

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "DASHBOARD"

if 'compo_save' not in st.session_state:
    st.session_state['compo_save'] = {}

if 'selected_strat_map' not in st.session_state:
    st.session_state['selected_strat_map'] = None

# Chargement des données pour le dashboard
if 'scrims_df' not in st.session_state:
    st.session_state['scrims_df'] = load_csv(SCRIMS_DB, ["Date", "Map", "Resultat", "Score"])

if 'planning_df' not in st.session_state:
    # On utilise PLANNING_DB qui doit être défini dans database.py
    st.session_state['planning_df'] = load_csv(PLANNING_DB, ["jour", "opp", "Resultat"])

# 4. LOGIQUE D'AFFICHAGE
is_strat = st.session_state["current_page"] == "STRATÉGIE"
is_map_sel = st.session_state.get('selected_strat_map') is not None

# CAS A : MODE STRATÉGIE IMMERSIF
if is_strat and is_map_sel:
    apply_immersive_mode()
    logic.show_strategy_map(st.session_state['selected_strat_map'])

# CAS B : INTERFACE NORMALE HQ
else:
    st.markdown("<h1 class='valo-title'>CRIMSON</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; letter-spacing:10px; color:#666; margin-top:-40px; margin-bottom:40px;'>ELITE TACTICAL INTERFACE</p>", unsafe_allow_html=True)

    # Menu de Navigation Horizontal
    pages = ["DASHBOARD", "MAPS & COMPOS", "MATCH ARCHIVE", "TACTICAL POOL", "PLANNING", "STRATÉGIE"]
    cols = st.columns(len(pages))

    for i, p in enumerate(pages):
        if cols[i].button(p, key=f"btn_{p}", use_container_width=True):
            st.session_state["current_page"] = p
            if p != "STRATÉGIE":
                st.session_state['selected_strat_map'] = None
            st.rerun()

    st.divider()

    # ROUTAGE DES PAGES
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
