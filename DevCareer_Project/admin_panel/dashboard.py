
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
from file_factory.doc_builder import create_resume_docx, generate_html_preview, create_resume_docx_from_html
from file_factory.repo_bundler import create_project_bundle
from admin_panel.tabs.resume_builder import render_resume_builder
from admin_panel.tabs.naukri_optimizer import render_naukri_optimizer
from admin_panel.tabs.ats_scanner import render_ats_scanner
from admin_panel.tabs.job_search import render_job_search
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
    except FileNotFoundError:
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
    "🇮🇳 Naukri Optimizer", 
    "📊 ATS Scanner",
    "💼 Job Search"
])

# --- Tab 1: Resume Builder ---
with tab1:
    render_resume_builder(engine)
# --- Tab 2: Cover Letter ---
with tab2:
    render_cover_letter_builder(engine)

# --- Tab 5: Naukri Optimizer ---
with tab5:
    render_naukri_optimizer(engine)

# --- Tab 4: LinkedIn Optimizer ---
with tab4:
    st.header("LinkedIn Optimizer")
    col1, col2 = st.columns(2)
    
    with col1:
        li_resume_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"], key="li_resume_uploader")
        li_resume_text = ""
        
        if li_resume_file is not None:
            # Use cached extraction
            li_resume_text = extract_text_from_file(li_resume_file.getvalue(), li_resume_file.type)
            
            if li_resume_text.startswith("Error"):
                st.error(li_resume_text)
            else:
                st.success("Resume Loaded from File!")
                
                # Auto-Extract Role & Stack if not already set or if new file
                if 'extracted_file' not in st.session_state or st.session_state.get('extracted_file') != li_resume_file.name:
                    with st.spinner("Auto-detecting Role & Tech Stack..."):
                        extracted = engine.extract_role_and_stack(li_resume_text)
                        # Update the widget keys directly
                        st.session_state['li_role'] = extracted.get('role', '')
                        st.session_state['li_stack'] = extracted.get('stack', '')
                        st.session_state['li_resume_input'] = li_resume_text # Update text area
                        st.session_state['extracted_file'] = li_resume_file.name
                        st.rerun() # Rerun to update inputs
    
        li_resume = st.text_area("Resume Content", height=300, key="li_resume_input")
    
    with col2:
        li_role = st.text_input("Target Role", placeholder="e.g. Senior Java Developer", key="li_role")
        li_stack = st.text_input("Tech Stack Focus", placeholder="e.g. Spring Boot, AWS, Kafka", key="li_stack")
        st.info("This tool generates a 'Recruiter SEO' kit to help you rank in top search results.")
    
    if st.button("Generate Optimization Kit"):
        if li_resume and li_role:
            with st.spinner("Analyzing Algorithm & Generating Kit..."):
                li_content = engine.optimize_linkedin(li_resume, li_role, li_stack)
                st.markdown(li_content)
                
                st.download_button(
                    label="Download Optimization Kit (TXT)",
                    data=li_content,
                    file_name="LinkedIn_Optimization_Kit.txt",
                    mime="text/plain"
                )
        else:
            st.error("Please upload a Resume and provide a Target Role.")

    st.divider()

    # --- Feature: JSON Profile Kit (New) ---
    st.subheader("🚀 Advanced Profile Kit (JSON)")
    st.info("Generate a structured, SEO-optimized profile kit including headlines, about section, and skill strategy.")
    
    li_region = st.text_input("Target Region", placeholder="e.g. Dubai, Bangalore, London", key="li_region")
    
    if st.button("Generate Profile Kit (JSON)"):
        if li_resume and li_role and li_region:
            with st.spinner("Generating Profile Kit..."):
                kit_data = engine.generate_linkedin_profile_kit(li_role, li_region, li_resume)
                
                if kit_data:
                    st.success("Profile Kit Generated!")
                    
                    # Display Headlines
                    st.markdown("### 1. Headlines")
                    for h in kit_data.get('headlines', []):
                        st.write(f"- {h}")
                        
                    # Display About Section
                    st.markdown("### 2. About Section")
                    about = kit_data.get('about_section', {})
                    st.markdown(f"**Hook:** {about.get('hook', '')}")
                    st.markdown(f"**Body:** {about.get('body', '')}")
                    st.markdown(f"**Stack:** {about.get('tech_stack_list', '')}")
                    st.markdown(f"**CTA:** {about.get('call_to_action', '')}")
                    
                    # Display Tips
                    st.markdown("### 3. Optimization Tips")
                    for tip in kit_data.get('experience_optimization_tips', []):
                        st.write(f"- {tip}")
                        
                    # Display Skills
                    st.markdown("### 4. SEO Skills")
                    st.write(", ".join(kit_data.get('skills_seo', [])))
                    
                    # Display Featured Strategy
                    st.markdown("### 5. Featured Strategy")
                    st.write(kit_data.get('featured_section_strategy', ''))
                    
                    # Download JSON
                    import json
                    st.download_button(
                        label="Download Profile Kit (JSON)",
                        data=json.dumps(kit_data, indent=2),
                        file_name="LinkedIn_Profile_Kit.json",
                        mime="application/json"
                    )
                else:
                    st.error("Failed to generate Profile Kit. Please try again.")
        else:
            st.error("Please provide Target Role, Region, and Upload Resume.")

    st.divider()

    # --- Feature: SEO Audit (New) ---
    st.subheader("🔍 LinkedIn SEO Audit & Ranking")
    st.info("Analyze your profile against the 'LinkedIn Recruiter' search algorithm.")
    
    if st.button("Run SEO Audit"):
        if li_resume and li_role and li_region:
            with st.spinner("Auditing Profile SEO..."):
                seo_data = engine.generate_linkedin_seo_audit(li_role, li_region, li_resume)
                
                if seo_data:
                    st.success("SEO Audit Complete!")
                    
                    # 1. SEO Audit
                    audit = seo_data.get('seo_audit', {})
                    st.markdown("### 1. Keyword Gap Analysis")
                    st.error(f"**Missing Keywords:** {audit.get('missing_keywords', 'None detected')}")
                    st.success(f"**Primary Keyword Cluster:** {audit.get('primary_keyword_cluster', '')}")
                    
                    # 2. Headline Strategy
                    st.markdown("### 2. Headline Optimization")
                    headlines = seo_data.get('headline_optimization', {})
                    st.info(f"**Strategy:** {headlines.get('strategy', '')}")
                    for opt in headlines.get('options', []):
                        st.write(f"- {opt}")
                        
                    # 3. About Section
                    st.markdown("### 3. About Section Rewrite")
                    st.write(seo_data.get('about_section_seo', ''))
                    
                    # 4. Experience Rewrites
                    st.markdown("### 4. Experience Optimization")
                    for exp in seo_data.get('experience_rewrites', []):
                        st.markdown(f"**Role:** {exp.get('original_role', 'Current Role')}")
                        st.markdown(f"**Instruction:** {exp.get('instruction', '')}")
                        for bullet in exp.get('optimized_bullet_points', []):
                            st.write(f"- {bullet}")
                            
                    # 5. Skills Ordering
                    st.markdown("### 5. Skill Section Ordering")
                    skills = seo_data.get('skills_section_ordering', {})
                    st.markdown(f"**📌 Pin Top 3:** {skills.get('top_3_pinned', '')}")
                    st.markdown(f"**Industry:** {skills.get('industry_knowledge', '')}")
                    st.markdown(f"**Tools:** {skills.get('tools_technologies', '')}")
                    
                    # 6. Hidden Factors
                    st.markdown("### 6. Hidden Ranking Factors")
                    for factor in seo_data.get('hidden_ranking_factors', []):
                        st.write(f"- {factor}")
                        
                    # Download JSON
                    import json
                    st.download_button(
                        label="Download SEO Audit (JSON)",
                        data=json.dumps(seo_data, indent=2),
                        file_name="LinkedIn_SEO_Audit.json",
                        mime="application/json"
                    )
                else:
                    st.error("Failed to generate SEO Audit. Please try again.")
        else:
            st.error("Please provide Target Role, Region, and Upload Resume.")

    st.divider()

    # --- Feature: Visual Audit (New) ---
    st.subheader("🎨 Visual Brand Audit")
    st.info("Audit your Profile Photo and Banner for trust, authority, and industry fit.")
    
    col_vis1, col_vis2 = st.columns(2)
    with col_vis1:
        vis_industry = st.selectbox("Industry Vibe", ["Corporate / Banking", "Modern Tech Startup", "Consulting / Agency", "Academic / Research", "Creative / Design"])
    with col_vis2:
        vis_input_method = st.radio("Input Method", ["Upload Image", "Describe Visuals"])
        
    vis_context = ""
    if vis_input_method == "Upload Image":
        vis_file = st.file_uploader("Upload Profile/Banner Screenshot", type=["png", "jpg", "jpeg"], key="vis_uploader")
        if vis_file:
            st.image(vis_file, caption="Visual Input", width=300)
            vis_context = "Image provided. Analyze the visual elements visible in the uploaded image."
            # In a real scenario, we'd pass the image bytes to a vision model. 
            # For now, we'll ask the user to describe it if the model isn't vision-enabled, 
            # OR we assume the backend handles the image (which our mock/Gemini 1.5 Pro can).
            # Let's assume we pass a description for now to be safe with the text-only prompt, 
            # or we can try to pass the image if the backend supports it.
            # The prompt expects "Visual Input" text. Let's ask the user to describe it for better results with text-only models,
            # or if we are using Gemini Vision, we could pass the image.
            # Given the prompt is text-based ("Visual Input: {visual_input}"), let's stick to text description for now 
            # or auto-convert image to description if we had a captioning tool.
            # To keep it simple and robust:
            vis_context = "User uploaded an image. (Note: For best results, please also describe the image below if the AI cannot see it)."
    
    vis_desc = st.text_area("Describe your Profile Photo & Banner (or add context to upload)", placeholder="e.g. Me in a suit, white background. Banner is a city skyline.")
    
    if vis_desc:
        vis_context = vis_desc

    if st.button("Run Visual Audit"):
        if li_role and vis_context:
            with st.spinner("Auditing Visual Brand..."):
                vis_data = engine.generate_linkedin_visual_audit(li_role, vis_industry, vis_context)
                
                if vis_data:
                    st.success("Visual Audit Complete!")
                    
                    # 1. Profile Photo
                    photo = vis_data.get('profile_photo_audit', {})
                    st.markdown(f"### 👤 Profile Photo (Score: {photo.get('score', '?')}/10)")
                    st.write(f"**Impression:** {photo.get('impression_analysis', '')}")
                    st.info(f"**Tip:** {photo.get('improvement_tip', '')}")
                    
                    # 2. Banner Image
                    banner = vis_data.get('banner_image_audit', {})
                    st.markdown(f"### 🖼️ Banner Image (Score: {banner.get('score', '?')}/10)")
                    st.write(f"**Relevance:** {banner.get('relevance_check', '')}")
                    st.success(f"**Suggestion:** {banner.get('suggestion', '')}")
                    
                    # 3. Consistency
                    st.markdown("### 🧠 Psychological Consistency")
                    st.write(vis_data.get('psychological_consistency', ''))
                    
                    # Download JSON
                    import json
                    st.download_button(
                        label="Download Visual Audit (JSON)",
                        data=json.dumps(vis_data, indent=2),
                        file_name="LinkedIn_Visual_Audit.json",
                        mime="application/json"
                    )
                else:
                    st.error("Failed to generate Visual Audit. Please try again.")
        else:
            st.error("Please provide Target Role and Visual Description.")

    st.divider()

    # --- Feature: Master Optimization Kit (New) ---
    st.subheader("👑 Master Optimization Kit (All-in-One)")
    st.info("Generate the ultimate LinkedIn transformation: SEO + Text + Visuals in one click.")
    
    with st.expander("🛠️ Service Provider Workflow (How to use)"):
        st.markdown("""
        **Follow these steps to gather data for your client:**
        1. **Get the URL:** Ask the client for their LinkedIn URL and paste it in the `Current LinkedIn URL` slot below.
        2. **Get the Text:** Open their profile, copy all text (About, Experience, Skills), and paste it into the `Resume Content` text area at the top of this page.
        3. **Get the Images:** Take a screenshot of their Profile Header (Photo + Banner) and upload it or describe it in the `Visual Brand Audit` section.
        
        **Important:** Please ensure all inputs (Role, Region, Resume, Visuals, URL) are provided above before generating.
        """)
    
    li_url = st.text_input("Current LinkedIn URL", placeholder="e.g. https://www.linkedin.com/in/your-name")

    if st.button("Generate Master Kit"):
        if li_role and li_region and li_resume and vis_context and li_url:
            with st.spinner("Generating Master Optimization Kit..."):
                # Use the industry from Visual Audit section if selected, else default
                industry = vis_industry if 'vis_industry' in locals() else "Technology"
                
                master_data = engine.generate_linkedin_master_kit(li_role, li_region, industry, li_resume, vis_context, li_url)
                
                if master_data:
                    st.success("Master Kit Generated!")
                    
                    # 1. URL & Settings Audit
                    st.markdown("### 1. URL & Settings Audit")
                    url_audit = master_data.get('url_settings_audit', {})
                    url_opt = url_audit.get('url_optimization', {})
                    st.write(f"**Status:** {url_opt.get('status', '')}")
                    st.info(f"**Fix:** {url_opt.get('fix', '')}")
                    st.warning(f"**Visibility:** {url_audit.get('public_visibility', '')}")

                    # 2. SEO Strategy
                    st.markdown("### 2. SEO Strategy Audit")
                    seo = master_data.get('seo_strategy_audit', {})
                    st.write("**Keyword Gaps:**")
                    for gap in seo.get('keyword_gap_analysis', []):
                        st.write(f"- {gap}")
                    st.write("**Primary Cluster:**")
                    for cluster in seo.get('primary_keyword_cluster', []):
                        st.write(f"- {cluster}")
                        
                    # 3. Text Optimization
                    st.markdown("### 3. Text Optimization")
                    text_opt = master_data.get('text_optimization', {})
                    
                    st.write("**Headline Options:**")
                    for opt in text_opt.get('headline_options', []):
                        st.write(f"- {opt}")
                        
                    st.write("**About Section:**")
                    about = text_opt.get('about_section', {})
                    st.markdown(f"> {about.get('hook', '')}")
                    st.markdown(f"{about.get('body', '')}")
                    
                    st.write("**Experience Rewrite:**")
                    exp = text_opt.get('experience_rewrites', {})
                    st.markdown(f"*{exp.get('role', 'Role')}*")
                    for stmt in exp.get('impact_statements', []):
                        st.write(f"- {stmt}")
                        
                    # 4. Visual Audit
                    st.markdown("### 4. Visual Audit")
                    vis = master_data.get('visual_audit', {})
                    photo = vis.get('profile_photo_check', {})
                    banner = vis.get('banner_image_check', {})
                    
                    col_m1, col_m2 = st.columns(2)
                    with col_m1:
                        st.write("**Profile Photo:**")
                        st.write(f"Score: {photo.get('technical_score', '?')}/10")
                        st.info(f"Fix: {photo.get('fix', '')}")
                    with col_m2:
                        st.write("**Banner:**")
                        st.write(f"Relevance: {banner.get('relevance', '')}")
                        st.success(f"Rec: {banner.get('recommendation', '')}")
                    
                    # Download JSON
                    import json
                    st.download_button(
                        label="Download Master Kit (JSON)",
                        data=json.dumps(master_data, indent=2),
                        file_name="LinkedIn_Master_Kit.json",
                        mime="application/json"
                    )
                else:
                    st.error("Failed to generate Master Kit. Please try again.")
        else:
            missing = []
            if not li_role: missing.append("Target Role")
            if not li_region: missing.append("Target Region")
            if not li_resume: missing.append("Resume Content")
            if not vis_context: missing.append("Visual Context (Upload or Describe)")
            if not li_url: missing.append("LinkedIn URL")
            
            st.error(f"Please ensure all inputs are provided. Missing: {', '.join(missing)}")

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
    st.info("Generate high-converting visuals: Impact Cards, Tech Badges, Carousels, and Banners.")
    
    if st.button("Generate Visual Kit"):
        if li_resume and li_role:
            with st.spinner("Extracting Data & Designing Assets..."):
                # 1. Extract Data
                vis_data = engine.extract_visual_content(li_resume, li_role)
                
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

                    # Recruiter Conversion Banner
                    with col_v4:
                        st.markdown("**4. Recruiter Conversion Banner**")
                        # Use contact name or default
                        name = data.get('contact', {}).get('name', 'Your Name')
                        banner_path = vf.generate_linkedin_banner(name, li_role, "https://github.com")
                        st.image(banner_path, caption="Custom Banner with QR")
                        with open(banner_path, "rb") as file:
                            st.download_button("Download Banner", file, "LinkedIn_Banner.png", "image/png")

                else:
                    st.error("Could not extract visual data from resume.")
        else:
            st.error("Please upload a Resume first.")

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


# --- Tab 6: ATS Scanner ---
with tab6:
    render_ats_scanner(engine)

# --- Tab 7: Job Search ---
with tab7:
    render_job_search()
