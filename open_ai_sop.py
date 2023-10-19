import openai
import streamlit as st
import time
api_key=st.secrets["api_key"]

openai.api_key = api_key

@st.cache_data
def get_instructions():
    instructions_cached = """Imagine you are a student applying for a graduate program at a prestigious university. You need to craft a compelling Statement of Purpose (SOP) to showcase your qualifications and motivations. Your goal is to demonstrate your fit for the program and your potential as a future academic or professional in the field.

Use the information provided by the user to write the Statement of Purpose. 

The statement of purpose should clearly cover all sections mentioned below:

1. Introduction
The introduction should describe how the user became interested in a particular field. Describe a series of events or narrate a life changing event or justify with a problem the student aims to solve.

2. Career Goals
The SOP should clearly describe the users career goal. The goal should be as specific as possible and should be relevant to the program the user wishes to pursue*

3. Education Background
Write about 2-3 relevant subjects the user studied in undergraduate education - and describe what skills / knowledge the user gained through those subjects and how the gained skills / knowledge is relevant to the program the user is applying to.

4. Projects, Research, Internships & Work Experience
Include paragraphs to describe relevant projects, research work, internships and work experience. The chosen experiences should be relevant to the program applied to and each experience described should explain how it created impact and how it brought the user closer to their career goal.

5. Skills / Knowledge Missing
Include a few knowledge pieces, skills the user is currently missing. These should be knowledge pieces / skills the student needs to achieve their career goal and which the student doesn't currently have.

6. Why this program & university
Write about why applying to the particular program and university is necessary for the user. Explain how the user will get the necessary knowledge, skills through the program & university. Write about specific courses, research work at the university and other activities at the university that would help the student. 

7. How the user can contribute to the university
Write how the user can contribute to the university, their peers, classroom discussion and student community. You could also explain how the student's background would enrich their peers experience or help the university in particular research areas. 

8. Conclusion
Summarize the main points and reiterate enthusiasm for the program and dedication to succeed. End with a positive note, expressing gratitude for the opportunity to apply.

Remember to maintain a clear, concise, and genuine tone throughout the SOP. Focus on demonstrating your passion, qualifications, and alignment with the program and university. Feel free to elaborate on each section and use personal experiences to illustrate your points.

The SOP should be free of grammatical and spelling errors and should be between 900 to 1100 words. Also, the SOP should flow properly. Each sentence should connect well with the next. And each paragraph should connect well with the next.
"""
    return instructions_cached

@st.cache_data
def get_sample_sops():
    sample_sops = """Sample SOP 1: MS in Data Science

    University of Pennsylvania

Traditionally, winning in sports has been a function of effective team ownership and hiring the best
coaches. Decisions on which players to select, trade and how to play were based on experience and
perceptions about players. That was till the Oakland Athletics (the A’s) Baseball team placed first in
the 2002 season of the American League West. Their General Manager – Billy Beane – had drafted
an odd set of players. His team did not visually “look” like champions and yet, the result was magical.
However, I assure you that no magic was involved. It was a clever use of Data Science (DATS). By
selecting only those players with a high on base percentage, Beane had improved the odds of his
team scoring more runs and therefore winning. Since school, I have been interested in watching and
playing sports – and when I read the A’s story, I realized the power of Data Science to gain
competitive advantage. I decided that my career goal would be to marry my love for sports with my
love for data and so, I would love to build a career in Sports Analytics.
DATS is an interdisciplinary field. Realizing this, I consciously decided to work on projects that would
foster my skills in this versatile domain. My first major project using it was for the Municipal
Corporation of Greater Mumbai (MCGM). They approached our college in the hope that we could
build a solution that would automate the discovery of abandoned vehicles in Mumbai. Such vehicles
are peppered throughout the city and make finding parking spots difficult. My solution was to build
an application that citizens could use. People could click pictures of vehicles, our algorithm would
then ascertain if the vehicle really was abandoned and if so, the MCGM would get it towed. I used
data annotation on the vehicle images to label features like dents, broken glass and punctured tires.
Feature extraction was carried out using a Mask R-CNN MobileNet model and classification of the
vehicle was accomplished using SVM. The vehicle was detected abandoned from those that were not
with an accuracy of 82% when tested at ground level by the MCGM officials. This solution will save a
lot of manpower for the MCGM and will reduce the city’s carbon footprint too by reducing traffic
caused due to abandoned vehicles. This step towards sustainability matches the vision and ReThink
Your Footprint awareness initiatives undertaken by the Upenn Sustainability committee.
Beyond the classroom, I volunteered with the Fire and Security Association of India’s student
committee. As the head of my college’s chapter, I conducted surveys and organized seminars on fire
safety across Mumbai. While working on one such event, I found that the leading cause of deaths in
fire accidents was due to delayed arrival of Emergency Vehicles (EVs). I surmised that one could
leverage concepts from DATS and Artificial Intelligence (AI) to solve this problem. Thus, I began work
on developing a Smart Traffic Management System for EVs. The system gives priority to EVs by
turning all traffic signals in their path ‘green’. Signals are switched to green if the EV is in the vicinity
of the signal and are turned back to their original state after the EV has passed. Data augmentation
techniques were employed to expand the data available for training of EVs. An activation mechanism
based neural network was introduced which improved model precision from 83% to 87% and
reduced computational complexity.
As I went about honing my technical skills, I was curious to know if I was capable of working on
cutting edge problems. To test myself, l applied for a research assistantship with Carnegie Mellon
University’s (CMU) Xu Labs. I was one of the few students selected globally and was charged with
classifying 3-D sub-cellular structures based on their shape using state of the art neural networks.
The project will provide a better understanding of subcellular structures which is essential in
determining the origin and spread of a disease along with ways of eliminating them.

While I enjoyed my work with Xu Labs, I missed being physically present at CMU due to travel
restrictions placed on account of the COVID pandemic. However, even when travel restrictions were
later relaxed, people refrained from traveling. After all, there was no mechanism to ensure that
people wore masks and maintained social distancing norms. Solving this problem could restore the
confidence of people and help restart the economy. To this end, I built a system that could detect if
people in a location were wearing masks and maintaining social distancing norms. The mask
detection model was built using OpenCV and residual networks. For any location, CCTV footage was
taken and Data Visualization libraries such as Seaborn and Matplotlib were used to generate heat
maps displaying human density. A histogram represented the count of people following and violating
norms with an accuracy of 86%. Additionally, the software I created was also capable of forecasting
the number of cases. The predictive model was made using LSTM networks and maps a sequence of
past observations to make future predictions. This model had a Root Mean Square (RMS) Error of 50
– far less than the 700 RMS error of other regression models prevalent at the time. I would greatly
appreciate the opportunity to learn from Prof. Sharath Chandra Guntuku whose project at the Penn
COVID Hub initiative aims to track and provide visual insights into common topics of discussion
pertaining to COVID-19 resonate with me.
Understanding the need for disseminating knowledge during the pandemic motivated me to virtually
join Unschool- an educational ecosystem as a DATS junior coach. During my time, I mentored
students by addressing course-related doubts via live sessions and provided practical exposure by
solving problems available on Kaggle through Jupyter Notebooks. I was delighted to discover that
Penn Data Science Group undertakes similar activities towards bridging the gap between industry
and academia. Besides, I have actively partaken in beach cleanup drives every weekend for 1.5 years
under the UN Champion of Earth, Mr. Afroz shah. The happy result being the return of back Olive
Ridley Sea Turtle after 20 years at the seashores of Mumbai which further inspires me to be a part of
the Upenn Sustainability committee.
Though I have majored in Electronics Engineering, I have taken every opportunity to move towards
my dream of building a career in Sports Analytics. I know that to truly realize my dream, I will need
to pursue a rigorous program to enhance my knowledge of this discipline. Therefore, I am applying
to Penn’s MSE in DATS. At Penn, I believe that I will be able to continue my research on several
projects I have already worked on. For instance, my project on the automatic detection of
Emergency vehicles is complementary to the research done at Penn IUR and I would extend my
experience to contribute to solving other problems of urbanization. I also would like the opportunity
to learn Big Data Analytics and Modern Data Mining Under Professors Zachary Ives and Linda Zhao
which will be a stepping stone towards my journey of becoming a Lead Data Scientist. Finally, I will
also apply to the Wharton Sports Analytics Initiative to build on my understanding of sports
analytics.
I am confident that with my experience and coursework, I will be able to thrive in Penn’s MSE in
DATS program. I therefore, submit my application for your kind consideration.

Sample SOP 2 : Master in Information Systems

Information systems is an emerging field that has received serious attention in the last few years. A few years
back, it started with manual systems that included Customer Databases. Catalogues have now turned into
advanced modern concepts like Data Mining. The massive development in this field has fascinated me and
motivated me to pursue a career in Information Systems. With extensive knowledge and ideas about C++, C,
Python, HTML, CSS, and JavaScript, I feel that I am ready to take the next step in my career in the field of
MIS. To keep up with the industry standards and equip myself with better skills, I have decided to pursue a
Master of Science degree in Information Systems from Northeastern University, Boston.

In my high school days, I was keen to learn more about computers, mathematics and other topics related to
science. I hope to learn more about my subjects of interest. I applied for an undergraduate degree program at
Mukesh Patel School of Technology Management and Engineering (NMIMS University), Mumbai. The
Bachelors in Information Technology course allowed me to get a fair idea of how vast and versatile the world
of Information Systems is. In this program, I came across several techniques like Cloud Computing, Web and
Mobile App Development, Computer Networks, Data Structures and Algorithms, Database Management, and
Database Administration. I did thorough research and studied these subjects with true dedication. They helped
me polish my skills and knowledge in understanding how different concepts work and how Information
Systems can significantly impact our lives. During this time, I got the opportunity to do several internships at
well-known companies, which greatly added to my learnings and developed more interest in the field.

With a keen interest in knowing more about Information Systems and their different aspects, I have completed
a few professional courses to understand the subject better. These courses include "Google Analytics For
Beginners" offered by Google and "Introduction to Data Science".These courses delivered a wholesome
amount of knowledge and in-depth ideas about various Information System platforms and techniques. I
successfully did the lessons from Coursera.com, and I have all the official certifications for the same. I also
completed the "Bitcoins and Cryptocurrencies'' course from edX.com, authorized by UC Berkeley, because I
found out that cryptocurrencies can have a bright future and MIS might play an essential role in it. Learning a
skill is different, and learning how to apply it in a real-world scenario is entirely different. I believe these
courses have allowed me to prepare myself for the latter. In the last three years of my college, I attended
numerous webinars and workshops like the Industrial automation, and robotics training - ISA Maharashtra,
Workshop on Cloud Computing - MPSTME, Capgemini - Tech Challenge (Data Analytics), and Global
Assessment of Information Technology (GAIT) - Bronze Certified conducted by Japan Third Party.


After a few months of learning and extensive research in Information Systems, I realized it was time to explore
new challenges and gather more professional experience. I worked as a Web developer intern at Being Digital
for six weeks. I was given the responsibility to create a medical website using Ruby On Rails. My website
turned out to be the best of the lot, and it did impress the management very much. Widhya Foundation took
me as a software engineering intern in February 2021. My experience here helped me learn and get hands-on
knowledge about the various software applications used in Information Systems. From December 2020 to
January 2021, I was a Web Development and Designing Intern at The Sparks Foundation. My involvement
with these companies and their management helped me to attain a good amount of professional experience. I
polished my communication, leadership, problem-solving, and teamwork skills with experts from different
industries. Not only that, but I also learned all about workplace culture, employee relations, and leadership
structure.I have worked on mobile applications and websites like Book Karo and Videshi Studies.

Now that I have talked about my academics and professional experience, I would like to mention that I want
to pursue my master's degree from the United States of America. The US degrees have an outstanding
reputation around the world, and companies across the globe recognize them. Universities in the USA have
maintained a very high standard of education which allows their students to be very successful in their
respective fields. With their always-changing and evolving classrooms, I will be getting a massive opportunity
to upgrade my skills and learn more about Information Systems, unlike anywhere else. Northeastern University
offers a Cooperative Education (co-op) as part of the program, which I am looking forward to because I will
be able to network with like-minded people around the campus and graduate with a stellar resume and
meaningful connections. The Information Systems curriculum is very flexible due to its wide variety of
rigorous courses. I can pursue any concentration I might find of particular interest. Northeastern University is
undoubtedly one of the best institutions offering a full-time Masters' degree in Information Systems. For
decades they have helped students realize their goals and imbued them with the winning mentality. Their
faculty is composed of the best professors and scholars from different countries.

Since my personal and professional interests come together, my goal is to do a Master's degree and then work
in Information Systems. I want to see myself as a successful Information Systems Manager, Computer Network
Architect, or Database Analyst in the coming years. I intend to return to India to support my family, who have
contributed to my career immensely over the years. I will be highly obliged to go through my application and
take admission to Northeastern University, Boston, USA.

Sample SOP 3: MS in Mechanical Engineering
When compared to other species, humans do not have any physical trait that stands out. We
are not the tallest, the fastest or even the strongest of any species. Yet, humans are
considered the pinnacle of life on earth. On reflection, one realizes that man’s ability to
extend his capability through tools and machines surely must have played a significant role in
making us the “dominant” species on earth. We find the manifestation of machines in each
walk of life – from simple levers that help reduce our effort to complex robots that can build
hundreds of cars a day. The contribution of machines in making modern life possible is why I
am fascinated by Mechanical Engineering.
Perhaps my inclination towards engineering began in high school, when I first understood
how Mathematics helped humans understand physical phenomena around them. To test my
knowledge of Math and Science, I participated in the International Math Olympiad, the
National Science Olympiad and the Australian Chemistry Olympiad. With each competition,
my interest in Math and Science grew. Consequently, I enrolled for an undergraduate degree
in Mechanical Engineering. Over the years, I realized that we have barely scratched the
surface of what can be invented for the betterment of humanity and nature alike. However, I
also knew that to contribute towards the advancement of engineering, I would first have to
become an excellent engineer.
To excel as an engineer, I worked hard on the undergraduate courses in college. I left no stone
unturned to understand every topic thoroughly. Even when the deadly COVID-19 pandemic
forced my college to stop on-campus lectures, I quickly adapted to online classes. There were
many challenges that teachers and students initially faced. But it dawned upon me that this
situation presented an opportunity. I was no longer confined to strict classroom timings or by
the curriculum taught at college. In fact, I had long known that to truly excel in my field of
study, I would need to go beyond the limited scope of the curriculum and educate myself
using any relevant source that I could find. This situation allowed me to do exactly that.
Resultantly, I studied from textbooks, online courses and through videos. Each new concept I
mastered on my own gave me a sense of gratification. Learning became the goal rather than
a means to secure high grades. In a sense, it seemed ironic that when my goal shifted from
grades to knowledge, my grades automatically improved. As a result, I currently hold the first
position in class and have a cumulative Grade Point Average of 9.75/10. But engineering is as
much about designing and building as it is about learning. And so, only securing high grades
was not enough for me to become a proficient Mechanical Engineer. The need of the hour
was to become conversant with tools that would help me bring ideas and concepts to life. So,
I started learning software like ANSYS, MATLAB, Fusion 360, and programming languages like
Python, C++ as all these tools would help me in analysis and simulations. This did help in
implementing projects. For example my team placed second in a project on the optimization
of engineering systems. This project required proficiency in Python. All of this has helped me
to identify my goals for pursuing a master’s degree.
While studying energy related subjects, like Thermodynamics and Thermal Systems, I learnt
that the machines we currently use to generate energy are not very efficient. A large
proportion of the energy that we get by burning fossil fuels is lost during generation and

transmission. This alarming fact threatens our very future. For one, it causes us to rapidly
deplete existing reserves of fossil fuels – which would make fuel far more expensive. Second,
the low efficiency forces us to burn more fuel than necessary to generate the required
amount of energy. This exacerbates the problem of climate change through excessive
pollution. Thus, my goal is to design more efficient machines to reduce wastage of fuels.
However, the knowledge I currently possessis not sufficient to help me achieve this goal. That
is why I wish to pursue a master’s in mechanical engineering.
My focus during my master’s would be to conduct research that would help reduce the
leakage of energy in the current designs or design new devices that are more efficient. I
believe that UT Austin would be facilitative for such a research. I hope to work with Dr. David
Bogard who has conducted advanced research in turbomachinery. I believe that under his
guidance, I could develop an effective cooling system which is necessary to increase the life
and performance of any machine. This, in turn would increase the machine’s efficiency. I plan
to leverage Industry 4.0 technologies like neural networks and machine learning to achieve
this.
Another way to reduce our consumption of fossil fuels is to accelerate the transition to clean
energy. Again, UT Austin provides an ideal platform to work in this area. I plan to take courses
on clean energy such as “Clean Energy Systems” at the Energy Institute. I will also like to be a
part of the Graduate Portfolio Program in Energy Studies at the Energy Institute to understand
energy issues from an overall policy perspective. This is crucial as understanding policy
pressures and framing the right policies is as critical to transitioning to clean energy as
developing new technology. Apart from understanding the policies that govern the
development of clean energy, I would also like to attend lectures of the UT Energy Symposium
to become more aware about the most pressing energy issues and to think of ways to solve
them. I believe that on graduation from UT Austin, I will be able to work on these areas in
companies like Baker Hughes, Bowman, Vertech and WSB Inc. . Working with such companies
will allow me to put my knowledge to practice and implement innovative ideas to solve the
important problems related to clean energy systems and leakage of energy. To sum up, UT
Austin is a place that will help me achieve my goal of reducing our consumption


Sample SOP 5: Masters in Engineering Management
     “What do ‘stocks’ mean?”
Her puzzled eyes looked at me for answers. Amruta, a girl all of 10, was at odds with the word. In 2021, I
worked with many NGOs supporting their efforts in making education accessible to underprivileged children.
Working as a Project Manager at TechForChange- I met Amruta- a young girl who was studying in a school
supported by one of the NGOs we were working with. Explaining the basics of finance to her , I experienced
the lack of financial literacy in India (990 million Indians are financially illiterate). The lack of financial literacy
forces millions of Indians into debt traps and bankruptcy. In fact, it is estimated that in 2019, one Indian
committed suicide every two hours due to bankruptcy. Looking at Amruta’s puzzled eyes shine on learning
what stocks meant, I knew it was my responsibility to solve this problem.

By 2028, I will launch ‘India’s First Financial Literacy App’ specifically curated to the needs of the semi-
literate population of India. In 6 years, India is projected to have 300 million employed people within the age

group of 18-25, with a disposable income of $2000 per annum. I aim to leverage internet penetration and
the power of AI, to create an App that will provide value to these people in four ways. (1) Improve
Accessibility: My experience with TechForChange taught me that in a diverse country like India, language
barrier is a real issue. To mitigate the same my app will be available in more than 22 languages supported by
robust voice assist. (2) Increase Awareness: A set of carefully curated and adaptive coursework which would
teach users various financial concepts (3) Accelerate Participation in the Digital Economy: As India strives

towards becoming a cash-less nation, my app would partner with several investment applications via cash-
less mediums. (4) Provide Cognitive Learning: The app would keep track of the savings and investment

behaviour of the user to suggest ways to improvise on both.
To achieve the above goal, I need to be three people in one- an entrepreneur, a financer and an innovator.
One can only connect the dots looking backwards. When I look back on my experiences, they fill me with
optimism and hope, as I have delivered results in each one of those roles.
Chapter 1: The Entrepreneur
In my junior year of engineering, I came across the India Innovation Challenge Design Contest- a start-up
challenge organized by Texas Instruments. Leading a team of 6, I decided our product should focus on India’s
famed white revolution- increasing the milk yield from Indian cattle- due to the fact that India has 75M dairy
farms and yet milk production is unable to match the ever-rising demand. To start, we interviewed many
dairy farmers and realized that cattle health was the most important variable. We then designed a prototype
of a ‘collar’ for the cows that would provide real-time data on cattle health. The question was how would
we analyse the information the collar provides?
Using my ML acumen, I deployed a Support Vector Machine algorithm to classify different cattle ailments
(accuracy: 85%) and the Random Forest algorithm to determine if the cow was in the estrus cycle (accuracy:
89%). I put myself in shoes of end-user (i.e., the farmer) to envision the product roadmap which helped me
create an easy-to-understand dashboard that displayed data and supervise the task of creating financial
projections and marketing plans. This 360-degree effort bore fruits as my team was shortlisted in the top 12
out of 10,000+ teams, and was awarded incubation at IIM Bangalore- India’s premier B-school!
Chapter 2: The Financer
My journey into the stock market started out with a disaster. I lost $100 within my first month of investing
due to my inexperience and inability to distil insights from all the information available. Realizing the
importance of said information and its power to inform user decisions, I decided to undertake a project
which would help predict stock prices using AI.
I researched stock market trends over the previous 7 years and collated a historical dataset to come up with
predictions. As a next step, I suggested the LSTM RNN algorithm which led to a decrease in MAPE (Mean
absolute percentage error) (from 10.3 to 2). To ensure maximum coverage, I analysed financial news

headlines to deduce market sentiments and used them to influence the prediction. Finally, I designed a web-
App that would provide a user-friendly interface for a market novice. My project was published in the

prestigious IEEE Xplore (link) and was elected as the best project in the department. Personally, this project
helped me understand the market and is one of the cornerstones of my current thriving portfolio.
Chapter 3: The Innovator

In my senior year, I was selected for a competitive research assistantship at one of the top B-schools in Asia-
SPJIMR. The objective of the research was to identify features influencing purchase behaviour of gift coupons

at an American retail company. The dataset was huge (12685 entries) and involved challenging cleaning
processes as it was procured through surveys. The main focus was to arrive at an accurate model: input of
which would be customer demographics like gender, occupation, etc. and the output would predict whether
the customer would buy the gif coupon.
I applied each of the relevant models individually and realized that maximum accuracy( 81%) was achieved
through the Random Forest algorithm. However, I believed there could be an opportunity to increase the
accuracy. So, I did extensive research and came across an ensembling method called stacking. Using my
fluency in Python, I created a custom stacking algorithm, combining different algorithms like Neural
Networks, Random Forest, and CatBoost Classifier, which increased the accuracy of the model by 5% and led
to feature changes in the final feature importance analysis.
The above experiences have taught me ‘how’ I can achieve my goal of starting ‘India’s First Financial Literacy
App’. However, I need an amalgamation of business and technical skills to allow me to launch faster and
scale quickly.
Pursuing the Management Science and Engineering program at Stanford University will be the perfect way
for me to achieve my goal- strengthening my skills and giving me a solid foundation to build upon. The
courses MS&E 275: Intelligent Growth in Startups and MS&E 272: Entrepreneurship Without Borders would
equip me with techniques needed to strategize my solution, knowledge to thoroughly understand India’s
emerging market, methods to build an effective team and achieve product market fit. Further, the course
on [x], would expose me to core financial concepts required. The work of Kathleen Eisenhardt on creating a
robust business model and Charles Eesley’s experience working with a similar segment of the Indian
populace in his first entrepreneurial venture would greatly benefit my learning. The opportunity to undergo
an internship will allow me to work as a Product Manager at a financial services firm, imbibing both- work
experience in the field of finance and hands-on training for my start-up. The quintessential cherry is Stanford
University’s legacy of producing entrepreneurs who have impacted specific sectors of society. By leveraging
the Stanford Technology Ventures Program (STVP)’s exposure I can polish my business model to the finest
detail, test my ideas and get valuable feedback.
Fast forward to 2030 – over 1 million Indians in the 18-25 age group are users of my app and have an
understanding of finance. Three fourths have a savings rate in excess of 15% and around one-third have
made investments in a variety of capital instruments giving them a passive income stream. This is what I
envision my future to be. I am certain that the experience gained through the three chapters of my life, the
learnings from the MS&E program and the tag as a Stanford alumnus, will help me enable others to no just
earn money, but live life on their own terms!


          """
    return sample_sops
instructions=get_instructions()
sample_sops=get_sample_sops()
def generate_sop(
        engine,
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
):
    if engine == "gpt-3.5":
        model_name = "gpt-3.5-turbo-16k"
    elif engine == "gpt-4":
        model_name = "gpt-4"
    elif not engine:
        model_name = "gpt-3.5-turbo-16k"
    else:
        raise ValueError("Invalid engine. Supported engines are 'gpt-3.5' and 'gpt-4'.")
    if resume_text is None:
        resume = ""
    else:
        resume = f"Also consider the following skills and work experiance while writing the SOP, if you think it fits. {resume_text}"

    completion = openai.ChatCompletion.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": f"""
                {instructions} Here are some sample SOPs you can train yourself on and mimic their style:
                \n {sample_sops}
                """,
            },
            {
                "role": "user",
                "content": f"""Write an SOP with a word limit of minimum {word_limit} and maximum 1100
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
    print("jh")
    sop_content = completion.choices[0]["message"]["content"]
    print(sop_content)
    return sop_content


def resume_summarize_with_gpt(resume_text):

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.3,
        max_tokens=300,
        messages=[
            {
                "role": "system",
                "content": f"""You are an excellant writer. You read resumes and provide a 150 word summary of their skills and experiances, based on the text from the resume 
                \n {sample_sops}
                """,
            },
            {
                "role": "user",
                "content": f"""Summarize this resume in 150 words {resume_text}
                """,
            },
        ],
    )

    resume = completion.choices[0]["message"]["content"]
    return resume
