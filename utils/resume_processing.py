import PyPDF2

def process_resume(file_path):
    resume_text = ""
    with open(file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)  # Use PdfReader instead of PdfFileReader
        for page in pdf_reader.pages:
            resume_text += page.extract_text()
    return resume_text


def process_job_description(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    return text
