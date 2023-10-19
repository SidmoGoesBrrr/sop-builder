
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
import database
import pytz
#####################################################################################################################################################
from streamlit.components.v1 import html

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
    
def send_otp(phone_no,otp):
    # url = "http://iqsms.airtel.in/api/v1/send-sms"

    # payload = {
    #     "customerId": "VIDYALANKA_cNkO5ZBR3WPzYFeg2OgB",
    #     "destinationAddress": "9321242446",
    #     "dltTemplateId": "1707169650342929076",
    #     "entityId": "1201159126160942166",
    #     "filterBlacklistNumbers": False,
    #     "message": f"{otp} is your OTP to login to Vidyalankar's AdmitAbroad webapp.",
    #     "messageType": "SERVICE_IMPLICIT",
    #     "priority": False,
    #     "sourceAddress": "IVIDYA",

    # }
    # headers = {
    #     "accept": "application/json",
    #     "content-type": "application/json"
    # }

    # response = requests.request("POST", url, json=payload, headers=headers)
    # print(response.text)
    pass

# Call the function with the OTP
im = Image.open('icon.png')
st.set_page_config(page_title="SOP Generator", page_icon=im)
if 'gen_button' not in st.session_state:
    st.session_state.disabled = True
st.header("Sign In")
username = st.text_input("Name")
phone_number = st.text_input("Mobile Number",placeholder="9631331342")
if username is not None and phone_number is not None:
    st.session_state.disabled = False
generate_otp = st.button("Generate OTP",disabled=st.session_state.disabled,key='gen_button')

if st.session_state.get('button') != True:
    st.session_state['button'] = generate_otp
    st.session_state.disabled = True

if st.session_state['button'] == True:
    st.session_state.disabled = True
    if len(phone_number)!=10 or phone_number is None:
        st.error("Sorry, not a valid phone number")
        st.session_state.disabled = False
        time.sleep(1)
        st.experimental_rerun()
    else:
        if username in [user['username'] for user in users_collection.find()] and phone_number in [user['phone_number'] for user in users_collection.find()]:
            otp = st.text_input("OTP")
            generated_otp=str(random.randint(1000, 9999))
            send_otp(phone_number,generated_otp)
            if st.button('Login'):
                if otp == "1234":
                    st.success("Logged in Successfully.")
                    st.session_state.user_logged_in = True
                    st.session_state.user_id=str(get_user_data(username)['_id'])
                    print(st.session_state.user_id)
                    ist = pytz.timezone('Asia/Kolkata')
                    time.sleep(2)
                    
                    update_user(username=username,
                                data={"last_logged_in": datetime.now(ist).strftime("%A,%d %B %Y - %H:%M:%S")})
                    nav_page("sop")
                    

                else:
                    st.error("Invalid OTP")
                    st.session_state.disabled = False
                    time.sleep(1)
                    st.experimental_rerun()
        else:
            st.error("Invalid User")
            st.session_state.disabled = False
            time.sleep(1)
            st.experimental_rerun()
