import streamlit as st
import pandas as pd
import os

# 1. CONFIGURATION (Impérativement en premier)
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
    st.error(f"Erreur d'importation : {e}. Vérifiez que styles.py et database.py sont présents.")

# 3. INITIALISATION DU SYSTÈME
if 'scrims_df' not in st.session_state:
    st.session_state['scrims_df'] = load_csv(SCRIMS_DB, ["Date", "Map", "Resultat", "Score", "Screenshot"])

# Initialisation des variables de session pour éviter les crashs (KeyError)
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = True

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "DASHBOARD"

if 'compo_save' not in st.session_state:
    st.session_state['compo_save'] = {} # Correction pour le bug Team Builder

if 'selected_strat_map' not in st.session_state:
    st.session_state['selected_strat_map'] = None

# Chargement automatique des données pour le graphique de Winrate
if 'planning_df' not in st.session_state:
    st.session_state['planning_df'] = load_csv(PLANNING_DB, ["jour", "opp", "Resultat"])

# 4. INTERFACE UTILISATEUR
is_strat = st.session_state["current_page"] == "STRATÉGIE"
is_map_sel = st.session_state.get('selected_strat_map') is not None

# CAS A : MODE STRATÉGIE IMMERSIF (Plein écran)
if is_strat and is_map_sel:
    apply_immersive_mode()
    logic.show_strategy_map(st.session_state['selected_strat_map'])

# CAS B : INTERFACE NORMALE HQ
else:
    # Titre principal stylisé
    st.markdown("<h1 class='valo-title'>CRIMSON</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; letter-spacing:10px; color:#666; margin-top:-40px; margin-bottom:40px;'>ELITE TACTICAL INTERFACE</p>", unsafe_allow_html=True)

    # Menu de Navigation Horizontal
    pages = ["DASHBOARD", "MAPS & COMPOS", "MATCH ARCHIVE", "TACTICAL POOL", "PLANNING", "STRATÉGIE"]
    cols = st.columns(len(pages))
    
    for i, p in enumerate(pages):
        if cols[i].button(p, key=f"btn_{p}", use_container_width=True):
            st.session_state["current_page"] = p
            # Reset de la map sélectionnée si on change de page
            if p != "STRATÉGIE":
                st.session_state['selected_strat_map'] = None
            st.rerun()

    st.divider()

    # ROUTAGE DES PAGES
    menu = st.session_state["current_page"]
    
    if menu == "DASHBOARD":
        logic.show_dashboard()
    elif menu == "MAPS & COMPOS":
        logic.show_team_builder() # Utilise l'initialisation 'compo_save' faite plus haut
    elif menu == "MATCH ARCHIVE":
        logic.show_archive()
    elif menu == "TACTICAL POOL":
        logic.show_tactical_pool()
    elif menu == "PLANNING":
        logic.show_planning()
    elif menu == "STRATÉGIE":
        logic.show_map_selection()

