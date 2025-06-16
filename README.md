# Scientific PDF Explicit Info Extractor

This project is a simple Python tool for extracting explicit, structured information from scientific papers in PDF format. It is designed to work locally and privately, using a local Large Language Model (LLM) via [Ollama](https://ollama.com/).

## Features
- **Batch processing:** Processes all PDF files in the current folder.
- **Text and table extraction:** Uses OCR and table extraction for robust parsing.
- **LLM-powered extraction:** Uses a local LLM (e.g., Llama 3 via Ollama) to extract explicit metadata and research details from the paper's content.
- **CSV export:** Saves all extracted information in a single CSV file for further analysis.

## Extracted Fields
The script extracts the following fields (if present in the PDF):
- Temporal classes (e.g., decades, centuries, literary epochs)
- BibTeX key
- Item type (e.g., journal article, conference paper)
- Authors
- Affiliations
- Title
- Journal
- Publication year
- Dataset(s) used
- Task (e.g., text classification, segmentation, retrieval)
- Evaluation metric
- Model description
- Model name
- Supervised ML (yes/no)
- Deep neural network (yes/no)
- Traditional feature based methods (yes/no, and which features)
- Neural Sequence Models (yes/no, and which)
- TransformerBased Methods (yes/no, and which)
- LLM methods (yes/no, and which)
- Trained or fine-tuned (yes/no)
- Feature engineering (yes/no and how)
- URLs
- DOI
- Abstract

## How it works
1. **Extracts text and tables** from each PDF using `pdfplumber`, `pytesseract`, and `camelot`.
2. **Sends the extracted content** to a local LLM via Ollama with a prompt to extract the required fields.
3. **Saves the results** in `extracted_papers_ollama.csv`.

## Requirements
- Python 3.8+
- [Ollama](https://ollama.com/) with a suitable model (e.g., llama3)
- Python packages: `pdfplumber`, `pytesseract`, `pandas`, `pdf2image`, `camelot-py[cv]`, `ollama`

## Usage
1. Place your PDFs in the project folder.
2. Run the script:
   ```
   python main_ollama.py
   ```
3. Find the results in `extracted_papers_ollama.csv`.

## Notes
- All processing is local; your PDFs and extracted data never leave your computer.
- The quality of extraction depends on the LLM and the quality of the PDF.

---
