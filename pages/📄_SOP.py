import streamlit as st

from open_ai_sop import generate_sop,resume_summarize_with_gpt3
# Check if the user is logged in


if st.session_state.get("user_logged_in") == True:
    from streamlit import session_state as state
    # TODO pip install reportlab
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet
    from io import BytesIO
    import time
    import database
    import PyPDF2
    import re
    import os

    # Function to extract text from a PDF file

    def extract_text_from_pdf(pdf_path):
        text = ""
        with open(pdf_path, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extractText()
        return text

    # Function to save the entered text to the database
    def save_to_database(key, value):
        database.update_user_by_id(st.session_state.user_id, {key: value})


    def display_sop(text):
        # Retrieve the content from text_areas and limit it to the specified word limit
        word_count = len(text.split())
        text=text+f"\nWord Count:{word_count}"
        banner.text(text)


    # Function to display success banner
    def show_success_banner():
        banner.success("Text saved successfully!")


    def saved_online():
        banner.info("Your draft has been saved")


    def check_if_program_length_okay(text):
        word_count = len(text.split())
        return word_count >= 50


    def error_msg(question):
        if current_section['question'] == "Which university is this SOP for?" or current_section[
            'question'] == "Which program is this SOP for?":
            banner.error("Please do not leave this field blank")
        else:
            banner.error("Please enter 50 words or more")


    def generate_pdf(text):
        pdf_filename = "output.pdf"

        # Create a PDF document
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Split the text into paragraphs and create Paragraph objects with proper styling
        paragraphs = text.split('\n')
        for paragraph in paragraphs:
            if paragraph.strip():
                p = Paragraph(paragraph, styles['Normal'])
                story.append(p)

        doc.build(story)

        return pdf_filename

    # TODO DELETE THIS FUNCTION IF YOU DONT LIKE WORD COUNT
    def count_words(text):
        if text:
            words = text.split()
            return len(words)
        else:
            return 0

        
    text_areas = {
        "program": {
            "question": "Which program is this SOP for?",
            "placeholder": "e.g., Master's in Computer Science"
        },
        "university": {
            "question": "Which university is this SOP for?",
            "placeholder": "e.g., Stanford University"
        },
        "field_interest": {
            "question": "How did you become interested in this field? Describe an instance that made you interested in the field or a sequence of events that made you interested in the field.",
            "placeholder": "e.g., As a kid, I was considered a nerd. Always reading books, watching anime or studying. I didn’t have too many friends – and so when I was taught programming for the first time in the sixth grade, I found a new thing to focus my “nerd energy” on. It began with a curious intent to understand how I could “tell” a computer what to do and so I wrote my first program – an algorithm that instructed the computer to generate a sequence of numbers in the Fibonacci series. To you, the reader, this might sound mundane – but to me, it was an “aha” moment. I wanted to test the boundaries of what I will into existence and wrote 176 programs between the sixth and tenth grades. Two of my most noteworthy programs from this time were a pac-man style game and a GK quiz I built. With time, my interest in programming grew and so, pursing an engineering degree in Computer Science was a natural choice."
        },
        "career_goal": {
            "question": "What is your career goal? And why did you choose this as your goal?",
            "placeholder": "e.g., A few years ago, a relative was involved in a road accident. He was crossing the street when suddenly a car that had jumped the signal crashed into him – killing him on the spot. This was a trying time for me and my family. I soon learnt that India has the dubious distinction of recording the greatest number of road accidents annually. The average number of road accidents in the last 5 years has been 4,72,000. The large majority of these occur due to human error – things like jumping signals, not adhering to speed limits, and driving under the influence of alcohol. Changing societal behaviour on all these fronts is difficult – and so, mass producing driverless cars seems like a promising solution to save human lives. Motivated by a personal loss, my goal thus is to work in the field of AI to make fully autonomous cars a reality."
        },
        "subjects_studied": {
            "question": "What subjects have you studied so far that have made you competent in your area of interest? What relevant skills, knowledge pieces have you learnt from these subjects? When and where did you study these subjects?",
            "placeholder": "e.g., In college, I studied several subjects that formed the foundation of my knowledge of Computer Science. The course on Object Oriented Programming taught me best practices in programming while subjects like Data Structures taught me how data should be stored for efficient retrieval. Further, studying algorithms taught me how to break a problem down and then combine basic programming constructs in a cohesive manner to solve them. Studying theory was certainly important, but the only way for me to test my skills was to work on projects to put theory to practice."
        },
        "projects_internships": {
            "question": "What projects, internships, research work have you done so far to achieve your career goals and how have these helped you get closer to achieving your career goals? Quantify the outcomes / achievements from these projects if any. You can also upload your resume.",
            "placeholder": "e.g., I worked on several projects that allowed me to sharpen my skills in machine learning and computer vision. Two projects worth mentioning are my work on creating a tumor identification software and a robot that could identify structural faults in building. The former of these two was a research project commissioned by a local hospital. They had a large inflow of patients who would regularly do CT scans and MRIs – but didn’t have enough doctors to look at the scans in a timely manner. To solve this problem, I studied existing research done on building such models. I found two models that could be tweaked for this purpose. However, these were general object detection models and so I had to train them on five years’ worth of patient scans. I also had the to optimize the algorithm itself for this use case. Today, this software is used by the hospital – and in the last year it has detected the nature and stage of over 2,500 tumors with a 97% accuracy saving crucial time and cost for both the hospital and patients. Seeing the results, my head of department recommended me to the department of building safety in the Mumbai Municipal Corporation (MMC). At the time, the MMC faced a peculiar issue – there were several buildings in Mumbai that looked structurally healthy from the outside but were on the brink of collapse. Civil engineers were wary of entering such buildings for inspection owing to the risk. To solve this, I created a robot fitted with a camera on top. Using the camera, the bot would autonomously navigate the interior of the building clicking pictures and would calculate the risk of structural failure by spotting cracks, bulging walls and sagging floors. "
        },
        "lacking_skills": {
            "question": "What specific skills / knowledge do you currently lack which are needed for you to achieve your career goals? These should be skills / knowledge that you don’t currently have.",
            "placeholder": "While the projects described above, and several others allowed me to understand and implement the basics of computer vision and Artificial Intelligence, I still lack several skills to become a full fledged AI engineer to develop autonomous cars. For example, I don’t know how to build object recognition software when objects are moving. Further, I don’t have a deep enough understanding of how to modify neural networks to support the specific requirements of creating a self-driving car. Thus, I am applying to the master’s in computer science program at your university."
        },
        "program_benefits": {
            "question": "What specific skills / knowledge will the master's program give you which will help you achieve your career goal? Elaborate based on courses, research work, networking events and other relevant activities at the university.",
            "placeholder": "e.g., At the Harvard I plan to bridge the gaps in my knowledge through courses like Pattern Recognition & Neural Networks and Intelligent Vehicle Systems. Further, I am keen to work with professor <<professor name>> as he is currently working with <<company name>> on a funded project to build autonomous cars. Apart from the coursework and research, your university also hosts several AI networking events. These sessions would allow me to interact with those working at the cutting edge of AI and understand which latest technologies could be applied to developing driverless cars. "
        },
        "contribution": {
            "question": "How will you contribute to the university based on your knowledge, experience? Cite specific things you can do to strengthen your peer’s learning, classroom discussion and how you can contribute to the student community at college.",
            "placeholder": "e.g., While I certainly stand to benefit by studying at your university, I also believe that I can contribute to research and to the community at large. As I have already worked on a few object detection related projects, I plan to apply to work part time at the Computer Vision lab and contribute to ongoing research there. Further, in college I had the privilege of teaching over 100 economically disadvantaged kids math and science. Several of these have gone on to get admission at top engineering colleges in India. I hope I can continue this gratifying work through the “Donate an Hour” club on your campus."
        },
        "end_screen": {
            "question": "Thank you for using SOP Generate. We hope you found it useful. If you did, please share it with your friends and family. If you have any feedback, please write to us at <<email address>>. We would love to hear from you.",
        }
    }

    # Streamlit app
    st.markdown("<h1 style='text-align: center; color: #80ed99;'>Welcome to the Statement of Purpose Generator</h1>",
                unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #c8b6ff;'>Start writing</h1>", unsafe_allow_html=True)
    st.markdown(
        "<h6 style='text-align: center; color: #fcf6bd;'>Answer in a minimum of 50 words and a maximum of 200 words.</h6>",
        unsafe_allow_html=True)

    # Initialize session state
    if "section_index" not in state:
        state.section_index = 0

    if 'word_count' not in st.session_state:
        st.session_state.word_count = 0

    if "generated_sop" not in st.session_state:
        st.session_state.generated_sop = ""

    # Display the current section
    current_section_key = list(text_areas.keys())[state.section_index]
    current_section = text_areas[current_section_key]
    try:
        previous_text = database.get_user_data_by_id(st.session_state.user_id)[current_section_key]
        st.write(f"### {current_section['question']}")
        text = st.text_area(" ", key=current_section_key, value=previous_text,
                            placeholder=current_section["placeholder"],
                            height=300)
        word_count = count_words(text)
        st.text(f"Word Count: {word_count}")
        st.session_state.word_count = word_count
    except:
        previous_text = ""

    # Navigation buttons
    sop_display_area=st.empty()
    col1, col2, col3, col4, col5 = st.columns(5)
    banner = st.empty()
    if state.section_index == len(text_areas) - 1:
        sop_display_area.write(str(st.session_state.generated_sop))
    
    if state.section_index == len(text_areas) - 5:
        uploaded_file = st.file_uploader("Upload your resume here", type=["pdf"])
        summary=None
        if uploaded_file is not None:
            status_placeholder = st.empty()

            status_placeholder.info("Resume Uploaded!")
            time.sleep(0.5)
            status_placeholder.info("Extracting text from the resume...")

            # Save the uploaded file temporarily with a unique filename
            temp_file_path = f"temp_resume_{str(st.session_state.user_id)}.pdf"
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(uploaded_file.getvalue())

            # Extract text from the uploaded PDF
            resume_text = extract_text_from_pdf(temp_file_path)

            status_placeholder.info("Extracted text from the resume.")

            # Summarize the resume using GPT-3.5 Turbo
            status_placeholder.info("Summarizing the resume...")
            summary = resume_summarize_with_gpt3(resume_text)

            status_placeholder.info("Summary generated.")

            # Display the summarized text
            

            # Remove the temporary PDF file
            os.remove(temp_file_path)
        st.session_state.summary=summary

    with col1:
        if state.section_index == 0:
            st.button("Previous⬅️", disabled=True)
        elif state.section_index == len(text_areas) - 1:
            if st.download_button("Download the Draft ", st.session_state.generated_sop, "sop.txt", "text/plain"):
                st.experimental_rerun()
        else:
            if st.button("Previous⬅️"):
                state.section_index = max(0, state.section_index - 1)
                st.experimental_rerun()

    with col2:
        if state.section_index == len(text_areas) - 1:
            if st.button("Save Draft Online"):
                user_data = database.get_user_data_by_id(st.session_state.user_id)
                if 'drafts' in user_data and isinstance(user_data['drafts'], list):
                    # If 'draft' is a list, fetch and append to it
                    existing_draft = user_data['drafts']
                    existing_draft.append(st.session_state.generated_sop)
                else:
                    # If 'draft' doesn't exist or is not a list, create a new list
                    existing_draft = [st.session_state.generated_sop]

                # Update the user's draft in the database
                database.update_user_by_id(st.session_state.user_id, {'drafts': existing_draft})
                saved_online()
                time.sleep(3)
                st.experimental_rerun()

    with col3:
        if state.section_index == len(text_areas) - 1:
            pdf_filename = generate_pdf(st.session_state.generated_sop)
            if st.download_button("Save Draft As PDF", open(pdf_filename, 'rb'), "sop.pdf"):
                st.experimental_rerun()
                

    with col4:
        if state.section_index == len(text_areas) - 1:
            regenerate = st.button("Change Word Limit and Regenerate")
            user_data = database.get_user_data_by_id(st.session_state.user_id)
            word_limit = st.number_input("Word Limit:", min_value=700, max_value=1100, value=800, step=10)
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

            # Call the generate_sop function with the required arguments
            generated_sop = generate_sop(
                engine='gpt-4',
                word_limit=word_limit,  # Adjust word limit accordingly
                **fetched_data  # Unpack the fetched_data dictionary to pass as arguments
            )
            if regenerate:
                generate_sop(word_limit)
                st.session_state.generated_sop=generated_sop
                display_sop(generated_sop)
                st.experimental_rerun()
        # NEW STUFF
        elif state.section_index == len(text_areas) - 2:
            option = st.selectbox("Which model of chat GPT would you like to use?", ["GPT-3.5", "GPT-4"])

    with col5:
        if state.section_index == len(text_areas) - 1:
            if st.button("Start Over"):
                state.section_index = 0
                st.experimental_rerun()

        elif state.section_index == len(text_areas) - 2:

            if st.button("Generate SOP✅"):
                save_to_database(current_section_key, text)
                with st.spinner("Generating SOP"):
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
                    state.section_index = min(len(text_areas) - 1, state.section_index + 1)

                    # Call the generate_sop function with the required arguments
                    generated_sop = generate_sop(
                        engine=option.lower(),
                        word_limit=800,
                        resume_text=st.session_state.summary,   # Adjust word limit accordingly
                        **fetched_data
                            # Unpack the fetched_data dictionary to pass as arguments
                    )
                    st.session_state.generated_sop=generated_sop
                    display_sop(generated_sop)
                    print(generated_sop)
                    st.experimental_rerun()

        else:
            if st.button("Next➡️"):
                length_pass = check_if_program_length_okay(text)
                if text.strip() != "" and (length_pass == True or (
                        current_section['question'] == "Which university is this SOP for?"
                        or current_section['question'] == "Which program is this SOP for?")):
                    state.section_index = min(len(text_areas) - 1, state.section_index + 1)
                    save_to_database(current_section_key, text)
                    show_success_banner()
                    time.sleep(1)
                    st.experimental_rerun()
                else:
                    error_msg(current_section['question'])

else:
    st.error("⚠️ You need to login to access this feature! Please log in. ⚠️")
