import streamlit as st
from utils.file_processor import extract_text_from_file
from file_factory.doc_builder import create_cover_letter_pdf
import os

def render_cover_letter_builder(engine):
    st.header("✉️ Enhancv Cover Letter Builder")
    st.markdown("Tell your story with a professionally designed cover letter.")

    # Wizard State Management
    if 'cl_step' not in st.session_state:
        st.session_state['cl_step'] = 1

    # Progress Bar
    steps = ["1. Story & Details", "2. AI Generation", "3. Design & Export"]
    current_step = st.session_state['cl_step']
    st.progress(current_step / 3)
    st.caption(f"Step {current_step} of 3: {steps[current_step-1]}")

    # --- STEP 1: INPUTS ---
    if current_step == 1:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Your Story")
            # Resume Source
            resume_text = ""
            if 'resume_data' in st.session_state and st.session_state['resume_data'].get('experience'):
                st.success("✅ Using data from Resume Builder")
                data = st.session_state['resume_data']
                resume_text = f"Name: {data['contact'].get('name')}\nSummary: {data.get('summary')}\n"
                for exp in data.get('experience', []):
                    resume_text += f"Role: {exp.get('title')} at {exp.get('company')}\n{exp.get('description')}\n"
            elif 'li_resume_input' in st.session_state and st.session_state['li_resume_input']:
                 st.success("✅ Using uploaded resume from LinkedIn Optimizer")
                 resume_text = st.session_state['li_resume_input']
            else:
                uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"], key="cl_resume_upload")
                if uploaded_file:
                    resume_text = extract_text_from_file(uploaded_file.getvalue(), uploaded_file.type)
            
            st.session_state['cl_resume_text'] = resume_text

        with col2:
            st.subheader("Target Role")
            job_description = st.text_area("Paste Job Description", height=200, placeholder="Paste the JD here...", key="cl_jd")
            tone = st.selectbox("Select Tone", ["Professional", "Enthusiastic", "Confident", "Creative", "Storyteller"], index=0, key="cl_tone")

        if st.button("Next: Generate Draft ➡️", type="primary"):
            if st.session_state.get('cl_resume_text') and job_description:
                st.session_state['cl_step'] = 2
                st.rerun()
            else:
                st.error("Please provide both Resume and Job Description.")

    # --- STEP 2: GENERATION ---
    elif current_step == 2:
        st.subheader("Drafting your narrative...")
        
        if 'cl_generated_content' not in st.session_state:
            with st.spinner("AI is writing your cover letter..."):
                content = engine.generate_cover_letter(
                    st.session_state['cl_resume_text'], 
                    st.session_state['cl_jd'], 
                    st.session_state['cl_tone']
                )
                st.session_state['cl_generated_content'] = content
        
        # Editable Preview
        edited_content = st.text_area("Refine Content", value=st.session_state['cl_generated_content'], height=400)
        st.session_state['cl_final_content'] = edited_content
        
        col_nav1, col_nav2 = st.columns([1, 4])
        with col_nav1:
            if st.button("⬅️ Back"):
                st.session_state['cl_step'] = 1
                st.rerun()
        with col_nav2:
            if st.button("Next: Design & Export ➡️", type="primary"):
                st.session_state['cl_step'] = 3
                st.rerun()

    # --- STEP 3: DESIGN & EXPORT ---
    elif current_step == 3:
        col_design, col_preview = st.columns([1, 2])
        
        with col_design:
            st.subheader("🎨 Design Studio")
            
            template = st.selectbox("Template", ["Simple", "Modern", "Creative"], key="cl_template")
            font = st.selectbox("Font", ["Arial", "Times New Roman", "Courier"], key="cl_font")
            color = st.color_picker("Accent Color", "#000000", key="cl_color")
            
            st.divider()
            
            if st.button("⬅️ Edit Content"):
                st.session_state['cl_step'] = 2
                st.rerun()
                
            if st.button("🔄 Start Over"):
                st.session_state['cl_step'] = 1
                del st.session_state['cl_generated_content']
                st.rerun()

        with col_preview:
            st.subheader("📄 Live Preview")
            
            # Simple HTML Preview
            html_preview = f"""
            <div style="
                font-family: {font}, sans-serif; 
                color: #333; 
                padding: 40px; 
                border: 1px solid #ddd; 
                background: white; 
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                white-space: pre-wrap;
                line-height: 1.6;
            ">
                <div style="color: {color}; font-weight: bold; margin-bottom: 20px;">{st.session_state.get('cl_final_content', '').splitlines()[0] if st.session_state.get('cl_final_content') else 'Header'}</div>
                {st.session_state.get('cl_final_content', '')}
            </div>
            """
            st.markdown(html_preview, unsafe_allow_html=True)
            
            st.divider()
            
            # PDF Generation
            if st.button("⬇️ Download PDF", type="primary"):
                output_path = "Generated_Cover_Letter.pdf"
                design_config = {'color': color, 'font': font, 'template': template}
                
                success = create_cover_letter_pdf(st.session_state['cl_final_content'], output_path, design_config)
                
                if success:
                    with open(output_path, "rb") as file:
                        st.download_button(
                            label="Click to Save PDF",
                            data=file,
                            file_name="My_Cover_Letter.pdf",
                            mime="application/pdf"
                        )
                    st.success("PDF Generated Successfully!")
                else:
                    st.error("Failed to generate PDF. Please try again.")
