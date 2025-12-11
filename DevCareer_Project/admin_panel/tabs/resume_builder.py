import streamlit as st
from streamlit_quill import st_quill
from file_factory.doc_builder import generate_structured_html_preview, create_structured_resume_docx
from admin_panel.tabs.template_gallery import get_all_templates

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

    # --- AI Resume Assistant (Enhanced) ---
    with st.expander("🤖 AI Resume Assistant", expanded=True):
        st.info("Tailor your resume to a specific job description.")
        
        col_jd1, col_jd2 = st.columns([2, 1])
        with col_jd1:
            target_jd = st.text_area("Paste Target Job Description", height=150, placeholder="Paste the JD here to get keyword recommendations...", key="rb_target_jd")
        
        with col_jd2:
            st.markdown("### Match Score")
            if target_jd:
                if st.button("Analyze Match"):
                    # Construct resume text for analysis
                    resume_text = f"{data.get('summary', '')} {data.get('skills', '')}"
                    for exp in data.get('experience', []):
                        resume_text += f" {exp.get('title', '')} {exp.get('description', '')}"
                    
                    with st.spinner("Analyzing keywords..."):
                        match_data = engine.match_keywords(resume_text, target_jd)
                        if match_data:
                            st.session_state['rb_match_data'] = match_data
            
            if 'rb_match_data' in st.session_state:
                md = st.session_state['rb_match_data']
                score = int(md.get('match_score', 0))
                st.metric("ATS Score", f"{score}/100")
                if score < 70:
                    st.warning("Low Match")
                else:
                    st.success("Good Match!")
        
        if 'rb_match_data' in st.session_state:
            md = st.session_state['rb_match_data']
            st.markdown("**Missing Keywords:**")
            st.write(", ".join(md.get('missing_keywords', [])))

    st.divider()

    # --- Layout: 2 Columns (Builder vs Preview) ---
    col_builder, col_preview = st.columns([1, 1])
    
    with col_builder:
        st.subheader("📝 Resume Builder")
        
        # --- Resume Sample Library ---
        with st.expander("📚 Resume Sample Library", expanded=False):
            st.info("Choose a professional template to get started.")
            
            # Sample Data (Mocking the structure)
            SAMPLE_RESUMES = {
                "Spotify (Tech)": {
                    "category": "Backend",
                    "config": {"color": "#1DB954", "font": "Roboto", "layout": "Modern (Left Column)"},
                    "data": {
                        "contact": {"name": "Sarah Jenkins", "location": "San Francisco, CA", "role": "Senior Backend Engineer"},
                        "summary": "Backend Engineer with 5+ years of experience in streaming architecture and high-scale distributed systems.",
                        "experience": [{"title": "Backend Engineer", "company": "Spotify", "dates": "2019-Present", "description": "<ul><li>Optimized music recommendation algorithms.</li><li>Reduced latency by 40% using Go.</li></ul>"}],
                        "skills": "Go, Python, Kubernetes, AWS, Microservices"
                    }
                },
                "Netflix (Full Stack)": {
                    "category": "Full Stack",
                    "config": {"color": "#E50914", "font": "Montserrat", "layout": "Classic (Single Column)"},
                    "data": {
                        "contact": {"name": "Alex Chen", "location": "Los Gatos, CA", "role": "Senior Full Stack Engineer"},
                        "summary": "Full Stack Engineer specializing in high-performance web applications and micro-frontends.",
                        "experience": [{"title": "Senior Engineer", "company": "Netflix", "dates": "2020-Present", "description": "<ul><li>Re-architected the playback UI using React and GraphQL.</li><li>Improved load times by 30% via server-side rendering.</li></ul>"}],
                        "skills": "React, Node.js, GraphQL, TypeScript, AWS"
                    }
                },
                "Amazon (DevOps)": {
                    "category": "DevOps",
                    "config": {"color": "#FF9900", "font": "Lato", "layout": "Modern (Left Column)"},
                    "data": {
                        "contact": {"name": "Priya Patel", "location": "Seattle, WA", "role": "DevOps Engineer"},
                        "summary": "DevOps specialist focused on CI/CD automation and cloud infrastructure scalability.",
                        "experience": [{"title": "DevOps Engineer", "company": "Amazon AWS", "dates": "2021-Present", "description": "<ul><li>Automated deployment pipelines using Jenkins and Terraform.</li><li>Managed Kubernetes clusters for high-availability services.</li></ul>"}],
                        "skills": "AWS, Docker, Kubernetes, Terraform, Python"
                    }
                },
                "Google (Data Science)": {
                    "category": "Data Science",
                    "config": {"color": "#4285F4", "font": "Open Sans", "layout": "Classic (Single Column)"},
                    "data": {
                        "contact": {"name": "David Kim", "location": "Mountain View, CA", "role": "Data Scientist"},
                        "summary": "Data Scientist with a focus on machine learning models and large-scale data analysis.",
                        "experience": [{"title": "Data Scientist", "company": "Google", "dates": "2019-Present", "description": "<ul><li>Developed recommendation models using TensorFlow.</li><li>Analyzed petabytes of user interaction data using BigQuery.</li></ul>"}],
                        "skills": "Python, TensorFlow, SQL, BigQuery, Machine Learning"
                    }
                },
                "Palo Alto (Cybersecurity)": {
                    "category": "Cybersecurity",
                    "config": {"color": "#FA582D", "font": "Roboto", "layout": "Modern (Left Column)"},
                    "data": {
                        "contact": {"name": "Marcus Johnson", "location": "Santa Clara, CA", "role": "Security Analyst"},
                        "summary": "Cybersecurity Analyst dedicated to protecting enterprise infrastructure from advanced threats.",
                        "experience": [{"title": "Security Analyst", "company": "Palo Alto Networks", "dates": "2020-Present", "description": "<ul><li>Monitored SOC dashboards for intrusion attempts.</li><li>Conducted penetration testing on internal APIs.</li></ul>"}],
                        "skills": "Network Security, Python, Wireshark, SIEM, Penetration Testing"
                    }
                },
                "Uber (Mobile Dev)": {
                    "category": "Mobile",
                    "config": {"color": "#000000", "font": "Montserrat", "layout": "Classic (Single Column)"},
                    "data": {
                        "contact": {"name": "Emily Davis", "location": "San Francisco, CA", "role": "Mobile Engineer"},
                        "summary": "Mobile Engineer expert in building cross-platform apps with Flutter and React Native.",
                        "experience": [{"title": "Mobile Engineer", "company": "Uber", "dates": "2021-Present", "description": "<ul><li>Optimized the driver app for low-bandwidth conditions.</li><li>Implemented real-time location tracking features.</li></ul>"}],
                        "skills": "Flutter, Dart, React Native, iOS, Android"
                    }
                }
            }
            
            # Filter
            categories = ["All", "Backend", "Full Stack", "DevOps", "Data Science", "Cybersecurity", "Mobile"]
            selected_cat = st.selectbox("Filter by Category", categories)
            
            # Display Grid
            cols = st.columns(3)
            for i, (name, sample) in enumerate(SAMPLE_RESUMES.items()):
                if selected_cat == "All" or sample["category"] == selected_cat:
                    with cols[i % 3]:
                        st.markdown(f"**{name}**")
                        st.caption(sample["category"])
                        # Placeholder for thumbnail
                        st.markdown(f"<div style='background-color:#333; height:100px; border-radius:5px; display:flex; align-items:center; justify-content:center; color:#888;'>{name} Preview</div>", unsafe_allow_html=True)
                        if st.button(f"Use {name}", key=f"use_sample_{i}"):
                            # Smart Template Logic
                            current_name = st.session_state['resume_data']['contact'].get('name', '')
                            
                            # 1. Apply Design Config (Always)
                            if 'config' in sample:
                                st.session_state['design_color'] = sample['config']['color']
                                st.session_state['design_font'] = sample['config']['font']
                                st.session_state['design_layout'] = sample['config']['layout']
                            
                            # 2. Apply Content (Only if user data is empty)
                            if not current_name:
                                base_structure = {
                                    'contact': {}, 'summary': '', 'experience': [], 'projects': [], 
                                    'education': [], 'skills': '', 'certifications': '', 'languages': ''
                                }
                                base_structure.update(sample['data'])
                                st.session_state['resume_data'] = base_structure
                                st.success(f"Loaded {name} Template & Content!")
                            else:
                                st.success(f"Applied {name} Design Style to your resume!")
                                
                            st.rerun()
            st.divider()

        # --- Executive Resume Converter ---
        with st.expander("💼 Executive Resume Converter", expanded=False):
            st.markdown("### Transform your profile into a Board-Ready Resume")
            st.info("Upload your LinkedIn PDF or current resume. Our AI will extract, polish, and reformat it into a premium design.")
            
            col_import1, col_import2 = st.columns([2, 1])
            with col_import1:
                uploaded_resume = st.file_uploader("Upload Resume / LinkedIn PDF", type=["pdf", "docx"], key="builder_import")
            
            with col_import2:
                st.write("") # Spacer
                st.write("") # Spacer
                auto_theme = st.checkbox("Auto-Apply Premium Theme", value=True, help="Automatically selects a stunning design for you.")
                auto_polish = st.checkbox("✨ AI Content Polish", value=True, help="Fixes typos, improves tone, and standardizes formatting.")
            
            if uploaded_resume is not None:
                if st.button("✨ Transform & Upgrade", type="primary"):
                    from utils.file_processor import extract_text_from_file
                    with st.spinner("Analyzing & Polishing Content..."):
                        text = extract_text_from_file(uploaded_resume.getvalue(), uploaded_resume.type)
                        if text.startswith("Error"):
                            st.error(text)
                        else:
                            parsed_data = engine.parse_resume_json(text)
                            if parsed_data:
                                st.session_state['resume_data'] = parsed_data
                                
                                # Auto-Apply Theme Logic
                                if auto_theme:
                                    import random
                                    all_templates = get_all_templates()
                                    # Prefer "Modern" or "Tech" templates for the "Wow" factor
                                    premium_templates = [t for t in all_templates if t['category'] in ['Professional', 'Tech', 'Creative']]
                                    if premium_templates:
                                        selected_tmpl = random.choice(premium_templates)
                                        st.session_state['design_color'] = selected_tmpl['config']['color']
                                        st.session_state['design_font'] = selected_tmpl['config']['font']
                                        st.session_state['design_layout'] = selected_tmpl['config']['layout']
                                        st.toast(f"Applied Theme: {selected_tmpl['name']}")
                                
                                st.success("Resume Converted Successfully!")
                                st.rerun()
                            else:
                                st.error("Failed to parse resume data.")

        # --- Theme Gallery (50+ Styles) ---
        with st.expander("🎨 Theme Gallery (50+ Styles)", expanded=False):
            st.info("Select a visual theme to instantly style your resume.")
            
            all_templates = get_all_templates()
            
            # Filter by Category
            theme_cats = ["All", "Professional", "Tech", "Creative", "Academic", "Curated"]
            sel_theme_cat = st.selectbox("Filter Themes", theme_cats)
            
            # Display Logic: Group by Category
            categories_to_show = theme_cats[1:] if sel_theme_cat == "All" else [sel_theme_cat]
            
            for cat in categories_to_show:
                # Filter templates for this category
                cat_templates = [t for t in all_templates if t["category"] == cat]
                
                if cat_templates:
                    st.markdown(f"### {cat}")
                    t_cols = st.columns(3)
                    
                    for i, tmpl in enumerate(cat_templates):
                        with t_cols[i % 3]:
                            # Card Styling
                            color = tmpl['config']['color']
                            font = tmpl['config']['font']
                            layout = tmpl['config']['layout'].split()[0]
                            
                            with st.container(border=True):
                                # Header with Color
                                st.markdown(f"""
                                <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 10px;'>
                                    <div style='background-color:{color}; width:40px; height:40px; border-radius:8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'></div>
                                    <div>
                                        <div style='font-weight: bold; font-size: 16px;'>{tmpl['name']}</div>
                                        <div style='font-size: 12px; color: #666;'>{font} • {layout}</div>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Unique key using category and index to avoid conflicts
                                if st.button("Apply Theme", key=f"apply_theme_{cat}_{i}", use_container_width=True):
                                    st.session_state['design_color'] = tmpl['config']['color']
                                    st.session_state['design_font'] = tmpl['config']['font']
                                    st.session_state['design_layout'] = tmpl['config']['layout']
                                    st.success(f"Applied {tmpl['name']}!")
                                    st.rerun()
                    st.divider()

        # --- Design Studio ---
        with st.expander("🛠️ Custom Design Studio", expanded=True):
            st.markdown("Fine-tune your resume look and feel.")
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                accent_color = st.color_picker("Accent Color", st.session_state.get('design_color', "#2E74B5"), key="design_color")
                layout_style = st.selectbox("Layout", ["Classic (Single Column)", "Modern (Left Column)"], index=0 if st.session_state.get('design_layout', "Classic").startswith("Classic") else 1, key="design_layout")
            with col_d2:
                # Find index of current font
                fonts = ["Arial", "Calibri", "Roboto", "Open Sans", "Lato", "Montserrat", "Times New Roman"]
                try:
                    font_idx = fonts.index(st.session_state.get('design_font', "Arial"))
                except ValueError:
                    font_idx = 0
                font_style = st.selectbox("Font", fonts, index=font_idx, key="design_font")
            
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
            col_sum1, col_sum2 = st.columns([3, 1])
            with col_sum1:
                data['summary'] = st.text_area("Bio / Summary", data.get('summary', ''), height=100)
            with col_sum2:
                if st.button("✨ Rewrite", key="rewrite_summary"):
                    if data.get('summary'):
                        with st.spinner("Improving..."):
                            improved = engine.improve_content(data['summary'])
                            data['summary'] = improved
                            st.rerun()

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
                col_exp_btn1, col_exp_btn2 = st.columns(2)
                with col_exp_btn1:
                    if st.button(f"✨ Generate Bullets", key=f"gen_bullets_{i}"):
                        with st.spinner("Generating metrics..."):
                            bullets = engine.generate_bullets(exp['title'], exp['company'], "General software engineering tasks")
                            exp['description'] = bullets
                with col_exp_btn2:
                    if st.button(f"✨ Improve Text", key=f"improve_exp_{i}"):
                        if exp.get('description'):
                            with st.spinner("Polishing..."):
                                improved = engine.improve_content(exp['description'])
                                exp['description'] = improved
                                st.rerun()
                
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
