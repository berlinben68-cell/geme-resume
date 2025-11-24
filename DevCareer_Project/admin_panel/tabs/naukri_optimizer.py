import streamlit as st
from utils.file_processor import extract_text_from_file

def render_naukri_optimizer(engine):
    st.header("🇮🇳 Naukri.com Profile Optimizer")
    st.markdown("Optimize your profile for India's #1 Job Portal. Crack the algorithm.")

    col1, col2 = st.columns(2)
    
    with col1:
        resume_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"], key="naukri_uploader")
        resume_text = ""
        
        if resume_file is not None:
            resume_text = extract_text_from_file(resume_file.getvalue(), resume_file.type)
            if resume_text.startswith("Error"):
                st.error(resume_text)
            else:
                st.success("Resume Loaded!")
                
                # Auto-Extract Role if not already set or if new file
                if 'naukri_extracted_file' not in st.session_state or st.session_state.get('naukri_extracted_file') != resume_file.name:
                    # Update resume text in session state so text_area picks it up
                    st.session_state['naukri_resume_text'] = resume_text
                    
                    with st.spinner("Auto-detecting Target Role..."):
                        extracted = engine.extract_role_and_stack(resume_text)
                        st.session_state['naukri_role'] = extracted.get('role', '')
                        st.session_state['naukri_extracted_file'] = resume_file.name
                        st.rerun()
        
        resume_input = st.text_area("Or Paste Resume Content", value=resume_text, height=300, key="naukri_resume_text")

    with col2:
        target_role = st.text_input("Target Role", placeholder="e.g. Senior Java Developer", key="naukri_role")
        st.info("Naukri's algorithm heavily weights the **Resume Headline** and **Key Skills**. This tool generates optimized versions for you.")
        
        if st.button("🚀 Optimize for Naukri"):
            if resume_input and target_role:
                with st.spinner("Analyzing Naukri Algorithm..."):
                    optimized_content = engine.optimize_naukri_profile(resume_input, target_role)
                    st.session_state['naukri_result'] = optimized_content
            else:
                st.error("Please provide Resume and Target Role.")

    if 'naukri_result' in st.session_state:
        st.divider()
        st.subheader("✅ Optimization Kit")
        st.markdown(st.session_state['naukri_result'])
        
        st.download_button(
            label="Download Kit (TXT)",
            data=st.session_state['naukri_result'],
            file_name="Naukri_Optimization_Kit.txt",
            mime="text/plain"
        )
