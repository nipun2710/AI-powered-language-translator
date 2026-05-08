import pdfplumber
import docx


def extract_pdf_text(file):

    text = ""

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

    return text


def extract_docx_text(file):

    doc = docx.Document(file)

    text = ""

    for para in doc.paragraphs:

        text += para.text + "\n"

    return text