
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
            
            