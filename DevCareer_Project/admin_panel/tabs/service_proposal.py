import streamlit as st

def render_service_proposal_tab(engine):
    st.header("Service Page Proposal Generator 🤝")
    st.info("Convert LinkedIn Service Page leads into paying clients with high-converting proposals.")
    
    # New Structured Inputs
    col_sp1, col_sp2 = st.columns(2)
    with col_sp1:
        sp_resume_type = st.selectbox("What type of resume?", ["Traditional resume", "Visual resume", "Infographic resume", "Federal resume", "Academic CV"])
        sp_writing_stage = st.selectbox("What stage of resume writing are you in?", ["I need revisions to an existing resume", "I need a resume from scratch", "I need a review/critique only"])
    
    with col_sp2:
        sp_career_stage = st.selectbox("Where are you in your career?", ["Early career (0-2 yrs)", "Mid career (3-10 yrs)", "Late career (10-20 yrs)", "Executive (20+ yrs)"])
        sp_industry = st.selectbox("Which industries are you focused on?", ["Technology", "Finance", "Consulting", "Healthcare", "Retail", "Manufacturing", "Other"])

    # Construct the project details string for the AI
    sp_project = f"""
    Project Details:
    - Type: {sp_resume_type}
    - Stage: {sp_writing_stage}
    - Career Level: {sp_career_stage}
    - Industry: {sp_industry}
    """
    
    # Input: PDF Upload or Text
    sp_pdf = st.file_uploader("Upload Client Profile (PDF) - e.g. LinkedIn Export", type=["pdf"], key="sp_pdf")
    
    sp_profile_final = ""
    
    # If PDF is NOT uploaded, show text area
    if not sp_pdf:
        sp_text_manual = st.text_area("Or Paste Profile Text", placeholder="e.g. Headline, About Section, Experience...", height=150)
        sp_profile_final = sp_text_manual

    if st.button("Generate Proposal"):
        # If PDF is uploaded, parse it now
        if sp_pdf:
            with st.spinner("Reading PDF..."):
                sp_profile_final = engine.parse_pdf(sp_pdf)
        
        # DEBUG
        print(f"DEBUG: Project Details: '{sp_project}'")
        print(f"DEBUG: Profile Final Length: {len(sp_profile_final)}")
        
        if sp_project and sp_profile_final:
            with st.spinner("Analyzing Profile & Generating Proposal..."):
                proposal_data = engine.generate_service_page_proposal(sp_project, sp_profile_final)
                
                if proposal_data and 'error' not in proposal_data:
                    st.success("Proposal Generated!")
                    
                    # Part 1: Internal Audit
                    with st.expander("🕵️ Internal Profile Audit (For Your Eyes Only)", expanded=True):
                        audit = proposal_data.get('resume_audit', {})
                        st.error(f"**Failure 1:** {audit.get('failure_1', '')}")
                        st.error(f"**Failure 2:** {audit.get('failure_2', '')}")
                        
                        # Before vs After
                        st.markdown("---")
                        st.markdown("### 🔄 Before vs After Transformation")
                        ba = proposal_data.get('before_after_analysis', {})
                        col_ba1, col_ba2 = st.columns(2)
                        with col_ba1:
                            st.warning(f"**Current State:**\n{ba.get('current_state', 'Generic Profile')}")
                        with col_ba2:
                            st.success(f"**Future State:**\n{ba.get('future_state', 'High-Converting Brand')}")
                    
                    # Part 2: Proposal Script
                    st.subheader("📋 Copy-Paste Proposal Script")
                    st.code(proposal_data.get('proposal_script', ''), language="text")
                elif proposal_data and 'error' in proposal_data:
                    st.error(proposal_data['error'])
                else:
                    st.error("Failed to generate proposal. Please try again.")
        else:
            st.error("Please provide Project Details and either Upload a PDF or Paste Text.")
