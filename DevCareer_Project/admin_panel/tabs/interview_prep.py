import streamlit as st
from core_engine.strategy_logic import StrategyLogic
from fpdf import FPDF
import base64

def create_pdf(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Interview Cheat Sheet", ln=1, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Architecture Defense", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=content.get('architecture_defense', ''))
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Time Complexity", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=content.get('time_complexity', ''))
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Potential Improvements", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=content.get('potential_improvements', ''))
    
    return pdf.output(dest='S').encode('latin-1')

def render_interview_prep_tab():
    st.header("🇮🇳 Interview Prep & Cheat Sheet")
    st.markdown("Generate a 'Cheat Sheet' to defend your ghostwritten projects in brutal technical interviews. ")
    
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        st.warning("Please set GEMINI_API_KEY in .streamlit/secrets.toml")
        return

    strategy_logic = StrategyLogic(api_key=api_key)
    
    project_details = st.text_area("Paste Project Details / Code Snippet / Readme", height=200)
    
    if st.button("Generate Cheat Sheet"):
        if project_details:
            with st.spinner("Generating interview defense strategy..."):
                result = strategy_logic.generate_interview_cheat_sheet(project_details)
                
                if result:
                    st.subheader("Architecture Defense")
                    st.write(result.get('architecture_defense'))
                    
                    st.subheader("Time Complexity")
                    st.write(result.get('time_complexity'))
                    
                    st.subheader("Potential Improvements")
                    st.write(result.get('potential_improvements'))
                    
                    # PDF Generation
                    pdf_bytes = create_pdf(result)
                    b64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
                    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="interview_cheat_sheet.pdf">Download Cheat Sheet PDF</a>'
                    st.markdown(href, unsafe_allow_html=True)
        else:
            st.error("Please provide project details.")
