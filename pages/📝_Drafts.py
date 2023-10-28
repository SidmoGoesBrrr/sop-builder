# import streamlit as st
# from pymongo import MongoClient
# import time
# import database
# from PIL import Image
# im = Image.open('icon.png')

# st.set_page_config(page_title="SOP Generator", page_icon=im)

# def display_drafts_page():
#     st.header("Drafts")
#     print(st.session_state.user_id)
#     try:
#         updated_draft = database.get_user_data_by_id(st.session_state.user_id)['drafts']
#         print(updated_draft)
#     except:
#         updated_draft = None
#     if updated_draft is not None:
#         for draft in updated_draft[::-1]:
#             st.write(draft)
#             st.write("-----------------------------------------------------------------------------------------------")
#     elif updated_draft.strip() == "":
#         st.info("No drafts found!")

#     else:
#         st.info("No drafts found!")


# if st.session_state.get("user_logged_in") == True:
#     display_drafts_page()
# else:
#     st.error("⚠️ You need to login to access this feature! Please log in. ⚠️")
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
    table_data = []
    for draft in drafts:
        university_name = draft.get('University Name', 'N/A')
        program_name = draft.get('Program Name', 'N/A')
        date_of_draft = draft.get('Date of Draft', 'N/A')
        time_stamp = draft.get('Time Stamp', 'N/A')
        view_draft_link = st.button("View Draft")
        table_data.append([university_name, program_name, date_of_draft, time_stamp, view_draft_link])

    # Define column names for the table
    columns = ["University Name", "Program Name", "Date of Draft", "Time Stamp", "View Draft"]

    return [columns] + table_data

# Check if the user is logged in and display drafts if logged in
if st.session_state.get("user_logged_in") == True:
    display_drafts_page()
else:
    st.error("⚠️ You need to log in to access this feature. Please log in. ⚠️")
