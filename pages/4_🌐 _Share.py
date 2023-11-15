import streamlit as st
import pyperclip
from urllib.parse import urlparse, urlencode
from PIL import Image
im = Image.open('icon.png')
db_url = urlparse("https://sop-builder.streamlit.app/").netloc

st.title("Share Your SOP")


def redirect_button(url: str, text: str = None, color="#C5221F"):
    if text == "Share On Facebook":
        color = "#3b5998"
    elif text == "Share On Twitter":
        color = "#1da1f2"
    elif text == "Share On LinkedIn":
        color = "#0077b5"
    elif text == "Share On WhatsApp":
        color = "#25D366"
    elif text == "Share On Reddit":
        color = "#FF4500"
    elif text == "Share On PinInterest":
        color = "#BD081C"
    elif text == "Share Via GMail":
        color = "#C5221F"
    st.markdown(
        f"""
    <a href="{url}" target="_blank">
        <div style="
            width: 100%;
            display: inline-block;
            padding: 0.5em 1em;
            color: #FFFFFF;
            background-color: {color};
            border-radius: 3px;
            text-decoration: none;">
            {text}
        </div>
    </a>
    <br><br>
    """,
        unsafe_allow_html=True
    )


col1, col2 = st.columns([2, 1])

with col1:
    st.write("Share your SOP on social media platforms.")
    subcol1, subcol2 = st.columns(2)
    with subcol1:
        redirect_button(f"https://www.facebook.com/sharer/sharer.php?u={db_url}", "Share On Facebook")
        redirect_button(f"https://twitter.com/intent/tweet?url={db_url}", "Share On Twitter")
        redirect_button(f"https://www.linkedin.com/shareArticle?url={db_url}", "Share On LinkedIn")
    with subcol2:
        redirect_button(f"https://wa.me/?text={db_url}", "Share On WhatsApp")
        redirect_button(f"https://www.reddit.com/submit?url={db_url}", "Share On Reddit")
        redirect_button(f"https://mail.google.com/mail/u/0/?fs=1&tf=cm&su=Check%20Out%20SOP%20Buider&body=https%3A%2F%2Fsop-builder.streamlit.app%2F#inbox", "Share Via GMail")
        # redirect_button("Not SURE", "Share Via Gmail")

# with col2:
#     st.write("Or you can Copy the Link")
#     st.button("Copy Link", on_click=pyperclip.copy("https://sop-builder.streamlit.app/"))
