
import streamlit as st
import random
from pymongo import MongoClient
from datetime import datetime
import os
from PIL import Image
from database import *
import requests
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import time
from streamlit.components.v1 import html

#####################################################################################################################################################
im = Image.open('icon.png')
st.set_page_config(page_title="SOP Generator", page_icon=im)
st.header("Sign Up")

def nav_page(page_name, timeout_secs=3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)


# Get user inputs
username = st.text_input("Name")
email = st.text_input("Email")
phone_number = st.text_input("Mobile Number")

# Check if phone number is 10 digits and name is not blank
phone_number_valid = phone_number.isdigit() and len(phone_number) == 10
name_valid = bool(username)
if st.button("Sign Up"):
    if not phone_number_valid:
        st.error("Mobile Number must be 10 digits.")
    
    if not name_valid:
        st.error("Name cannot be blank.")

    if name_valid and phone_number_valid:
        user = get_user_data(username)
        if username in [user['username'] for user in users_collection.find()]:
            st.error("User Already registered. Please Sign In.")
        else:
            create_user(username, email, phone_number)
            st.success("User registered successfully. Please Sign In")
            time.sleep(2)
            st.session_state.user_logged_in = True
            nav_page("sop")
            st.session_state.user_id=str(get_user_data(username)['_id'])
            