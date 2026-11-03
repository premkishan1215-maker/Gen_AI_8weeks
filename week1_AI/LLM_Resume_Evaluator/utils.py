from pypdf import PdfReader
from docx import Document


def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)

    resume_text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            resume_text += page_text + "\n"

    if not resume_text.strip():
        raise ValueError("No text found in PDF.")

    return resume_text


def extract_text_from_docx(docx_file):
    document = Document(docx_file)

    resume_text = ""

    for paragraph in document.paragraphs:
        resume_text += paragraph.text + "\n"

    if not resume_text.strip():
        raise ValueError("No text found in Word document.")

    return resume_text


def extract_text(file):
    file_name = file.name.lower()

    if file_name.endswith(".pdf"):
        return extract_text_from_pdf(file)

    elif file_name.endswith(".docx"):
        return extract_text_from_docx(file)

    else:
        raise ValueError("Unsupported file format. Upload PDF or DOCX.")