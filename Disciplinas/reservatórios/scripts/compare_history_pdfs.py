import pdfplumber
import os

# Extract full text from the key comparison PDFs
pdfs = {
    'Paulo Isaac Abel': 'histo/referências de meus colegas/História da Engenharia de Reservatórios (1).pdf',
    'Rocélio Da Silva': 'histo/referências de meus colegas/historiadeengres (1).pdf'
}

for author, pdf_path in pdfs.items():
    if os.path.exists(pdf_path):
        print("\n" + "="*80)
        print(f"AUTHOR: {author}")
        print("="*80 + "\n")
        with pdfplumber.open(pdf_path) as pdf:
            print(f"Total Pages: {len(pdf.pages)}\n")
            # Get full text from all pages to analyze structure
            full_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
            
            # Print first 3000 chars to see structure
            print("FULL CONTENT PREVIEW:")
            print(full_text[:3000])
