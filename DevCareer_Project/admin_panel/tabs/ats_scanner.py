import streamlit as st
from utils.file_processor import extract_text_from_file

def render_ats_scanner(engine):
    st.header("📊 ATS Scanner & Scorer")
    st.markdown("Analyze your resume against Applicant Tracking Systems.")

    ats_tab1, ats_tab2 = st.tabs(["🛡️ Universal ATS Audit", "🎯 Job Description Match"])

    # --- Sub-Tab 1: Universal Audit (No JD) ---
    with ats_tab1:
        st.subheader("Universal ATS Audit")
        st.info("See what the bot sees. Check for parsing errors and formatting red flags.")
        
        audit_file = st.file_uploader("Upload Resume for Audit", type=["pdf", "docx"], key="ats_audit_uploader")
        
        if audit_file is not None:
            audit_text = extract_text_from_file(audit_file.getvalue(), audit_file.type)
            
            if st.button("Run Universal Scan"):
                print("DEBUG: Run Universal Scan button clicked")
                with st.spinner("Simulating ATS Parsing..."):
                    # 1. Parsing Simulation
                    print("DEBUG: Calling simulate_ats_parsing...")
                    parsed_data = engine.simulate_ats_parsing(audit_text)
                    print(f"DEBUG: parsed_data result: {parsed_data}")
                    
                    # 2. Formatting Audit
                    print("DEBUG: Calling audit_resume_formatting...")
                    audit_report = engine.audit_resume_formatting(audit_text)
                    print("DEBUG: audit_report received")
                    
                    # Display Results
                    col_p1, col_p2 = st.columns(2)
                    
                    with col_p1:
                        st.markdown("### 🤖 ATS Parsed Data")
                        st.json(parsed_data)
                    
                    with col_p2:
                        st.markdown("### 📝 Formatting Report")
                        st.markdown(audit_report)

    # --- Sub-Tab 2: Job Match (Existing Logic) ---
    with ats_tab2:
        st.subheader("Job Description Match")
        col1, col2 = st.columns(2)
        
        with col1:
            ats_market = st.radio("Target Market", ["India", "UAE"], horizontal=True)
            ats_resume_file = st.file_uploader("Upload Resume for Scoring", type=["pdf", "docx"], key="ats_score_uploader")
            ats_resume_text = ""
            
            if ats_resume_file is not None:
                ats_resume_text = extract_text_from_file(ats_resume_file.getvalue(), ats_resume_file.type)
                if ats_resume_text.startswith("Error"):
                    st.error(ats_resume_text)
                else:
                    # Auto-update text area
                    if 'ats_score_file' not in st.session_state or st.session_state.get('ats_score_file') != ats_resume_file.name:
                        st.session_state['ats_score_input'] = ats_resume_text
                        st.session_state['ats_score_file'] = ats_resume_file.name
                        st.rerun()
            
            ats_resume_text = st.text_area("Resume Content", height=200, key="ats_score_input")

        with col2:
            jd_text = st.text_area("Paste Job Description", height=300)
            
            if st.button("Calculate Match Score"):
                if ats_resume_text and jd_text:
                    with st.spinner("Analyzing against ATS filters..."):
                        ats_result = engine.check_ats_score(ats_resume_text, jd_text, ats_market)
                        st.markdown(ats_result)
                else:
                    st.error("Please provide both Resume and Job Description.")
