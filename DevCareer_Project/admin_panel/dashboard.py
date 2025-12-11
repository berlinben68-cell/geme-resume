
# dashboard.py
import streamlit as st
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import importlib
import core_engine.prompts
importlib.reload(core_engine.prompts)
import core_engine.ai_logic
importlib.reload(core_engine.ai_logic)
from core_engine.ai_logic import IntelligenceEngine
from streamlit_quill import st_quill
import file_factory.doc_builder
importlib.reload(file_factory.doc_builder)
from file_factory.doc_builder import create_resume_docx, generate_html_preview, create_resume_docx_from_html
from file_factory.repo_bundler import create_project_bundle
from admin_panel.tabs.resume_builder import render_resume_builder
from admin_panel.tabs.naukri_optimizer import render_naukri_optimizer
from admin_panel.tabs.ats_scanner import render_ats_scanner

from admin_panel.tabs.cover_letter import render_cover_letter_builder


from utils.file_processor import extract_text_from_file

st.set_page_config(page_title="DevCareer OS", layout="wide")

# Sidebar for API Key
api_key = st.sidebar.text_input("Gemini API Key", type="password")
if not api_key:
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except (FileNotFoundError, KeyError):
        pass


if not api_key:
    st.warning("Please enter your Gemini API Key in the sidebar to proceed.")
    st.stop()

# @st.cache_resource
def get_engine(api_key):
    return IntelligenceEngine(api_key)

engine = get_engine(api_key)

# Tabs for different modules
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📄 Resume Builder", 
    "✉️ Cover Letter", 
    "🏗️ GitHub Architect", 
    "🔗 LinkedIn Optimizer", 
    "🤝 Service Proposal",
    "🇮🇳 Naukri Optimizer", 
    "📊 ATS Scanner"
])

# --- Tab 1: Resume Builder ---
with tab1:
    render_resume_builder(engine)
# --- Tab 2: Cover Letter ---
with tab2:
    render_cover_letter_builder(engine)

# --- Tab 5: Service Proposal ---
with tab5:
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

# --- Tab 6: Naukri Optimizer ---
with tab6:
    render_naukri_optimizer(engine)

# --- Tab 4: LinkedIn Optimizer ---
with tab4:
    st.header("LinkedIn Optimizer 🚀")
    st.caption("Transform your profile into a Recruiter Magnet in 4 simple steps.")
    
    # Initialize Session State for Wizard Data
    if 'li_wizard_step' not in st.session_state:
        st.session_state['li_wizard_step'] = 1
    
    # --- Step 1: Upload & Analyze ---
    st.subheader("Step 1: Upload Your Profile")
    with st.expander("📂 Upload Resume or LinkedIn PDF", expanded=True):
        li_resume_file = st.file_uploader("Upload Resume / LinkedIn PDF (PDF/DOCX)", type=["pdf", "docx"], key="li_resume_uploader_wizard")
        st.caption("💡 Tip: You can upload your 'Save to PDF' profile export from LinkedIn.")
        
        li_resume_text = ""
        if li_resume_file is not None:
            li_resume_text = extract_text_from_file(li_resume_file.getvalue(), li_resume_file.type)
            if li_resume_text.startswith("Error"):
                st.error(li_resume_text)
            else:
                st.success("✅ File Analyzed Successfully")
                # Auto-Extract Logic
                if 'extracted_file_wizard' not in st.session_state or st.session_state.get('extracted_file_wizard') != li_resume_file.name:
                    with st.spinner("🕵️ Auto-detecting Role & Location..."):
                        extracted = engine.extract_role_and_stack(li_resume_text)
                        # Update Widget Keys Directly to Force UI Refresh
                        st.session_state['li_role_input'] = extracted.get('role', '')
                        st.session_state['li_stack_input'] = extracted.get('stack', '')
                        st.session_state['li_url_input'] = extracted.get('linkedin_url', '')
                        
                        # Update Industry Select
                        detected_ind = extracted.get('industry', 'Technology')
                        options = ["Technology", "Finance", "Consulting", "Healthcare", "Retail", "Other"]
                        if detected_ind in options:
                            st.session_state['li_industry_select'] = detected_ind
                        else:
                             st.session_state['li_industry_select'] = "Other"

                        loc = extracted.get('location', '')
                        if loc:
                            if "UAE" in loc.upper() or "DUBAI" in loc.upper():
                                st.session_state['li_market_select'] = "UAE"
                            elif "INDIA" in loc.upper() or "BANGALORE" in loc.upper():
                                st.session_state['li_market_select'] = "India"
                            st.session_state['li_region_input'] = loc
                        
                        # Auto-extract banner content (hook, tagline, LinkedIn URL)
                        target_role = extracted.get('role', 'Professional')
                        banner_content = engine.extract_banner_content(li_resume_text, target_role)
                        
                        # Update banner customization fields
                        if banner_content:
                            st.session_state['custom_hook_input'] = banner_content.get('custom_hook', '')
                            st.session_state['custom_tagline_input'] = banner_content.get('custom_tagline', '')
                            # Update portfolio URL if LinkedIn URL was extracted
                            if banner_content.get('linkedin_url'):
                                st.session_state['portfolio_url_input'] = banner_content.get('linkedin_url')
                        
                        st.session_state['extracted_file_wizard'] = li_resume_file.name
                        st.rerun()

    # --- Step 2: Define Strategy ---
    st.subheader("Step 2: Define Your Strategy")
    with st.expander("🎯 Target Role & Market", expanded=True):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            li_role = st.text_input("Target Job Role", key="li_role_input", placeholder="e.g. Senior Product Manager")
            li_stack = st.text_input("Tech Stack / Core Skills", key="li_stack_input", placeholder="e.g. Python, AWS, React")
            li_market = st.selectbox("Target Market", ["India", "UAE", "USA", "Europe", "Other"], key="li_market_select")
        with col_s2:
            li_region = st.text_input("Target Location (City)", key="li_region_input", placeholder="e.g. Dubai")
            li_industry = st.selectbox("Target Industry", ["Technology", "Finance", "Consulting", "Healthcare", "Retail", "Other"], key="li_industry_select")
            
        st.info(f"ℹ️ **Strategy Note:** Optimizing for **{li_market}** will adjust the tone to be more *{'Formal & Executive' if li_market == 'UAE' else 'Skill-Centric & Competitive'}*.")

    # --- Step 3: Add Context (Optional) ---
    st.subheader("Step 3: Add Context (Optional)")
    with st.expander("🖼️ Visuals & URL (Click to Expand)", expanded=False):
        li_url = st.text_input("LinkedIn URL", value=st.session_state.get('li_url_wiz', ''), placeholder="https://linkedin.com/in/...", key="li_url_input")
        vis_context = st.text_area("Visual Context (Describe your photo/banner)", placeholder="e.g. I have a professional headshot in a suit, and a banner showing code.", key="vis_context_input")

    # --- Step 4: Generate & Report ---
    st.subheader("Step 4: Generate Master Kit")
    
    if st.button("🚀 Generate Optimization Kit", type="primary"):
        if li_resume_text and li_role and li_region:
            with st.spinner("🤖 AI is analyzing 50+ ranking factors..."):
                # Call Engine
                master_data = engine.generate_linkedin_master_kit(li_role, li_region, li_industry, li_resume_text, vis_context, li_url)
                
                if master_data:
                    st.session_state['master_data_wiz'] = master_data
                    st.success("🎉 Optimization Complete!")
                else:
                    st.error("Generation failed. Please try again.")
        else:
            st.warning("⚠️ Please complete Step 1 & 2 (Upload Resume, Target Role, and Location) to proceed.")

    # --- Display Results ---
    if 'master_data_wiz' in st.session_state:
        data = st.session_state['master_data_wiz']
        st.divider()
        
        # Tabs for Result View
        res_tab1, res_tab2, res_tab3, res_tab4 = st.tabs(["📊 SEO Strategy", "✍️ Content Rewrite", "🎨 Visual Audit", "⚙️ Settings"])
        
        with res_tab1:
            st.markdown("### Keyword Strategy")
            seo = data.get('seo_strategy_audit', {})
            st.write("**Primary Keywords:**")
            for k in seo.get('primary_keyword_cluster', []):
                st.caption(f"🔑 {k}")
            st.write("**Missing Keywords:**")
            for k in seo.get('keyword_gap_analysis', []):
                st.error(f"❌ {k}")

        with res_tab2:
            st.markdown("### Content Optimization")
            text = data.get('text_optimization', {})
            st.info("**Headline Options:**")
            for h in text.get('headline_options', []):
                st.write(f"- {h}")
            
            st.markdown("---")
            st.markdown("**About Section Hook:**")
            st.write(text.get('about_section', {}).get('hook', ''))
            
            st.markdown("---")
            st.markdown("**Experience Rewrite (Recent Role):**")
            exp = text.get('experience_rewrites', {})
            for bullet in exp.get('impact_statements', []):
                st.success(f"✅ {bullet}")

        with res_tab3:
            st.markdown("### Visual Brand Audit")
            vis = data.get('visual_audit', {})
            photo = vis.get('profile_photo_check', {})
            st.write(f"**Photo Score:** {photo.get('technical_score', '?')}/10")
            st.info(f"💡 Fix: {photo.get('fix', '')}")
            
            banner = vis.get('banner_image_check', {})
            st.write(f"**Banner Relevance:** {banner.get('relevance', '')}")

        with res_tab4:
            st.markdown("### URL & Settings")
            url_audit = data.get('url_settings_audit', {})
            st.write(f"**URL Status:** {url_audit.get('url_optimization', {}).get('status', '')}")
            st.warning(f"**Visibility Check:** {url_audit.get('public_visibility', '')}")

        # --- Download Section ---
        st.divider()
        st.subheader("📥 Download Your Report")
        col_d1, col_d2 = st.columns(2)
        
        with col_d1:
            # Generate PDF
            from file_factory.doc_builder import create_linkedin_report_pdf
            pdf_path = "LinkedIn_Optimization_Report.pdf"
            if create_linkedin_report_pdf(data, pdf_path):
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="📄 Download Professional PDF Report",
                        data=f,
                        file_name="LinkedIn_Optimization_Report.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
        
        with col_d2:
            import json
            st.download_button(
                label="💾 Download Raw JSON Data",
                data=json.dumps(data, indent=2),
                file_name="LinkedIn_Data.json",
                mime="application/json",
                use_container_width=True
            )

    st.divider()
    
    # --- Feature 1: Metadata SEO Pack ---
    st.subheader("🕵️ Invisible Keyword Injection (Metadata SEO)")
    st.info("Generate keyword-heavy 'Project' entries to hack the LinkedIn algorithm.")
    
    if st.button("Generate Metadata SEO Pack"):
        if li_role and li_stack:
            with st.spinner("Injecting Keywords..."):
                seo_content = engine.generate_keyword_injection(li_role, li_stack)
                st.markdown(seo_content)
        else:
            st.error("Please provide Target Role and Tech Stack above.")

    st.divider()
    
    # --- Feature 2: Visual Assets Factory ---
    st.subheader("🎨 Visual Assets Factory (Premium)")
    st.info("Generate high-converting visuals: Impact Cards, Tech Badges, Carousels, and Professional Banner Templates.")
    
    # Banner Template Section
    st.markdown("### 🎨 LinkedIn Banner Templates")
    st.caption("Choose from 5 professional templates with attractive hooks and color combinations")
    
    col_template1, col_template2 = st.columns([2, 1])
    
    with col_template1:
        # Template selector
        template_options = {
            'lead_generation': '🟡 Lead Generation (Yellow/Black)',
            'professional_authority': '🔵 Professional Authority (Navy/Gold)',
            'tech_innovator': '🔷 Tech Innovator (Cyan/Dark Gray)',
            'executive_premium': '⚫ Executive Premium (Black/White/Gold)',
            'creative_bold': '🟣 Creative Bold (Purple/Orange)',
            'modern_gradient': '🌊 Modern Gradient (Blue/Cyan)',
            'success_green': '🟢 Success Green (Forest Green/Gold)',
            'elegant_rose': '🌹 Elegant Rose (White/Rose Red)'
        }
        
        selected_template = st.selectbox(
            "Select Banner Template",
            options=list(template_options.keys()),
            format_func=lambda x: template_options[x],
            key="banner_template_select"
        )
        
        # Show template preview info
        from core_engine.visual_factory import VisualFactory
        vf_temp = VisualFactory()
        template_info = vf_temp.BANNER_TEMPLATES[selected_template]
        
        st.info(f"**Default Hook:** {template_info['hook']}")
        st.caption(f"**Default Tagline:** {template_info['tagline']}")
    
    with col_template2:
        # Manual Profile Photo Upload
        vf_profile_photo = st.file_uploader(
            "Profile Photo", 
            type=["jpg", "png", "jpeg"], 
            key="vf_profile_photo", 
            help="Upload your profile photo for banner"
        )
    
    # Customization inputs
    col_custom1, col_custom2 = st.columns(2)
    
    with col_custom1:
        custom_hook = st.text_input(
            "Custom Hook (Optional)",
            placeholder="Leave empty to use template default",
            key="custom_hook_input",
            help="Override the default hook text"
        )
        
        custom_tagline = st.text_input(
            "Custom Tagline (Optional)",
            placeholder="Leave empty to use template default",
            key="custom_tagline_input",
            help="Override the default tagline"
        )
    
    with col_custom2:
        portfolio_url_input = st.text_input(
            "Portfolio/LinkedIn URL",
            value="https://linkedin.com/in/yourname",
            key="portfolio_url_input",
            help="URL for QR code"
        )
        
        company_name_input = st.text_input(
            "Company/Brand Name (Optional)",
            placeholder="e.g., SAVERA Automation",
            key="company_name_input"
        )
    
    # Generate buttons
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("🎨 Generate Banner Only", type="primary"):
            if li_resume_text and li_role:
                with st.spinner(f"Generating {template_info['name']} Banner..."):
                    from core_engine.visual_factory import VisualFactory
                    vf = VisualFactory()
                    
                    # Save profile photo temporarily if uploaded
                    photo_path = None
                    if vf_profile_photo:
                        import tempfile
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                            tmp_file.write(vf_profile_photo.getvalue())
                            photo_path = tmp_file.name
                    
                    # Generate banner with template
                    banner_path = vf.generate_banner_with_template(
                        template_key=selected_template,
                        custom_hook=custom_hook if custom_hook else None,
                        custom_tagline=custom_tagline if custom_tagline else None,
                        profile_photo_path=photo_path,
                        portfolio_url=portfolio_url_input,
                        company_name=company_name_input if company_name_input else None,
                        output_path=f"linkedin_banner_{selected_template}.png"
                    )
                    
                    st.success(f"✅ {template_info['name']} Banner Generated!")
                    st.image(banner_path, caption=f"{template_info['name']} Banner", use_container_width=True)
                    
                    with open(banner_path, "rb") as file:
                        st.download_button(
                            "📥 Download Banner",
                            file,
                            f"LinkedIn_Banner_{selected_template}.png",
                            "image/png",
                            use_container_width=True
                        )
            else:
                st.error("Please upload a Resume and define your Target Role in Step 1 & 2 above.")
    
    with col_btn2:
        if st.button("🎨 Generate Full Visual Kit"):
            if li_resume_text and li_role:
                with st.spinner("Extracting Data & Designing Assets..."):
                    # 1. Extract Data
                    vis_data = engine.extract_visual_content(li_resume_text, li_role)
                    
                    if vis_data:
                        from core_engine.visual_factory import VisualFactory
                        vf = VisualFactory()
                        
                        # 2. Generate Assets
                        col_v1, col_v2 = st.columns(2)
                        col_v3, col_v4 = st.columns(2)
                        
                        # Impact Card
                        with col_v1:
                            st.markdown("**1. Impact Card**")
                            card_path = vf.generate_impact_card(vis_data.get('problem', 'Legacy System'), vis_data.get('solution', 'Microservices'))
                            st.image(card_path, caption="Before/After Impact")
                            with open(card_path, "rb") as file:
                                st.download_button("Download Card", file, "Impact_Card.png", "image/png")

                        # Tech Badge
                        with col_v2:
                            st.markdown("**2. Tech Stack Badge**")
                            badge_path = vf.generate_tech_badge(vis_data.get('skills', 'Java, AWS'))
                            st.image(badge_path, caption="Core Stack")
                            with open(badge_path, "rb") as file:
                                st.download_button("Download Badge", file, "Tech_Badge.png", "image/png")

                        # 5-Slide Carousel
                        with col_v3:
                            st.markdown("**3. 5-Slide Case Study Deck**")
                            pdf_path = vf.generate_carousel_slides(
                                vis_data.get('title', 'Project Case Study'), 
                                vis_data.get('results', []),
                                problem=vis_data.get('problem', 'Challenge'),
                                solution=vis_data.get('solution', 'Solution'),
                                tech_stack=vis_data.get('skills', 'Tech Stack')
                            )
                            st.success("PDF Generated!")
                            with open(pdf_path, "rb") as file:
                                st.download_button("Download Carousel (PDF)", file, "Case_Study_Carousel.pdf", "application/pdf")

                        # Template Banner
                        with col_v4:
                            st.markdown("**4. Template Banner**")
                            
                            # Save profile photo temporarily if uploaded
                            photo_path = None
                            if vf_profile_photo:
                                import tempfile
                                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                                    tmp_file.write(vf_profile_photo.getvalue())
                                    photo_path = tmp_file.name
                            
                            banner_path = vf.generate_banner_with_template(
                                template_key=selected_template,
                                custom_hook=custom_hook if custom_hook else None,
                                custom_tagline=custom_tagline if custom_tagline else None,
                                profile_photo_path=photo_path,
                                portfolio_url=portfolio_url_input,
                                company_name=company_name_input if company_name_input else None
                            )
                            st.image(banner_path, caption="Template Banner")
                            with open(banner_path, "rb") as file:
                                st.download_button("Download Banner", file, "LinkedIn_Banner_Template.png", "image/png")

                    else:
                        st.error("Could not extract visual data from resume.")
            else:
                st.error("Please upload a Resume and define your Target Role in Step 1 & 2 above.")

    st.divider()
    st.subheader("🤖 Algorithmic Dominance (Tech-First Features)")
    st.info("Use Data Science & AI to beat the LinkedIn Algorithm.")
    
    algo_tab1, algo_tab2, algo_tab3, algo_tab4 = st.tabs(["👁️ Recruiter Simulator", "✍️ Recommendation Ghostwriter", "📢 Thought Leader Content", "⚔️ Competitor Gap Analysis"])
    
    # 1. Recruiter Simulator
    with algo_tab1:
        st.markdown("#### Recruiter Eye-Tracking Audit (Gemini Vision)")
        st.write("Upload a screenshot of your LinkedIn Profile (Desktop/Mobile). AI will simulate a recruiter's 6-second scan.")
        profile_screenshot = st.file_uploader("Upload Profile Screenshot", type=["png", "jpg", "jpeg"])
        
        if st.button("Run Recruiter Simulation"):
            if profile_screenshot and li_role:
                with st.spinner("Simulating Recruiter Scan..."):
                    # Read image bytes
                    img_bytes = profile_screenshot.getvalue()
                    audit_report = engine.simulate_recruiter_review(img_bytes, li_role)
                    st.markdown(audit_report)
            else:
                st.error("Please upload a screenshot and ensure Target Role is set above.")

    # 2. Recommendation Ghostwriter
    with algo_tab2:
        st.markdown("#### Social Proof Generator")
        st.write("Generate pre-written recommendations to send to your boss/peers.")
        key_achievement = st.text_input("Key Achievement to Highlight", placeholder="e.g., Scaled backend to 10k TPS, Led team of 5")
        
        if st.button("Draft Recommendations"):
            if li_role and key_achievement:
                with st.spinner("Drafting Recommendations..."):
                    recs = engine.generate_recommendations(li_role, key_achievement)
                    st.markdown(recs)
            else:
                st.error("Please provide Target Role and Key Achievement.")

    # 3. Thought Leader Content
    with algo_tab3:
        st.markdown("#### Activity Feed Content Pack")
        st.write("Generate high-value comments and posts to look active.")
        content_project = st.text_input("Project Name for Content", placeholder="e.g., Payment Gateway Migration")
        content_stack = st.text_input("Tech Stack used", placeholder="e.g., Redis, Go, gRPC")
        
        if st.button("Generate Content Calendar"):
            if content_project and content_stack:
                with st.spinner("Generating Content..."):
                    calendar = engine.generate_content_calendar(content_project, content_stack)
                    st.markdown(calendar)
            else:
                st.error("Please provide Project Name and Tech Stack.")

    # 4. Competitor Gap Analysis
    with algo_tab4:
        st.markdown("#### Benchmarking vs. Gold Standard")
        st.write("Compare your profile against a 'Gold Standard' competitor (or Job Description).")
        competitor_text = st.text_area("Paste Competitor Profile Text / Ideal JD", height=200)
        
        if st.button("Analyze Gap"):
            if li_resume and competitor_text and li_role:
                with st.spinner("Running Gap Analysis..."):
                    gap_report = engine.analyze_competitor_gap(li_resume, competitor_text, li_role)
                    st.markdown(gap_report)
            else:
                st.error("Please ensure you have uploaded your resume (above), set a Target Role, and pasted Competitor Text.")


# --- Tab 3: GitHub Architect ---
with tab3:
    st.header("GitHub Architect")
    col1, col2 = st.columns(2)
    with col1:
        project_desc = st.text_area("Describe the Project", placeholder="E.g. A To-Do list app...")
    with col2:
        tech_stack = st.text_input("Tech Stack (Optional)", placeholder="React, Firebase, etc.")
    
    if st.button("Architect Project"):
        if project_desc:
            with st.spinner("Designing Architecture..."):
                # Returns a dict now
                arch_output = engine.architect_project(project_desc, tech_stack)
                st.session_state['arch_output'] = arch_output
                
                st.subheader("1. README Preview")
                st.markdown(arch_output['readme'], unsafe_allow_html=True)
                
                st.subheader("2. Architecture Diagram")
                st.markdown(arch_output['mermaid'])
                
                st.subheader("3. Folder Structure")
                st.code(arch_output['structure'])
        else:
            st.error("Please describe the project.")

    if 'arch_output' in st.session_state:
        if st.button("Bundle & Zip Repo"):
            data = st.session_state['arch_output']
            # Pass all 3 parts
            zip_path = create_project_bundle("New_Project", data['readme'], data['mermaid'], data['structure'], ".")
            if zip_path:
                with open(zip_path, "rb") as file:
                    st.download_button(
                        label="Download Project ZIP",
                        data=file,
                        file_name="Project_Bundle.zip",
                        mime="application/zip"
                    )


# --- Tab 7: ATS Scanner ---
with tab7:
    render_ats_scanner(engine)







