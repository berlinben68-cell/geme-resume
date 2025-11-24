import streamlit as st
from streamlit_quill import st_quill
from file_factory.doc_builder import generate_structured_html_preview, create_structured_resume_docx

def render_resume_builder(engine):
    # Initialize Structured Data
    if 'resume_data' not in st.session_state:
        st.session_state['resume_data'] = {
            'contact': {},
            'summary': '',
            'experience': [],
            'projects': [],
            'education': [],
            'skills': '',
            'certifications': '',
            'languages': ''
        }
    
    data = st.session_state['resume_data']

    # --- Layout: 2 Columns (Builder vs Preview) ---
    col_builder, col_preview = st.columns([1, 1])
    
    with col_builder:
        st.subheader("📝 Resume Builder")
        
        # --- Import Resume Feature ---
        with st.expander("📤 Import Resume (PDF/DOCX)", expanded=False):
            st.info("Upload your existing resume to auto-fill the builder.")
            uploaded_resume = st.file_uploader("Upload Resume", type=["pdf", "docx"], key="builder_import")
            
            if uploaded_resume is not None:
                if st.button("Import Data"):
                    from utils.file_processor import extract_text_from_file
                    with st.spinner("Extracting data..."):
                        text = extract_text_from_file(uploaded_resume.getvalue(), uploaded_resume.type)
                        if text.startswith("Error"):
                            st.error(text)
                        else:
                            parsed_data = engine.parse_resume_json(text)
                            if parsed_data:
                                st.session_state['resume_data'] = parsed_data
                                st.success("Resume Imported Successfully!")
                                st.rerun()
                            else:
                                st.error("Failed to parse resume data.")

        # --- Design Studio ---
        with st.expander("🎨 Design Studio", expanded=True):
            st.markdown("Customize your resume look and feel.")
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                accent_color = st.color_picker("Accent Color", "#2E74B5")
                layout_style = st.selectbox("Layout", ["Classic (Single Column)", "Modern (Left Column)"])
            with col_d2:
                font_style = st.selectbox("Font", ["Arial", "Calibri", "Roboto", "Open Sans", "Lato", "Montserrat", "Times New Roman"])
            
            design_config = {'color': accent_color, 'font': font_style, 'layout': layout_style}

        # 1. Contact Info
        with st.expander("👤 Contact Information"):
            data['contact']['name'] = st.text_input("Full Name", data['contact'].get('name', ''))
            data['contact']['email'] = st.text_input("Email", data['contact'].get('email', ''))
            data['contact']['phone'] = st.text_input("Phone", data['contact'].get('phone', ''))
            data['contact']['location'] = st.text_input("Location", data['contact'].get('location', ''))
            data['contact']['linkedin'] = st.text_input("LinkedIn URL", data['contact'].get('linkedin', ''))
            data['contact']['portfolio'] = st.text_input("Portfolio URL", data['contact'].get('portfolio', ''))

        # 2. Professional Summary (New)
        with st.expander("📝 Professional Summary"):
            data['summary'] = st.text_area("Bio / Summary", data.get('summary', ''), height=100)

        # 3. Experience
        with st.expander("💼 Experience"):
            if st.button("Add Job"):
                data['experience'].append({})
            
            for i, exp in enumerate(data['experience']):
                st.markdown(f"**Job {i+1}**")
                exp['title'] = st.text_input(f"Title #{i+1}", exp.get('title', ''))
                exp['company'] = st.text_input(f"Company #{i+1}", exp.get('company', ''))
                exp['dates'] = st.text_input(f"Dates #{i+1}", exp.get('dates', ''))
                exp['location'] = st.text_input(f"Location #{i+1}", exp.get('location', ''))
                
                # AI Bullet Generator
                if st.button(f"✨ Generate Bullets for Job {i+1}"):
                    with st.spinner("Generating metrics..."):
                        bullets = engine.generate_bullets(exp['title'], exp['company'], "General software engineering tasks")
                        exp['description'] = bullets
                
                exp['description'] = st_quill(value=exp.get('description', ''), html=True, key=f"quill_exp_{i}")
                st.divider()

        # 4. Projects
        with st.expander("🚀 Projects"):
            if st.button("Add Project"):
                data['projects'].append({})
            
            for i, proj in enumerate(data['projects']):
                st.markdown(f"**Project {i+1}**")
                proj['title'] = st.text_input(f"Project Name #{i+1}", proj.get('title', ''))
                proj['tech_stack'] = st.text_input(f"Tech Stack #{i+1}", proj.get('tech_stack', ''))
                proj['description'] = st_quill(value=proj.get('description', ''), html=True, key=f"quill_proj_{i}")
                st.divider()

        # 5. Education
        with st.expander("🎓 Education"):
            if st.button("Add Education"):
                data['education'].append({})
            
            for i, edu in enumerate(data['education']):
                edu['school'] = st.text_input(f"School #{i+1}", edu.get('school', ''))
                edu['degree'] = st.text_input(f"Degree #{i+1}", edu.get('degree', ''))
                edu['dates'] = st.text_input(f"Dates #{i+1}", edu.get('dates', ''))
                st.divider()

        # 6. Skills & Extras
        with st.expander("🛠️ Skills & Extras"):
            data['skills'] = st.text_area("Skills (Comma separated)", data.get('skills', ''))
            data['certifications'] = st.text_area("Certifications (One per line)", data.get('certifications', ''))
            data['languages'] = st.text_area("Languages (Comma separated)", data.get('languages', ''))

    with col_preview:
        st.subheader("👁️ Live Preview")
        
        try:
            # Pass design config to preview generator
            preview_html = generate_structured_html_preview(data, design_config)
            st.components.v1.html(preview_html, height=1000, scrolling=True)
        except Exception as e:
            st.error(f"Preview Error: {e}")

        # Download Button
        if st.button("Download Resume (DOCX)"):
            output_path = "My_Resume.docx"
            # Note: DOCX generator currently uses a simplified template system. 
            # Ideally, we'd pass the design_config there too, but for now we use the closest matching template or update it.
            # For this iteration, we'll stick to the preview being the main visual upgrade.
            if create_structured_resume_docx(data, output_path, "Standard ATS"):
                with open(output_path, "rb") as file:
                    st.download_button(
                        label="Download Resume",
                        data=file,
                        file_name=f"Resume_{data['contact'].get('name', 'User')}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
