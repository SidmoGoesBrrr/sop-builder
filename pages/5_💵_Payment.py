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
    st.markdown(f"<a href='{payment_link}' target='_blank'><button style='color: white; background-color: #4CAF50; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;'>Proceed to Payment</button></a>", unsafe_allow_html=True)

    st.write("Please click the button above to proceed with the payment.")

# Check if the user is logged in
if st.session_state.get("user_logged_in"):
    display_payment_page()
else:
    st.error("⚠️ You need to log in to access this feature. Please log in. ⚠️")
