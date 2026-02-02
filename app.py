import streamlit as st
import pandas as pd
import os

# 1. CONFIGURATION (TOUJOURS EN PREMIER)
st.set_page_config(page_title="CRIMSON HQ", layout="wide", page_icon="🩸")

# 2. IMPORTS
from styles import apply_global_styles, apply_immersive_mode
from database import init_folders, load_csv, SCRIMS_DB, AGENTS_DB
import logic

# 3. INITIALISATION
init_folders()
apply_global_styles()

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "DASHBOARD"
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = True

# 4. INTERFACE
is_strat = st.session_state["current_page"] == "STRATÉGIE"
is_map_sel = st.session_state.get('selected_strat_map') is not None

if is_strat and is_map_sel:
    apply_immersive_mode()
    logic.show_strategy_map(st.session_state['selected_strat_map'])
else:
    st.markdown("<h1 class='valo-title'>CRIMSON</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; letter-spacing:10px; color:#666; margin-top:-40px; margin-bottom:40px;'>ELITE TACTICAL INTERFACE</p>", unsafe_allow_html=True)

    # Menu de Navigation
    pages = ["DASHBOARD", "MAPS & COMPOS", "MATCH ARCHIVE", "TACTICAL POOL", "PLANNING", "STRATÉGIE"]
    cols = st.columns(len(pages))
    
    for i, p in enumerate(pages):
        if cols[i].button(p, key=f"btn_{p}", use_container_width=True):
            st.session_state["current_page"] = p
            st.rerun()

    st.divider()

    # Routage
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
