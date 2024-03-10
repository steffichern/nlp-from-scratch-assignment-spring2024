import fitz  # PyMuPDF
import requests

def download_pdf(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def save_text_to_file(text, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)

# URL of the PDF
pdf_url = 'https://www.cmu.edu/about/cmu_fact_sheet_02.pdf'
# Temporary PDF filename
pdf_filename = './history/cmu_fact_sheet.pdf'
# Destination text filename
text_filename = './history/cmu_fact_sheet.txt'


download_pdf(pdf_url, pdf_filename)
pdf_text = extract_text_from_pdf(pdf_filename)
save_text_to_file(pdf_text, text_filename)

print(f"Extracted text from '{pdf_filename}' to '{text_filename}'")
