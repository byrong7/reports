import streamlit as st
import pandas as pd
from io import BytesIO
import requests
import os
PASSWORD = os.environ.get("APP_PASS", "")
URL = os.environ.get("APP_CSV", "")




df = pd.read_csv(URL)
# =============================================================================
# =============================================================================
# =============================================================================
# # # 
# =============================================================================
# =============================================================================
# =============================================================================

# === Ρυθμίσεις σελίδας ===
st.set_page_config(page_title="B2B Report", layout="wide")

    

# Αν δεν έχει εγκριθεί πρόσβαση ακόμα
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Αν δεν είναι authenticated, εμφάνισε το login
if not st.session_state.authenticated:
    password = st.text_input("Enter password:", type="password")
    if password == PASSWORD:
        st.session_state.authenticated = True
        st.rerun()

    elif password:
        st.error("Wrong password")
if st.session_state.authenticated:
        
    st.title("B2B Reports")
    # === Sidebar Filters ===
    st.sidebar.markdown("## Select Owner")
    
    owners = df["OWNER"].dropna().unique().tolist()
    
    # Session state to preserve selection
    if "selected_owners" not in st.session_state:
        st.session_state.selected_owners = []
    
    
    # Owner Buttons
    for owner in owners:
        if st.sidebar.button(f"{owner}"):
            if owner not in st.session_state.selected_owners:
                st.session_state.selected_owners = []
                st.session_state.selected_owners.append(owner)
    # Clear Filters Button
    if st.sidebar.button("Clear Filters"):
        st.session_state.selected_owners = []
    
    # If no selection, show all
    selected_owners = st.session_state.selected_owners or owners
    filtered_df = df[df["OWNER"].isin(selected_owners)]
    
    # === Make Links Clickable ===
    def make_clickable(link, label):
        if isinstance(link, str) and link.startswith("http"):
            return f'<a href="{link}" target="_blank">{label}</a>'
        return label
    
    display_df = filtered_df.copy()
    display_df["LINK"] = [
        make_clickable(link, "Open") for link in display_df["LINK"]
    ]
    
    # === Show Table ===
    st.markdown("""
        <style>
        table th {
            text-align: left !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # === Εμφάνιση πίνακα ===
    st.markdown("### Report Table")
    st.write(display_df.to_html(escape=False, index=False), unsafe_allow_html=True)
    
    # === Stats ===
    st.markdown("#### Total Records:")
    st.write(len(display_df))
