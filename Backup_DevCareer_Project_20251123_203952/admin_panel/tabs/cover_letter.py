import streamlit as st
from utils.file_processor import extract_text_from_file

def render_cover_letter_builder(engine):
    st.header("✉️ Cover Letter Builder")
    st.markdown("Generate a tailored cover letter in seconds.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("1. Inputs")
        
        # Resume Source
        resume_text = ""
        
        # Check if resume is already in session state from other tabs
        if 'resume_data' in st.session_state and st.session_state['resume_data'].get('experience'):
            st.info("Using data from Resume Builder.")
            # Construct a basic text representation from structured data for the AI
            data = st.session_state['resume_data']
            resume_text = f"Name: {data['contact'].get('name')}\nSummary: {data.get('summary')}\n"
            for exp in data.get('experience', []):
                resume_text += f"Role: {exp.get('title')} at {exp.get('company')}\n{exp.get('description')}\n"
        elif 'li_resume_input' in st.session_state and st.session_state['li_resume_input']:
             st.info("Using uploaded resume from LinkedIn Optimizer.")
             resume_text = st.session_state['li_resume_input']
        else:
            st.warning("No resume found. Please upload one below.")
            uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"], key="cl_resume_upload")
            if uploaded_file:
                resume_text = extract_text_from_file(uploaded_file.getvalue(), uploaded_file.type)

        # Job Description
        job_description = st.text_area("Paste Job Description", height=200, placeholder="Paste the JD here...")
        
        # Tone
        tone = st.selectbox("Select Tone", ["Professional", "Enthusiastic", "Confident", "Creative"], index=0)

        generate_btn = st.button("✨ Generate Cover Letter", type="primary")

    with col2:
        st.subheader("2. Result")
        
        if generate_btn:
            if resume_text and job_description:
                with st.spinner("Drafting your cover letter..."):
                    cover_letter = engine.generate_cover_letter(resume_text, job_description, tone)
                    st.session_state['cover_letter_result'] = cover_letter
            else:
                st.error("Please ensure you have a Resume and Job Description.")

        if 'cover_letter_result' in st.session_state:
            # Editable Text Area
            edited_letter = st.text_area("Edit Letter", value=st.session_state['cover_letter_result'], height=400)
            
            # Download Button
            st.download_button(
                label="Download as Text File",
                data=edited_letter,
                file_name="Cover_Letter.txt",
                mime="text/plain"
            )
