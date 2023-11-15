import logging
import streamlit as st
from pymongo import MongoClient
import time
import database
import pytz
from datetime import datetime
import random
import streamlit as st
import pandas as pd
from PIL import Image

im = Image.open('icon.png')

# Function to display the payment page
def display_payment_page():
    # Razorpay payment link
    payment_link = "https://rzp.io/l/aasopbuilder"
    if 'waiting_for_payment' not in st.session_state:
        st.session_state.waiting_for_payment = False
    # Displaying the payment button

    if "payment_successful" not in st.session_state:
        st.session_state.payment_successful = False
    
    if st.button('Buy Credits'):
        # Open the payment link in a new tab
        st.link_button("Pay Now", payment_link,type="secondary",)
        # Set a flag indicating the payment process has started
        st.session_state['waiting_for_payment'] = True
        st.info("⏳ Waiting for payment...")
        # Redirect to the payment page
        while st.session_state['waiting_for_payment']:
            sheet_url = pd.read_csv("https://docs.google.com/spreadsheets/d/1rs4dVdlLXi8c3kN0pRRegu-gKjIH6j1gw_3pyGUZJo0/export?gid=719810628&format=csv",
                                    index_col=1)
            logging.info(sheet_url)
            logging.info(sheet_url.index)
            sop_db_ph_no=database.get_user_data_by_id(st.session_state.user_id).get("phone_number", 0)
            razorpay_created_at=sheet_url.loc[sop_db_ph_no, 'Created At']
            created_at_datetime = datetime.fromtimestamp(razorpay_created_at, tz=pytz.UTC)

            # Get the current time in UTC
            current_datetime_utc = datetime.now(pytz.UTC)

            # Calculate the time difference in seconds
            time_difference = (current_datetime_utc - created_at_datetime).total_seconds()
            logging.info(time_difference)
            logging.info(sop_db_ph_no)
            logging.info(sheet_url.loc)
            
            # check if there is the required phone number in the sheet and if yes, check payment status of that phone number
            if sop_db_ph_no in sheet_url.index and time_difference < 180: #3 minutes
                payment_status = sheet_url.loc[database.get_user_data_by_id(st.session_state.user_id).get("phone_number", 0), "Payment Status"]
                # Strip whitespace and newline characters from the payment status
                payment_status = payment_status.strip()

                if payment_status == "captured paid":
                    st.session_state['waiting_for_payment'] = False
                    st.session_state['payment_successful'] = True
                    # Update the user's SOP credits
                    user_data = database.get_user_data_by_id(st.session_state.user_id)
                    user_data['SOP_CREDITS'] += 99
                    database.update_user(user_data['username'], user_data)
                    st.success("🎉 Congratulations! You have successfully purchased 99 SOP credit. You can now create 1 SOP draft. 🎉")
                    st.balloons()
                    st.info("🔥 You can also view your SOP draft by clicking on the 'Drafts' button on the sidebar. 🔥")
                    break

                elif payment_status == "failed":
                    st.session_state['waiting_for_payment'] = False
                    st.error("⚠️ Payment failed. Please try again. ⚠️")
                    break

if st.session_state.get("user_logged_in"):
    display_payment_page()
else:
    st.error("⚠️ You need to log in to access this feature. Please log in. ⚠️")
