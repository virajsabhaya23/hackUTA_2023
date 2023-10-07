from PyPDF2 import PdfReader
import csv

def read_pdf(userFile):
    """
        Reads a PDF file and extracts its text
        :param userFile: PDF file uploaded by user
        :return: text extracted from PDF file
    """
    pdf_reader = PdfReader(userFile)
    text = ""
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
    with open(userFile.name, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            text += row[0]
    return text