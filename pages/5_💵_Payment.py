import logging
import streamlit as st
from pymongo import MongoClient
import time
import database
import random
import streamlit as st
import pandas as pd


# Function to display the payment page
def display_payment_page():
    # Razorpay payment link
    payment_link = "https://rzp.io/l/aasopbuilder"
    if 'waiting_for_payment' not in st.session_state:
        st.session_state.waiting_for_payment = False
    # Displaying the payment button

    if "payment_successful" not in st.session_state:
        st.session_state.payment_successful = False
    
    if st.button('Pay Now To Get SOP Credits'):
        # Open the payment link in a new tab
        st.markdown(f"<a href='{payment_link}' target='_blank'>Click here to complete the payment</a>", unsafe_allow_html=True)
        # Set a flag indicating the payment process has started
        st.session_state['waiting_for_payment'] = True
        st.info("⏳ Waiting for payment...")
        # Redirect to the payment page
        while st.session_state['waiting_for_payment']:
            sheet_url = pd.read_csv("https://docs.google.com/spreadsheets/d/1rs4dVdlLXi8c3kN0pRRegu-gKjIH6j1gw_3pyGUZJo0/export?gid=719810628&format=csv",
                                    index_col=0)
            # check if there is the required phone number in the sheet and if yes, check payment status of that phone number
            if database.get_user_data_by_id(st.session_state.user_id).get("phone_number", 0) in sheet_url.index:
                if sheet_url.loc[database.get_user_data_by_id(st.session_state.user_id).get("phone_number", 0), "Payment Status"] == "paid":
                    st.session_state['waiting_for_payment'] = False
                    st.session_state['payment_successful'] = True
                    # Update the user's SOP credits
                    user_data = database.get_user_data_by_id(st.session_state.user_id)
                    user_data['SOP_CREDITS'] += 1
                    database.update_user(user_data['username'], user_data)
                    st.success("🎉 Congratulations! You have successfully purchased 1 SOP credit. You can now create 1 SOP draft. 🎉")
                    st.balloons()
                    st.info("🔥 You can also view your SOP draft by clicking on the 'Drafts' button on the sidebar. 🔥")
                    break


if st.session_state.get("user_logged_in"):
    display_payment_page()
else:
    st.error("⚠️ You need to log in to access this feature. Please log in. ⚠️")
