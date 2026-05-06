import pdfplumber
import os

pdfs = {
    'Paulo (12pp)': 'histo/referências de meus colegas/História da Engenharia de Reservatórios (1).pdf',
    'Rocélio (35pp)': 'histo/referências de meus colegas/historiadeengres (1).pdf',
}

for name, pdf_path in pdfs.items():
    if os.path.exists(pdf_path):
        print(f"\n{'='*100}")
        print(f"ANALYZING: {name}")
        print(f"{'='*100}\n")
        
        with pdfplumber.open(pdf_path) as pdf:
            # Get pages 3-6 which usually have table of contents
            all_text = ""
            for i in range(min(6, len(pdf.pages))):
                text = pdf.pages[i].extract_text()
                if text:
                    all_text += text + "\n[PAGE BREAK]\n"
            
            print("STRUCTURE & CONTENTS (First 6 pages):\n")
            print(all_text)
            print("\n" + "="*100)
