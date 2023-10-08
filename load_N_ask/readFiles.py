from PyPDF2 import PdfReader
import csv

def read_pdf(userFile):
    """
        Reads a PDF file and extracts its text
        :param userFile: PDF file uploaded by user
        :return: text extracted from PDF file
    """
    text = ""
    for pdf_file in userFile:
        pdf_reader = PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def read_csv(userFile):
    """
        Reads a CSV file and extracts its text
        :param userFile: CSV file uploaded by user
        :return: text extracted from CSV file
    """
    text = ""
    with open(userFile.name, 'r') as f:
        text = f.read()
    return text

def read_txt(userFile):
    """
        Reads a TXT file and extracts its text
        :param userFile: TXT file uploaded by user
        :return: text extracted from TXT file
    """
    text = ""
    with open(userFile.name, 'r') as f:
        text = f.read()
    return text
