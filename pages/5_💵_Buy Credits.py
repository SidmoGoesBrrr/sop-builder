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
    st.title("Payment Page")
    st.write("You can buy extra credits here")
    st.write("Everytime you change inputs, you will need 99 credits to generate a new SOP")
    st.write("To regenerate with the same input you will need 0 credits")
    st.write("You can buy 99 credits for INR 99.00")
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
        start_time = time.time()
        last_log_time = start_time
        # Redirect to the payment page
        while st.session_state['waiting_for_payment']:
            current_time = time.time()
            elapsed_time = current_time - start_time
            log_elapsed_time = current_time - last_log_time

            # Log every 1 minute
            if log_elapsed_time > 60:
                logging.info("1 minute elapsed, no payment received yet.")
                last_log_time = current_time  # Update last log time

            # Expire payment after 10 minutes (600 seconds)
            if elapsed_time > 600:
                st.session_state['waiting_for_payment'] = False
                st.error("⚠️ Payment process expired. Please try again. ⚠️")
                break
            try:
                sheet_url = pd.read_csv("https://docs.google.com/spreadsheets/d/1rs4dVdlLXi8c3kN0pRRegu-gKjIH6j1gw_3pyGUZJo0/export?gid=719810628&format=csv")
                #logging.info(sheet_url)
                sop_db_ph_no="91"+database.get_user_data_by_id(st.session_state.user_id).get("phone_number", 0)
                logging.info(sop_db_ph_no)
                #check every cell in column "Payment Contact". Check its length first and if that is 10 then add 91 to it and then compare with sop_db_ph_no
                # Process 'Payment Contact' column - Add '91' to numbers of length 10
                sheet_url['Processed Payment Contact'] = sheet_url['Payment Contact'].apply(lambda x: "91" + str(x) if len(str(x)) == 10 else str(x))

                # Filter the DataFrame based on processed phone numbers
                filtered_df = sheet_url[sheet_url['Processed Payment Contact'] == sop_db_ph_no]
                logging.info(filtered_df)
                if not filtered_df.empty:
                    # Find the row with the highest 'Created At' timestamp
                    highest_timestamp_row = filtered_df.loc[filtered_df['Created At'].idxmax()]
                    # Get the current time in UTC
                    current_datetime_utc = datetime.now(pytz.UTC)
                    razorpay_created_at=highest_timestamp_row.get('Created At', 0)
                    created_at_datetime = datetime.fromtimestamp(razorpay_created_at, tz=pytz.UTC)
                    # Calculate the time difference in seconds
                    time_difference = (current_datetime_utc - created_at_datetime).total_seconds()
                    logging.info(time_difference)
                    
                    # check if there is the required phone number in the sheet and if yes, check payment status of that phone number
                    if sop_db_ph_no in sheet_url['Processed Payment Contact'].values and time_difference < 180: #3 minutes
                        payment_status = highest_timestamp_row['Payment Status']
                        # Strip whitespace and newline characters from the payment status
                        payment_status = payment_status.strip()
                        logging.info(payment_status)
                        if payment_status == "captured\npaid":
                            st.session_state['waiting_for_payment'] = False
                            st.session_state['payment_successful'] = True
                            # Update the user's SOP credits
                            user_data = database.get_user_data_by_id(st.session_state.user_id)
                            no_of_sop=highest_timestamp_row['Payment Order Items Quantity:']
                            logging.info(no_of_sop)
                            logging.info(99*no_of_sop)
                            user_data['SOP_CREDITS'] += 99*no_of_sop
                            database.update_user(user_data['username'], user_data)
                            if no_of_sop==1:
                                st.success(f"🎉 Congratulations! You have successfully purchased {int(99*no_of_sop)} SOP credits. You can now create {str(no_of_sop)} SOP draft. 🎉")
                            elif no_of_sop>1:
                                st.success(f"🎉 Congratulations! You have successfully purchased {int(99*no_of_sop)} SOP credits. You can now create {str(no_of_sop)} SOP drafts. 🎉")
                            st.balloons()
                            st.info("🔥 You can also view your SOP draft by clicking on the 'Drafts' button on the sidebar. 🔥")
                            break

                        elif payment_status == "failed":
                            st.session_state['waiting_for_payment'] = False
                            st.error("⚠️ Payment failed. Please try again. ⚠️")
                            break
                else:
                    logging.warning("No matching records found for the phone number.")

            except Exception as e:
                logging.error(f"An error occurred: {e}")
if st.session_state.get("user_logged_in"):
    display_payment_page()
else:
    st.error("⚠️ You need to log in to access this feature. Please log in. ⚠️")
