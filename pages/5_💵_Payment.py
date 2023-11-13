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
    st.markdown(f"<a href='{payment_link}' target='_blank'><button style='color: white; background-color: #4CAF50; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;' onclick='localStorage.setItem(\"payment_clicked\", \"true\")'>Proceed to Payment</button></a>", unsafe_allow_html=True)

    # Add a placeholder for the waiting message
    waiting_message = st.empty()

    # Check if the payment button was clicked (using browser local storage)
    st.markdown("""
        <script>
        const paymentClicked = localStorage.getItem("payment_clicked");
        if (paymentClicked) {
            window.parent.postMessage({type: "streamlit:setComponentValue", args: {data: true}}, "*");
        }
        </script>
    """, unsafe_allow_html=True)

    # Display the waiting message
    if st.session_state.get('waiting_for_payment'):
        waiting_message.info("Waiting for payment confirmation... Please do not close this page.")

# Initialize session state for payment waiting
if 'waiting_for_payment' not in st.session_state:
    st.session_state.waiting_for_payment = False

# Listen to messages from JavaScript
st.markdown("""
    <script>
    window.addEventListener("message", (event) => {
        if (event.data.type === "streamlit:setComponentValue") {
            Streamlit.setComponentValue(event.data.args.data);
        }
    });
    </script>
""", unsafe_allow_html=True)

# Check if the user is logged in
if st.session_state.get("user_logged_in"):
    display_payment_page()
else:
    st.error("⚠️ You need to log in to access this feature. Please log in. ⚠️")
