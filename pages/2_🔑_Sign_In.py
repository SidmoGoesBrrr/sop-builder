import random
from pymongo import MongoClient
from datetime import datetime
from PIL import Image
import requests
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import time
import database
from database import get_user_data, update_user
import pytz
import streamlit as st
import os
from streamlit.components.v1 import html


@st.cache_resource(ttl=1200)
def get_users_collection():
    users_collection = database.users_collection
    return users_collection


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


def send_otp(phone_number, generated_otp):
    url = 'https://iqsms.airtel.in/api/v1/send-sms'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': st.secrets["sms_auth"],
    }

    data = {
        "customerId": st.secrets["customerId"],
        "destinationAddress": f"{str(phone_number)}",
        "message": f"{str(generated_otp)} is your OTP to login to Vidyalankar's AdmitAbroad webapp.",
        "sourceAddress": "IVIDYA",
        "messageType": "SERVICE_EXPLICIT",
        "dltTemplateId": st.secrets["dltTemplateId"],
        "entityId": st.secrets["entityId"]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("Request was successful.")
        print("Response content:")
        print(response.text)
    else:
        print(f"Request failed with status code {response.status_code}:")
        print(response.text)


# Call the function with the OTP
im = Image.open('icon.png')

st.set_page_config(page_title="SOP Generator", page_icon=im)

if 'gen_button' not in st.session_state:
    st.session_state.disabled = True
if 'login_button' not in st.session_state:
    st.session_state.login_button = True
st.header("Sign In")
username = st.text_input("Name")
phone_number = st.text_input("Mobile Number", placeholder="9631331342")
if username is not None and phone_number is not None:
    st.session_state.disabled = False

generate_otp = st.button("Generate OTP", disabled=st.session_state.disabled, key='gen_button')


if generate_otp:
    st.session_state.disabled = False
    if len(phone_number) != 10 or phone_number is None:
        st.error("Sorry, not a valid phone number")

    else:
        users_collection = get_users_collection()
        if username in [user['username'] for user in users_collection.find()] and phone_number in [user['phone_number']
                                                                                                   for user in
                                                                                                   users_collection.find()]:
            st.session_state.generated_otp = random.randint(1000, 9999)
            time.sleep(1)
            send_otp(phone_number, st.session_state.generated_otp)
            time.sleep(5)
            st.success("OTP sent successfully")
            st.session_state.login_button = False
        else:
            st.error("Invalid User")
            st.session_state.disabled = False
            time.sleep(1)

if not st.session_state.login_button:
    otp = st.text_input("Enter OTP", key='otp')
    if st.button('Login'):
        print(otp, st.session_state.generated_otp)
        if otp == str(st.session_state.generated_otp):
            st.success("Logged in Successfully.")
            st.session_state.user_logged_in = True
            st.session_state.user_id = str(get_user_data(username)['_id'])
            print(st.session_state.user_id)
            ist = pytz.timezone('Asia/Kolkata')

            update_user(username=username,
                        data={"last_logged_in": datetime.now(ist).strftime("%A,%d %B %Y - %H:%M:%S")})
            os.rename(r'pages/2_🔑_Sign_In.py', r'lages/2_🔑_Sign_In.py')
            os.rename(r'lages/2_🔑_Sign_Out.py', r'pages/2_🔑_Sign_Out.py')
            nav_page("")

        else:
            st.error("Invalid OTP")
            st.session_state.disabled = False
            time.sleep(1)
