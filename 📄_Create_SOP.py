import streamlit as st
from PIL import Image

im = Image.open('icon.png')
st.set_page_config(page_title="SOP Generator", page_icon=im)

from open_ai_sop import generate_sop, resume_summarize_with_gpt
# Check if the user is logged in
import requests

from streamlit import session_state as state
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import time
import database
import PyPDF2
import re
import os
import io
import os
from datetime import datetime
import pytz

from streamlit_star_rating import st_star_rating

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            #GithubIcon {visibility: hidden;}
            </style>
            """
st.markdown(
    """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK {
        display: none;
    }
    button {
        height: 60px !important;
    }
    input {
        height: 30px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(hide_streamlit_style, unsafe_allow_html=True)
# Function to display user information with HTML and CSS

if "user_logged_in" not in st.session_state:
    st.session_state.user_logged_in = False
    try:
        os.rename(r'lages/2_🔑_Sign_In.py', r'pages/2_🔑_Sign_In.py')
        os.rename(r'pages/2_🔑_Sign_Out.py', r'lages/2_🔑_Sign_Out.py')
    except:
        pass

if "user_id" not in st.session_state:
    st.session_state.user_id = ""


def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text


# Function to save the entered text to the database
def save_to_database(key, value):
    database.update_user_by_id(st.session_state.user_id, {key: value})


def display_sop(text):
    # Retrieve the content from text_areas and limit it to the specified word limit
    word_count = len(text.split())
    text = text + f"\nWord Count: {word_count}"
    banner.text(text)


def rating():
    st.write("Rate this SOP before using other buttons")
    return st_star_rating(label="Rate this SOP", maxValue=5, defaultValue=0, key="rating")


# Function to display success banner
def show_success_banner():
    banner.success("Text saved successfully!")


def check_if_program_length_okay(text, min_limit=50, max_limit=500):
    word_count = len(text.split())
    return min_limit <= word_count <= max_limit


def error_msg(question):
    if current_section['question'] == "Which university is this SOP for?" or \
            current_section['question'] == "Which program is this SOP for?":
        banner.error("Please do not leave this field blank")
    else:
        banner.error("Please enter between 50 and 500 words.")


def count_words(text):
    if text:
        words = text.split()
        return len(words)
    else:
        return 0


@st.cache_data
def load_text():
    text_dict = {
        "first_page": {
            "heading": "Welcome to AdmitAbroad's SOP Generator",
            "link": "https://www.youtube.com/"
        },
        "program": {
            "heading": "Program Name",
            "question": "Which program is this SOP for?",
            "placeholder": "e.g., Master's in Computer Science",
            "link": "https://www.youtube.com/"
        },
        "university": {
            "heading": "University Name",
            "question": "Which university is this SOP for?",
            "placeholder": "e.g., Stanford University",
            "link": "https://www.youtube.com/"
        },
        "field_interest": {
            "heading": "Introduction and Origins",
            "question": "How did you become interested in this field? Describe an instance that made you interested in the field or a sequence of events that made you interested in the field.",
            "placeholder": "e.g., As a kid, I was considered a nerd. Always reading books, watching anime or studying. I didn’t have too many friends – and so when I was taught programming for the first time in the sixth grade, I found a new thing to focus my “nerd energy” on. It began with a curious intent to understand how I could “tell” a computer what to do and so I wrote my first program – an algorithm that instructed the computer to generate a sequence of numbers in the Fibonacci series. To you, the reader, this might sound mundane – but to me, it was an “aha” moment. I wanted to test the boundaries of what I will into existence and wrote 176 programs between the sixth and tenth grades. Two of my most noteworthy programs from this time were a pac-man style game and a GK quiz I built. With time, my interest in programming grew and so, pursing an engineering degree in Computer Science was a natural choice.",
            "link": "https://www.youtube.com/"
        },
        "career_goal": {
            "heading": "Career Goals",
            "question": "What is your career goal? And why did you choose this as your goal?",
            "placeholder": "e.g., A few years ago, a relative was involved in a road accident. He was crossing the street when suddenly a car that had jumped the signal crashed into him – killing him on the spot. This was a trying time for me and my family. I soon learnt that India has the dubious distinction of recording the greatest number of road accidents annually. The average number of road accidents in the last 5 years has been 4,72,000. The large majority of these occur due to human error – things like jumping signals, not adhering to speed limits, and driving under the influence of alcohol. Changing societal behaviour on all these fronts is difficult – and so, mass producing driverless cars seems like a promising solution to save human lives. Motivated by a personal loss, my goal thus is to work in the field of AI to make fully autonomous cars a reality.",
            "link": "https://www.youtube.com/"
        },
        "subjects_studied": {
            "heading": "Subjects Studied",
            "question": "What subjects have you studied so far that have made you competent in your area of interest? What relevant skills, knowledge pieces have you learnt from these subjects? When and where did you study these subjects?",
            "placeholder": "e.g., In college, I studied several subjects that formed the foundation of my knowledge of Computer Science. The course on Object Oriented Programming taught me best practices in programming while subjects like Data Structures taught me how data should be stored for efficient retrieval. Further, studying algorithms taught me how to break a problem down and then combine basic programming constructs in a cohesive manner to solve them. Studying theory was certainly important, but the only way for me to test my skills was to work on projects to put theory to practice.",
            "link": "https://www.youtube.com/"
        },
        "projects_internships": {
            "heading": "Achievements, Projects, Work & Research Done",
            "question": "What projects, internships, research work have you done so far to achieve your career goals and how have these helped you get closer to achieving your career goals? Quantify the outcomes / achievements from these projects if any. You can also upload your resume.",
            "placeholder": "e.g., I worked on several projects that allowed me to sharpen my skills in machine learning and computer vision. Two projects worth mentioning are my work on creating a tumor identification software and a robot that could identify structural faults in building. The former of these two was a research project commissioned by a local hospital. They had a large inflow of patients who would regularly do CT scans and MRIs – but didn’t have enough doctors to look at the scans in a timely manner. To solve this problem, I studied existing research done on building such models. I found two models that could be tweaked for this purpose. However, these were general object detection models and so I had to train them on five years’ worth of patient scans. I also had the to optimize the algorithm itself for this use case. Today, this software is used by the hospital – and in the last year it has detected the nature and stage of over 2,500 tumors with a 97% accuracy saving crucial time and cost for both the hospital and patients. Seeing the results, my head of department recommended me to the department of building safety in the Mumbai Municipal Corporation (MMC). At the time, the MMC faced a peculiar issue – there were several buildings in Mumbai that looked structurally healthy from the outside but were on the brink of collapse. Civil engineers were wary of entering such buildings for inspection owing to the risk. To solve this, I created a robot fitted with a camera on top. Using the camera, the bot would autonomously navigate the interior of the building clicking pictures and would calculate the risk of structural failure by spotting cracks, bulging walls and sagging floors. ",
            "link": "https://www.youtube.com/"
        },
        "lacking_skills": {
            "heading": "Skills & Knowledge Needed",
            "question": "What specific skills / knowledge do you currently lack which are needed for you to achieve your career goals? These should be skills / knowledge that you don’t currently have.",
            "placeholder": "While the projects described above, and several others allowed me to understand and implement the basics of computer vision and Artificial Intelligence, I still lack several skills to become a full fledged AI engineer to develop autonomous cars. For example, I don’t know how to build object recognition software when objects are moving. Further, I don’t have a deep enough understanding of how to modify neural networks to support the specific requirements of creating a self-driving car. Thus, I am applying to the master’s in computer science program at your university.",
            "link": "https://www.youtube.com/"
        },
        "program_benefits": {
            "heading": "How the Program Will Help You",
            "question": "What specific skills / knowledge will the master's program give you which will help you achieve your career goal? Elaborate based on courses, research work, networking events and other relevant activities at the university.",
            "placeholder": "e.g., At the Harvard I plan to bridge the gaps in my knowledge through courses like Pattern Recognition & Neural Networks and Intelligent Vehicle Systems. Further, I am keen to work with professor <<professor name>> as he is currently working with <<company name>> on a funded project to build autonomous cars. Apart from the coursework and research, your university also hosts several AI networking events. These sessions would allow me to interact with those working at the cutting edge of AI and understand which latest technologies could be applied to developing driverless cars. ",
            "link": "https://www.youtube.com/"
        },
        "contribution": {
            "heading": "How You Can Contribute",
            "question": "How will you contribute to the university based on your knowledge, experience? Cite specific things you can do to strengthen your peer’s learning, classroom discussion and how you can contribute to the student community at college.",
            "placeholder": "e.g., While I certainly stand to benefit by studying at your university, I also believe that I can contribute to research and to the community at large. As I have already worked on a few object detection related projects, I plan to apply to work part time at the Computer Vision lab and contribute to ongoing research there. Further, in college I had the privilege of teaching over 100 economically disadvantaged kids math and science. Several of these have gone on to get admission at top engineering colleges in India. I hope I can continue this gratifying work through the “Donate an Hour” club on your campus.",
            "link": "https://www.youtube.com/"
        },
        "end_screen": {
            "heading": "Your SOP is ready!",
            "question": "Thank you for using SOP Generate. We hope you found it useful. If you did, please share it with your friends and family. If you have any feedback, please write to us at <<email address>>. We would love to hear from you.",
            "link": ""
        }
    }
    return text_dict


text_areas = load_text()

# Initialize session state
if "section_index" not in state:
    state.section_index = 0

if 'word_count' not in st.session_state:
    st.session_state.word_count = 0

if "generated_sop" not in st.session_state:
    st.session_state.generated_sop = ""

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "word_limit" not in st.session_state:
    st.session_state.word_limit = 0

if "rating_given" not in st.session_state:
    st.session_state.rating_given = 0

# Streamlit app
st.markdown(
    f"<h1 style='text-align: center;'>{text_areas[list(text_areas.keys())[state.section_index]]['heading']}</h1>",
    unsafe_allow_html=True)
st.markdown(
    "<h6 style='text-align: center;'>Answer in a minimum of 50 words and a maximum of 200 words.</h6>",
    unsafe_allow_html=True)

# Display the current section
if st.session_state.section_index == 0:
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
        "<h1 style='text-align: center;'>Create Your SOP using AI in minutes</h1>",
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
    if st.session_state.user_logged_in:
        if st.button("Next➡️"):
            st.session_state.section_index += 1
            st.rerun()
            st.rerun()
    else:
        st.error("Please login to continue")
else:
    current_section_key = list(text_areas.keys())[state.section_index]
    current_section = text_areas[current_section_key]
    try:
        if st.session_state.section_index == len(text_areas) - 1:
            st.session_state.section_index = len(text_areas) - 1
        else:
            previous_text = database.get_user_data_by_id(st.session_state.user_id)[current_section_key]
            st.write(f"### {current_section['question']}")
            link = f'[Watch Best Practices To Write This Answer]({text_areas[list(text_areas.keys())[state.section_index]]["link"]})'
            st.markdown(link, unsafe_allow_html=True)
            text = st.text_area(" ", key=current_section_key, value=previous_text,
                                placeholder=current_section["placeholder"],
                                height=300)
            word_count = count_words(text)
            st.text(f"Word Count: {word_count}")
            st.session_state.word_count = word_count
    except Exception as e:
        print("Exception in displaying text area")
        print(e)
        pass

    # Navigation buttons
    sop_display_area = st.empty()
    st.divider()
    col1, col2, col3, col4, col5 = st.columns(5)
    banner = st.empty()
    if state.section_index == len(text_areas) - 1:
        sop_display_area.write(str(st.session_state.generated_sop))
        if st.session_state.rating_given == 0:
            st.session_state.rating_given = rating()
            user_data = database.get_user_data_by_id(st.session_state.user_id)
            ist = pytz.timezone('Asia/Kolkata')
            current_timestamp = datetime.now(ist).strftime("%A,%d %B %Y - %H:%M:%S")
            if 'drafts' in user_data and isinstance(user_data['drafts'], list):
                # If 'draft' is a list, fetch and append to it
                existing_draft = user_data['drafts']
                existing_draft.append(
                    {'content': st.session_state.generated_sop, 'timestamp': current_timestamp,
                     'rating': st.session_state.rating_given})
            else:
                # If 'draft' doesn't exist or is not a list, create a new list
                existing_draft = [
                    {'content': st.session_state.generated_sop, 'timestamp': current_timestamp,
                     'rating': st.session_state.rating_given}]
            # Update the user's draft in the database
            database.update_user_by_id(st.session_state.user_id, {'drafts': existing_draft})
            st.rerun()

    if state.section_index == len(text_areas) - 5:
        if st.session_state.summary == "":
            uploaded_file = st.file_uploader("Upload your resume here", type=["pdf"])
            if uploaded_file is not None:
                with st.status("Summarizing Resume With AI", expanded=True) as status:
                    st.write("Parsing the resume...")
                    # Save the uploaded file temporarily with a unique filename
                    temp_file_path = f"temp_resume_{str(st.session_state.user_id)}.pdf"
                    with open(temp_file_path, "wb") as temp_file:
                        temp_file.write(uploaded_file.getvalue())
                    # Extract tex   t from the uploaded PDF
                    resume_text = extract_text_from_pdf(temp_file_path)
                    st.write("Summarizing the resume...")

                    # Summarize the resume using GPT-3.5 Turbo
                    summary = resume_summarize_with_gpt(resume_text)
                    st.write("Resume Summary:")
                    st.write(summary)

                    # Display the summarized text

                    # Remove the temporary PDF file
                    os.remove(temp_file_path)
                    st.session_state.summary = summary
                    status.update(label="Resume Summarized!", state="complete", expanded=False)

    with col1:
        if state.section_index == 0:
            st.button("⬅️Previous", disabled=True)
        elif state.section_index == len(text_areas) - 1:
            if st.button("⬅️Previous", disabled=not st.session_state.rating_given):
                state.section_index = max(0, state.section_index - 1)
                st.rerun()
        else:
            if st.button("⬅️Previous"):
                state.section_index = max(0, state.section_index - 1)
                st.rerun()

    with col2:
        if state.section_index == len(text_areas) - 1:
            import docx

            doc_download = docx.Document()
            doc_download.add_paragraph(st.session_state.generated_sop)
            doc_download.save("sop.docx")
            bio = io.BytesIO()
            doc_download.save(bio)
            if st.download_button(
                    label="Download Word File⬇️",
                    data=bio.getvalue(),
                    file_name="sop.docx",
                    mime='docx',
                    disabled=not st.session_state.rating_given):
                st.rerun()

    with col3:
        if st.session_state.section_index == len(text_areas) - 2:
            st.session_state.word_limit = st.number_input("Word Limit:", value=800, step=10, max_value=1200,
                                                          min_value=500)
        elif st.session_state.section_index == len(text_areas) - 1:
            st.session_state.word_limit = st.number_input("Word Limit:", value=800, step=10, max_value=1200,
                                                          min_value=500, disabled=not st.session_state.rating_given)

    with col4:
        if state.section_index == len(text_areas) - 1:
            print(st.session_state.rating_given)
            print(not st.session_state.rating_given)
            regenerate = st.button("Try Again🔄", disabled=not st.session_state.rating_given)
            user_data = database.get_user_data_by_id(st.session_state.user_id)
            fetched_data = {
                "program": user_data.get("program", ""),
                "university": user_data.get("university", ""),
                "field_interest": user_data.get("field_interest", ""),
                "career_goal": user_data.get("career_goal", ""),
                "subjects_studied": user_data.get("subjects_studied", []),
                "projects_internships": user_data.get("projects_internships", []),
                "lacking_skills": user_data.get("lacking_skills", []),
                "program_benefits": user_data.get("program_benefits", []),
                "contribution": user_data.get("contribution", [])
            }
            if regenerate and database.get_user_data_by_id(st.session_state.user_id).get("SOP_CREDITS", 0) >= 9:
                if 500 <= st.session_state.word_limit <= 1100:
                    with st.status("Regenerating Sop...", expanded=True) as regen_status:
                        st.session_state.generated_sop = ""
                        generated_sop = generate_sop(
                            st.session_state.word_limit,
                            **fetched_data,
                            resume_text=st.session_state.summary)
                        st.session_state.generated_sop = generated_sop
                        regen_status.update(label="SOP Regenerated", state="complete", expanded=False)
                        database.update_user_data_by_id(st.session_state.user_id,
                                                        {"SOP_CREDITS": database.get_user_data_by_id(
                                                            st.session_state.user_id).get("SOP_CREDITS", 0) - 9})

                        st.session_state.rating_given = 0
                        st.rerun()
                        display_sop(generated_sop)
                else:
                    st.error("Invalid Word Limit. Your value must be greater than 700 and less than 1100")
            else:
                st.error("You don't have enough credits to generate SOP. Please buy more credits from the sidebar.")

    with col5:
        if state.section_index == len(text_areas) - 1:
            if st.button("Start Over⏪", disabled=not st.session_state.rating_given):
                state.section_index = 1
                st.session_state.generated_sop = ""
                st.session_state.summary = ""
                st.rerun()

        elif state.section_index == len(text_areas) - 2:
            if st.button("Generate SOP✅", disabled=st.session_state.section_index == len(text_areas) - 1) and \
                    database.get_user_data_by_id(st.session_state.user_id).get("SOP_CREDITS", 0) >= 99:
                if 500 <= st.session_state.word_limit <= 1100:
                    with st.status("Generating Sop...", expanded=True) as sop_status:
                        save_to_database(current_section_key, text)
                        user_data = database.get_user_data_by_id(st.session_state.user_id)
                        fetched_data = {
                            "program": user_data.get("program", ""),
                            "university": user_data.get("university", ""),
                            "field_interest": user_data.get("field_interest", ""),
                            "career_goal": user_data.get("career_goal", ""),
                            "subjects_studied": user_data.get("subjects_studied", []),
                            "projects_internships": user_data.get("projects_internships", []),
                            "lacking_skills": user_data.get("lacking_skills", []),
                            "program_benefits": user_data.get("program_benefits", []),
                            "contribution": user_data.get("contribution", [])
                        }
                        st.write("Sending request to openAI")
                        state.section_index = min(len(text_areas) - 1, state.section_index + 1)

                        # Call the generate_sop function with the required arguments
                        generated_sop = generate_sop(
                            word_limit=st.session_state.word_limit,
                            resume_text=st.session_state.summary,  # Adjust word limit accordingly
                            **fetched_data)
                        st.write("SOP Generated Successfully")
                        database.update_user_data_by_id(st.session_state.user_id,
                                                        {"SOP_CREDITS": database.get_user_data_by_id(st.session_state.user_id).get("SOP_CREDITS", 0) - 99})
                        st.session_state.generated_sop = generated_sop
                        time.sleep(0.2)
                        sop_status.update(label="SOP Generated", state="complete", expanded=False)
                        st.rerun()
                        display_sop(st.session_state.generated_sop)
                else:
                    st.error("Invalid Word Limit. Your value must be greater than 700 and less than 1100")
            else:
                st.error("You don't have enough credits to generate SOP. Please buy more credits from the sidebar.")

        else:
            if st.button("Next➡️"):
                length_pass = check_if_program_length_okay(text)
                if text.strip() != "" and (length_pass == True or (
                        current_section['question'] == "Which university is this SOP for?"
                        or current_section['question'] == "Which program is this SOP for?")):
                    state.section_index = min(len(text_areas) - 1, state.section_index + 1)
                    save_to_database(current_section_key, text)
                    show_success_banner()
                    time.sleep(0.2)
                    st.rerun()
                else:
                    error_msg(current_section['question'])


def display_user_info_html(user_id):
    user_name = database.get_user_data_by_id(user_id).get("username", "User")
    user_credits = database.get_user_data_by_id(user_id).get("SOP_CREDITS", 0)
    html = f"""
    <style>
    .user-info {{
        position: fixed;
        bottom: 10px;
        align-items: center;
        padding: 10px;
        border-radius: 5px;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
    }}
    </style>
    <div class="user-info">
    <p><strong>User:</strong> {user_name}</p>
    <p><strong>Credits:</strong> {user_credits}</p>
    </div>"""

    # Display the HTML
    st.markdown(html, unsafe_allow_html=True)


# Example usage
if st.session_state.user_logged_in:
    display_user_info_html(st.session_state.user_id)
