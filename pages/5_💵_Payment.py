import logging
import streamlit as st
from pymongo import MongoClient
import time
import database
import streamlit as st
from streamlit.components.v1 import html
# Function to display the payment page
def display_payment_page():
    # Razorpay payment link
    payment_link = "https://rzp.io/l/3FTyewKI8f"
    
    # Payment text
    payment_text = "💰 Purchase one SOP for 99 rupees per SOP 💰"
    
    # Display payment text in bold with emoji
    st.markdown(f"<p style='font-size: 24px; font-weight: bold;'>{payment_text}</p>", unsafe_allow_html=True)

    # Function to open the payment link


    def open_page(url):
        open_script= """
            <script type="text/javascript">
                window.open('%s', '_blank').focus();
            </script>
        """ % (url)
        html(open_script)

    # Create a Streamlit button to open the payment link
    if st.button("Pay now",on_click=open_page(payment_link)):
        st.write("If you are not redirected, please click here.")
        st.session_state["payment_status"] = "waiting"
        st.write("Waiting for payment...")
        while st.session_state["payment_status"] == "waiting":
            time.sleep(1)
# Check if the user is logged in
if st.session_state.get("user_logged_in"):
    display_payment_page()
else:
    st.error("⚠️ You need to log in to access this feature. Please log in. ⚠️")
