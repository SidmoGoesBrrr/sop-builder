import streamlit as st
from pymongo import MongoClient
import time
import database

def display_drafts_page():
    st.header("Drafts")
    updated_draft = database.get_user_data_by_id(st.session_state.user_id)['draft']
    if updated_draft:
        for draft in updated_draft[::-1]:
            st.write(draft)
            st.write("-----------------------------------------------------------------------------------------------")
    while not st.button("Back"):
        time.sleep(3)

if st.session_state.get("user_logged_in") == True:
    display_drafts_page()
else:
    st.error("⚠️ You need to login to access this feature! Please log in. ⚠️")