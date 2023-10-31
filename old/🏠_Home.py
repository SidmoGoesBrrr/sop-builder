import streamlit as st

from PIL import Image
#####################################################################################################################################################
im = Image.open('icon.png')
st.session_state.user_id=""
st.session_state.generated_sop=""
st.markdown(
        """
        <style>
            .main {
                background-color: #212529;
                padding: 2rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Create the landing page content
st.markdown(
    "<h1 style='text-align: center; color: #c2c5aa;'>Welcome to the Statement of Purpose Generator</h1>",
    unsafe_allow_html=True,
)

st.image("art.png")

# Add a brief introduction
st.subheader(
    "Crafting an impressive Statement of Purpose (SOP) for your university application has never been easier."
)
st.subheader("What is SOP (Statement of Purpose) ?")
information = st.empty()
information.write(
    "A Statement of Purpose (SOP) holds significant importance in the immigration process. It is a crucial document that showcases an individual's intentions and aspirations when applying for a visa or seeking immigration to another country. The SOP acts as a personal statement, allowing the applicant to express their goals, qualifications, and reasons for wanting to relocate. By crafting a compelling and well-structured SOP, individuals can effectively communicate their genuine interest in contributing to the host country's society and economy. This document plays a pivotal role in influencing immigration officers' decisions and can greatly impact the success of an immigration application. Therefore, it is vital to carefully articulate one's ambitions, experiences, and motivations in an SOP to enhance their chances of a favorable outcome in the immigration process."
)