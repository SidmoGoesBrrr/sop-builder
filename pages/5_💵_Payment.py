import logging
import streamlit as st
from pymongo import MongoClient
import time
import database

# Function to display the payment page
def display_payment_page():
    # Razorpay payment link
    payment_link = "https://rzp.io/l/3FTyewKI8f"

    # Displaying the payment button
    if st.link_button('Proceed to Payment', payment_link):
        # Open the payment link
        st.markdown(f"<a href='{payment_link}' target='_blank'>Click here if you are not redirected</a>", unsafe_allow_html=True)
        # Set a flag indicating the payment process has started
        st.session_state['waiting_for_payment'] = True

    # Check if waiting for payment
    if st.session_state.get('waiting_for_payment', False):
        st.info("Waiting for payment confirmation... Please do not close this page.")

# Initialize session state for payment waiting
if 'waiting_for_payment' not in st.session_state:
    st.session_state.waiting_for_payment = False

# Check if the user is logged in
if st.session_state.get("user_logged_in"):
    display_payment_page()
else:
    st.error("⚠️ You need to log in to access this feature. Please log in. ⚠️")
