import streamlit as st
from pypdf import PdfReader
from docx import Document
import io

@st.cache_data
def extract_text_from_file(file_bytes, file_type):
    text = ""
    try:
        if file_type == "application/pdf":
            reader = PdfReader(io.BytesIO(file_bytes))
            for page in reader.pages:
                text += page.extract_text() + "\n"
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(io.BytesIO(file_bytes))
            for para in doc.paragraphs:
                text += para.text + "\n"
    except Exception as e:
        return f"Error reading file: {e}"
    return text
