import os
import PyPDF2
import docx

def extract_text(filepath):
    """
    Extracts text from PDF or DOCX resume.
    """
    _, ext = os.path.splitext(filepath.lower())
    if ext == '.pdf':
        return extract_text_from_pdf(filepath)
    elif ext in ['.docx', '.doc']:
        return extract_text_from_docx(filepath)
    else:
        raise ValueError(f"Unsupported file format: {ext}")

def extract_text_from_pdf(filepath):
    text = ""
    with open(filepath, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def extract_text_from_docx(filepath):
    doc = docx.Document(filepath)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return "\n".join(text).strip()
