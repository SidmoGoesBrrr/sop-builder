import os
import streamlit as st
import time
from database import *
from streamlit.components.v1 import html
from PIL import Image

im = Image.open('icon.png')
st.header("Sign Out")
st.write("Click on the button Below to Sign out")
st.write("Thank you for using our SOP generator") 

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


if st.button('Sign Out'):
    st.session_state.user_logged_in = False
    st.session_state.login_button = True
    st.success("Logged out Successfully.")
    time.sleep(2)
    os.rename(r'pages/2_🔑_Sign_Out.py', r'lages/2_🔑_Sign_Out.py')
    os.rename(r'lages/1_🚀_Sign_Up.py', r'pages/1_🚀_Sign_Up.py')
    os.rename(r'lages/2_🔑_Sign_In.py', r'pages/2_🔑_Sign_In.py')
    st.session_state.disabled = True
    st.session_state['button'] = False
    for i in st.session_state:
        if i != 'user_logged_in' and i != 'login_button':
            del st.session_state[i]
    nav_page('sign_in')
