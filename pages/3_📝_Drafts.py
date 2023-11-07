import logging
import streamlit as st
from pymongo import MongoClient
import time
import database
from PIL import Image

# Define a function to display drafts in a table
def display_drafts_page():
    st.header("Drafts")
    user_data = database.get_user_data_by_id(st.session_state.user_id)
    drafts = user_data.get('drafts', [])
    if drafts:
        for i, draft in enumerate(drafts, start=1):
            university_name = draft.get('University Name', user_data['university'])
            program_name = draft.get('Program Name', user_data['program'])
            date_of_draft = draft.get('Date of Draft', draft['timestamp'].split('-')[0])
            time_stamp = draft.get('Time', draft['timestamp'].split('-')[1])

            st.subheader(f"Draft {i}")
            st.text(f"University Name: {university_name}")
            st.text(f"Program Name: {program_name}")
            st.text(f"Date of Draft: {date_of_draft}")
            st.text(f"Time Stamp: {time_stamp}")
            
            if st.button(f"View Draft {i}"):
                view_individual_draft(i, draft['content'])

    else:
        st.info("No drafts found!")

def view_individual_draft(draft_id, draft_content):
    st.header(f"Draft {draft_id}")
    st.subheader("Here is your draft:")
    # draw a divider
    st.markdown("---")
    st.write(draft_content)
    st.markdown("---")

# Check if the user is logged in and display drafts if logged in
if st.session_state.get("user_logged_in") == True:
    display_drafts_page()
else:
    st.error("⚠️ You need to log in to access this feature. Please log in. ⚠️")
