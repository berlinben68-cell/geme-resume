import streamlit as st
from core_engine.strategy_logic import StrategyLogic

def render_global_mobility_tab():
    st.header("Global Mobility & Prestige Strategy")
    
    # Initialize Strategy Logic
    # In a real app, get API key from config/secrets
    api_key = st.secrets.get("GEMINI_API_KEY") 
    if not api_key:
        st.warning("Please set GEMINI_API_KEY in .streamlit/secrets.toml")
        return

    strategy_logic = StrategyLogic(api_key=api_key)

    tab1, tab2, tab3 = st.tabs(["🇦🇪 UAE Golden Visa", "🇦🇪 Bi-Lingual Executive", "🇺🇸/🇪🇺 Western Migration"])

    with tab1:
        st.subheader("Golden Visa Portfolio Aligner")
        st.markdown("Analyze your profile for UAE Golden Visa eligibility (AI, Blockchain, Data Science).")
        
        github_summary = st.text_area("Paste your GitHub Profile Summary / Bio / Pinned Repos", height=150)
        
        if st.button("Analyze for Golden Visa"):
            if github_summary:
                with st.spinner("Analyzing profile against Golden Visa requirements..."):
                    result = strategy_logic.golden_visa_gap_analysis(github_summary)
                    if result:
                        st.info(f"Status: **{result.get('status', 'Unknown')}**")
                        st.write(f"**Analysis:** {result.get('gap_analysis', '')}")
                        
                        st.subheader("Suggested Projects to Add")
                        for project in result.get('suggested_projects', []):
                            with st.expander(f"🚀 {project.get('title')}"):
                                st.write(f"**Description:** {project.get('description')}")
                                st.write(f"**Tech Stack:** {project.get('tech_stack')}")
            else:
                st.error("Please enter your GitHub summary.")

    with tab2:
        st.subheader("Bi-Lingual Executive Generator (Arabic/English)")
        st.markdown("Generate a professional 'Business Arabic' translation for your README.")
        
        english_readme = st.text_area("Paste your English README content", height=200)
        
        if st.button("Generate Arabic Translation"):
            if english_readme:
                with st.spinner("Translating to Professional Arabic..."):
                    arabic_content = strategy_logic.generate_arabic_readme(english_readme)
                    st.text_area("Arabic Translation", value=arabic_content, height=200)
                    
                    st.markdown("### Integration Code")
                    st.code(f"""
<details>
<summary>🇦🇪 Read in Arabic / العربية</summary>

{arabic_content}

</details>
                    """, language="html")
            else:
                st.error("Please paste your README content.")

    with tab3:
        st.subheader("US/EU Migration Scorer")
        st.markdown("Score your repo for Western/Silicon Valley compatibility.")
        
        repo_summary = st.text_area("Paste a summary of your target repository", height=150)
        
        if st.button("Score Repository"):
            if repo_summary:
                with st.spinner("Scoring repository..."):
                    result = strategy_logic.western_compatibility_score(repo_summary)
                    if result:
                        st.metric("Compatibility Score", f"{result.get('score')}/100")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.error("🚩 Red Flags")
                            for flag in result.get('red_flags', []):
                                st.write(f"- {flag}")
                        
                        with col2:
                            st.success("✅ Improvements")
                            for imp in result.get('improvements', []):
                                st.write(f"- {imp}")
            else:
                st.error("Please enter a repository summary.")
