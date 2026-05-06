import os
import sys

# List of PDFs to analyze
pdf_files = [
    "histo/referências de meus colegas/APOSTILA-CURSO-BASICO-Eng-RES-doc (1).pdf",
    "histo/referências de meus colegas/História da Engenharia de Reservatórios (1).pdf",
    "histo/referências de meus colegas/História_de_engenharia_de_reservatório (1).pdf",
    "histo/referências de meus colegas/historiadeengres (1).pdf",
    "histo/referências de meus colegas/TCC - MODELO ABNT ISPTEC - Projecto parte 11.pdf"
]

# Check if pdfplumber is available
try:
    import pdfplumber
except ImportError:
    print("pdfplumber not found. Attempting to install...")
    os.system("pip install pdfplumber")
    import pdfplumber

# Extract text from each PDF
base_path = os.path.dirname(os.path.abspath(__file__))

for pdf_file in pdf_files:
    full_path = os.path.join(base_path, pdf_file)
    print(f"\n{'='*80}")
    print(f"FILE: {os.path.basename(pdf_file)}")
    print(f"PATH: {full_path}")
    print(f"EXISTS: {os.path.exists(full_path)}")
    
    if os.path.exists(full_path):
        try:
            with pdfplumber.open(full_path) as pdf:
                print(f"PAGES: {len(pdf.pages)}")
                # Extract first 3 pages worth of text to get overview
                text_preview = ""
                for i, page in enumerate(pdf.pages[:3]):
                    text = page.extract_text()
                    if text:
                        text_preview += f"\n--- PAGE {i+1} ---\n{text[:500]}"
                print(f"\nFIRST 3 PAGES PREVIEW:\n{text_preview[:2000]}")
        except Exception as e:
            print(f"ERROR extracting: {e}")
    else:
        print("FILE NOT FOUND")
    print(f"{'='*80}")
