import streamlit as st
import re
import docx2txt
from io import BytesIO
from PyPDF2 import PdfReader

def init_session_state():
    """
        Initializes session state
    """
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []

def clear_submit():
    """
        Clears submit button
    """
    st.session_state["submit"] = False

# @st.experimental_memo()
# def parse_docx(file: BytesIO) -> str:
#     text = docx2txt.process(file)
#     text = re.sub(r'\n\s*\n', '\n', text)
#     return text

# @st.experimental_memo()
# def parse_text(file: BytesIO) -> str:
#     text = file.read().decode('utf-8')
#     text = re.sub(r'\n\s*\n', '\n\n', text)
#     return text

# @st.experimental_memo()
# def read_pdf(file: BytesIO) -> str:
#     """
#         Reads a PDF file and extracts its text
#         :param userFile: PDF file uploaded by user
#         :return: text extracted from PDF file
#     """
#     pdf_reader = PdfReader(file)
#     text = ""
#     for page in pdf_reader.pages:
#         text += page.extract_text()
#     return text