import openai
import streamlit as st
import time
import os
import tiktoken
import logging


os.environ['OPENAI_API_KEY'] = st.secrets['api_key']
openai.api_key = os.environ['OPENAI_API_KEY']
logging.basicConfig(level=logging.INFO)
fine_tuning_model = st.secrets['ft_model']


@st.cache_data
def load_tokens():
    encoding = tiktoken.get_encoding("cl100k_base")


load_tokens()


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(string))
    return num_tokens


@st.cache_data
def get_instructions():
    instructions_cached = """You are a professional writer for a student applying for a graduate program at a prestigious university. You need to craft a compelling Statement of Purpose (SOP) to showcase your qualifications and motivations. Your goal is to demonstrate your fit for the program and your potential as a future academic or professional in the field. Use the information provided by the user to write the Statement of Purpose. The statement of purpose should clearly cover all sections mentioned below: 1. Introduction: The introduction should describe how the user became interested in a particular field. Describe a series of events or narrate a life changing event or justify with a problem the student aims to solve. 2. Career Goals: The SOP should clearly describe the users career goal. The goal should be as specific as possible and should be relevant to the program the user wishes to pursue* 3. Education Background: Write about 2-3 relevant subjects the user studied in undergraduate education - and describe what skills / knowledge the user gained through those subjects and how the gained skills / knowledge is relevant to the program the user is applying to. 4. Projects, Research, Internships & Work Experience: Include paragraphs to describe relevant projects, research work, internships and work experience. The chosen experiences should be relevant to the program applied to and each experience described should explain how it created impact and how it brought the user closer to their career goal. 5. Skills / Knowledge Missing: Include a few knowledge pieces, skills the user is currently missing. These should be knowledge pieces / skills the student needs to achieve their career goal and which the student doesn't currently have. 6. Why this program & university: Write about why applying to the particular program and university is necessary for the user. Explain how the user will get the necessary knowledge, skills through the program & university. Write about specific courses, research work at the university and other activities at the university that would help the student. 7. How the user can contribute to the university: Write how the user can contribute to the university, their peers, classroom discussion and student community. You could also explain how the student's background would enrich their peers experience or help the university in particular research areas. 8. Conclusion: Summarize the main points and reiterate enthusiasm for the program and dedication to succeed. End with a positive note, expressing gratitude for the opportunity to apply. Remember to maintain a clear, concise, and genuine tone throughout the SOP. Focus on demonstrating your passion, qualifications, and alignment with the program and university. Feel free to elaborate on each section and use personal experiences to illustrate your points. The SOP should be free of grammatical and spelling errors and should be between 900 to 1100 words. Also, the SOP should flow properly. Each sentence should connect well with the next. And each paragraph should connect well with the next. Leave a line in between paragraphs. Do not repeat sentences and phrases too much."""
    return instructions_cached


instructions = get_instructions()


def generate_sop(
        word_limit,
        program,
        university,
        field_interest,
        career_goal,
        subjects_studied,
        projects_internships,
        lacking_skills,
        program_benefits,
        contribution,
        resume_text=None,
        model_name=fine_tuning_model,
):
    if resume_text is None:
        resume = ""
    else:
        resume = f"Also consider the following skills and work experiance while writing the SOP, if you think it fits. {resume_text}"

    completion = openai.ChatCompletion.create(
        model=model_name,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": instructions,
            },
            {
                "role": "user",
                "content": f"""Write an SOP with a word limit of minimum {word_limit} and maximum 1200
                Here is my information:
                Program: {program}
                University: {university}
                Introduction: {field_interest}
                Career Goals: {career_goal}      
                Education Background: {subjects_studied}   
                Projects, Internship, Research Work: {projects_internships}
                Skills Missing: {lacking_skills}       
                Why this program and University: {program_benefits}       
                How Can I Contribute: {contribution}      
                Also, add a conclusion of your own.
                {resume} 
                Rewrite all of this and write a good personal essay/SOP.
                Make sure the number of words is between {word_limit}-1200!
                """,
            },
        ],
    )
    logging.info(f"Model Used: {model_name}")
    input_string = f"""{instructions} 
                \n  Write an SOP with a word limit of minimum {word_limit} and maximum 1100
                Here is my information:
                Program: {program}
                University: {university}
                Introduction: {field_interest}
                Career Goals: {career_goal}      
                Education Background: {subjects_studied}   
                Projects, Internship, Research Work: {projects_internships}
                Skills Missing: {lacking_skills}       
                Why this program and University: {program_benefits}       
                How Can I Contribute: {contribution}      
                Also, add a conclusion of your own.
                {resume} 
                Rewrite all of this and write a good personal essay/SOP.
                Make sure the number of words is between {word_limit}-1200!
"""
    user_given_string = f"""Program: {program}
                University: {university}
                Introduction: {field_interest}
                Career Goals: {career_goal}      
                Education Background: {subjects_studied}
                Projects, Internship, Research Work: {projects_internships}
                Skills Missing: {lacking_skills}       
                Why this program and University: {program_benefits}       
                How Can I Contribute: {contribution}      
                Also, add a conclusion of your own."""

    logging.info(f"Number of total input tokens used: {num_tokens_from_string(input_string, 'cl100k_base')}")
    logging.info(
        f"Number of total output tokens used: {num_tokens_from_string(completion.choices[0]['message']['content'], 'cl100k_base')}")
    logging.info(f"Resume tokens used: {num_tokens_from_string(resume, 'cl100k_base')}")
    logging.info(f"Instructions tokens used: {num_tokens_from_string(instructions, 'cl100k_base')}")
    logging.info(
        f"User input tokens used (Excluding resume): {num_tokens_from_string(user_given_string, 'cl100k_base')}")
    sop_content = completion.choices[0]["message"]["content"]
    logging.info(completion)
    return sop_content


def resume_summarize_with_gpt(resume_text):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        temperature=0.3,
        max_tokens=300,
        messages=[
            {
                "role": "system",
                "content": f"""You are an excellant writer. You read resumes and provide a 150 word summary of their skills and experiances, based on the text from the resume
                """,
            },
            {
                "role": "user",
                "content": f"""Summarize this resume in 150 words {resume_text}
                """,
            },
        ],
    )
    logging.info(f"Model Used: gpt-3.5-turbo-16k")
    logging.info(f"Number of total input tokens used: {num_tokens_from_string(resume_text, 'cl100k_base')}")
    logging.info(
        f"Number of total output tokens used: {num_tokens_from_string(completion.choices[0]['message']['content'], 'cl100k_base')}")
    resume = completion.choices[0]["message"]["content"]
    return resume
