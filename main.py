import os
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
import pandas as pd
import camelot
import ollama
import time

REQUIRED_FIELDS = [
    "Temporal classes", "BibTeX key", "Item type", "Authors", "Affiliations", "Title", "Journal",
    "Publication year", "Dataset(s) used", "Task", "Evaluation metric", "Model description",
    "Model name", "Supervised ML", "Deep neural network", "Traditional feature based methods",
    "Neural Sequence Models", "TransformerBased Methods", "LLM methods", "Trained or fine-tuned",
    "Feature engineering", "URLs", "DOI", "Abstract"
]

def extract_text(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception:
        return ""

def ocr_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)
    return text

def extract_tables(pdf_path):
    try:
        tables = camelot.read_pdf(pdf_path, pages="all", flavor="stream")
        return [t.df.to_string() for t in tables]
    except Exception:
        return []

def ollama_extract_fields(text, tables, model_name="llama3"):
    prompt = f"""
You are an expert at extracting structured information from scientific papers.
Given the following text and tables from a scientific paper, extract the following fields as a JSON object with these keys:
{REQUIRED_FIELDS}

If a field is missing, leave it empty. If a field is a yes/no, answer 'yes' or 'no' and provide details if requested.
Text:
{text[:3000]}

Tables:
{tables[:1]}

Return only the JSON object.
"""
    response = ollama.chat(model=model_name, messages=[
        {"role": "user", "content": prompt}
    ])
    import json
    try:
        # Попытка найти JSON в ответе
        import re
        match = re.search(r'\{[\s\S]*\}', response['message']['content'])
        if match:
            data = json.loads(match.group(0))
        else:
            data = {k: "" for k in REQUIRED_FIELDS}
    except Exception:
        data = {k: "" for k in REQUIRED_FIELDS}
    return data

# Папка с PDF
pdf_folder = "."  # текущая папка
pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")]

results = []
for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_folder, pdf_file)
    print(f"Processing: {pdf_file}")
    text = extract_text(pdf_path)
    if not text.strip():
        text = ocr_pdf(pdf_path)
    tables = extract_tables(pdf_path)
    data = ollama_extract_fields(text, tables)
    data["PDF"] = pdf_file
    results.append(data)
    time.sleep(5)  # небольшая пауза между запросами

# Сохраняем результат
df = pd.DataFrame(results)
df.to_csv("extracted_papers_ollama.csv", index=False)
print("Done! Results saved to extracted_papers_ollama.csv")
