import logging
import streamlit as st
from pymongo import MongoClient
import time
import database
from PIL import Image

# Load the icon image
im = Image.open('icon.png')

# Set Streamlit page configuration
st.set_page_config(page_title="SOP Generator", page_icon=im)

# Define a function to display drafts in a table
def display_drafts_page():
    st.header("Drafts")
    user_id = st.session_state.user_id
    try:
        user_data = database.get_user_data_by_id(user_id)
        drafts = user_data.get('drafts', [])

        if drafts:
            st.table(drafts_to_table(drafts))
        else:
            st.info("No drafts found!")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def drafts_to_table(drafts):
    # Create a table from the list of drafts
    logging.info(f"Drafts: {drafts}")
    user_data = database.get_user_data_by_id(st.session_state.user_id)
    table_data = []
    for draft in drafts:
        university_name = draft.get('University Name', user_data['university'])
        program_name = draft.get('Program Name', user_data['program']) #Saturday,28 October 2023 - 20:33:59
        date_of_draft = draft.get('Date of Draft', draft['timestamp'].split('-')[0])
        time_stamp = draft.get('Time', draft['timestamp'].split('-')[1])
        table_data.append([university_name, program_name, date_of_draft, time_stamp, st.button("View Draft",key=drafts.index(draft))])

    # Define column names for the table
    columns = ["University Name", "Program Name", "Date of Draft", "Time Stamp", "View Draft"]

    return [columns] + table_data

# Check if the user is logged in and display drafts if logged in
if st.session_state.get("user_logged_in") == True:
    display_drafts_page()
else:
    st.error("⚠️ You need to log in to access this feature. Please log in. ⚠️")
