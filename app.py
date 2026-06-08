import pandas as pd
import pdfplumber
import streamlit as st
import re
from gemini_helper import get_resume_feedback
import matplotlib.pyplot as plt
from smart_match import smart_skill_match
from report_generator import generate_report


@st.cache_data
def load_skills():
    return pd.read_csv("skills.csv")


@st.cache_data
def cached_ai_response(prompt):
    return get_resume_feedback(prompt)


# now we make interface from here
st.title("ATS Resume Analyser")

resume = st.file_uploader("upload your resume in pdf format", type=["pdf"])
job_description = st.text_area("enter the job description")

# extract resme content


if resume is not None:

    text = ""

    with pdfplumber.open(resume) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text

    st.success("Resume Uploaded Successfully!")

    if not job_description.strip():

        st.warning(
            "Please enter a job description."
        )

        st.stop()    

    st.subheader("Extracted Resume Text")

    st.text_area(
        "Resume Content",
        text,
        height=300
    )

    # Extract skill

    skills_df = load_skills()

    resume_text = text.lower()

    found_skills = []

    for skill in skills_df.iloc[:, 0]:

        pattern = r'\b' + re.escape(skill.lower()) + r'\b'

        if re.search(pattern, resume_text):
            found_skills.append(skill)

    found_skills = list(dict.fromkeys(found_skills))

    st.subheader("Detected Skills")

    st.write(", ".join(found_skills))

    jd_text = job_description.lower()

   # Extract JD
   
    jd_skills = []

    for skill in skills_df.iloc[:,0]:

        pattern = r'\b' + re.escape(skill.lower()) + r'\b'

        if re.search(pattern, jd_text):
            jd_skills.append(skill)

    jd_skills = list(dict.fromkeys(jd_skills))

    st.subheader("Job Description Skills")

    for skill in jd_skills:
        st.success(skill)

    # matched skills

    matched_skills = smart_skill_match(
        found_skills,
        jd_skills
   )

    matched_skills = list(dict.fromkeys(matched_skills))

    for skill in matched_skills:
        st.success(skill)

    # missing skills

    missing_skills = []

    for skill in jd_skills:

        if skill not in matched_skills:

            missing_skills.append(skill)

    st.subheader("Missing Skills")

    for skill in missing_skills:
        st.error(skill)

    # ATS SCORE CALCULATION

    st.write("JD Skills:", jd_skills)
    st.write("Matched Skills:", matched_skills)

    if len(jd_skills) > 0:

        ats_score = (
            len(matched_skills)
            /
         len(jd_skills)
        ) * 100

    else:

        ats_score = 0
    
    # shwing ats score with bar

    st.subheader("ATS Score")
    ats_score = min(ats_score, 100)

    st.progress(int(ats_score))

    st.metric(
        "Score",
        f"{ats_score:.2f}%"
    )
    # analysing resume

    if ats_score >= 80:

        st.success(
            "Excellent Match! Resume is highly aligned with the job description."
        )

    elif ats_score >= 60:

        st.warning(
            "Good Match! Consider adding some missing skills."
        )

    else:

        st.error(
            "Low Match! Resume requires improvement."
        )
    # showing stats in tabular format

    st.subheader("Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Resume Skills",
            len(found_skills)
        )

    with col2:
        st.metric(
            "JD Skills",
            len(jd_skills)
        )

    with col3:
        st.metric(
            "Matched Skills",
            len(matched_skills)
        )

    # showing what to learn

    st.subheader("Recommendations")

    if len(missing_skills) > 0:

        st.write(
            "Consider adding the following skills:"
        )

        for skill in missing_skills:

            st.write(f"• {skill}")

    else:

        st.success(
            "Great! No missing skills detected."
        )
    st.subheader("Skill Match Analysis")
    matched_count = len(matched_skills)
    missing_count = len(missing_skills)

    fig, ax = plt.subplots(figsize=(5,2))

    ax.barh(
        ["Matched Skills", "Missing Skills"],
        [matched_count, missing_count]
    )

    st.pyplot(fig)
    plt.close(fig)

    # genai addition to the code through api key

    st.subheader("AI Resume Review")

    prompt = f"""
    Resume Skills:
    {found_skills}

    Job Description Skills:
    {jd_skills}

    Matched Skills:
    {matched_skills}

    Missing Skills:
    {missing_skills}

    ATS Score:
    {ats_score}

    Act as a professional recruiter.

    Provide:

    1. Strengths
    2. Weaknesses
    3. Improvement Suggestions

    Keep response concise.
    """

    if "feedback" not in st.session_state:
        st.session_state.feedback = ""

    if st.button("Generate AI Review"):

        st.session_state.feedback = cached_ai_response(
            prompt
        )

    st.markdown(st.session_state.feedback)

    st.subheader("AI Learning Roadmap")

    roadmap_prompt = f"""
    The candidate is missing these skills:

    {missing_skills}

    Create a learning roadmap.

    For each missing skill provide:

    1. What it is
    2. Why it is important
    3. Key topics to learn
    4. A mini project idea

    Use clear headings.

    Generate at least 50 words per skill.
    """

    if "roadmap" not in st.session_state:
        st.session_state.roadmap = ""

    if st.button("Generate Learning Roadmap"):

        st.session_state.roadmap = cached_ai_response(
            roadmap_prompt
        )

    st.markdown(st.session_state.roadmap)    

    # resume rewrite suggestion

    st.subheader("Resume Rewrite Suggestions")

    rewrite_prompt = f"""
    Job Description Skills:
    {jd_skills}
    
    Missing Skills:
    {missing_skills}
    
    Act as an ATS resume expert.
    
    Suggest 5 resume bullet points that naturally incorporate
    the missing skills.
    
    Rules:
    
    - Professional tone
    - Action-oriented
    - ATS friendly
    - Use resume bullet format
    - Do not invent unrealistic achievements
    """
    if "suggestions" not in st.session_state:
        st.session_state.suggestions = ""


    if st.button("Generate Resume Suggestions"):

        st.session_state.suggestions = cached_ai_response(
            rewrite_prompt
        )
        
    st.markdown( st.session_state.suggestions)    

    # report generated must not be empty

    if not st.session_state.feedback:
        st.warning("Generate AI Review first")
        st.stop()
    
    if not st.session_state.roadmap:
        st.warning("Generate Learning Roadmap first")
        st.stop()

    if not st.session_state.suggestions:
        st.warning("Generate Resume Suggestions first")
        st.stop()    

    # generate report

    st.subheader("Download ATS Report")


    if st.button("Generate PDF Report"):

        pdf_file = generate_report(
            ats_score,
            matched_skills,
            missing_skills,
            st.session_state.feedback,
            st.session_state.roadmap,
            st.session_state.suggestions 
        )

        with open(pdf_file, "rb") as file:

            st.download_button(
                label="Download Report",
            data=file,
                file_name="ATS_Report.pdf",
                mime="application/pdf"
            )    

    



    
