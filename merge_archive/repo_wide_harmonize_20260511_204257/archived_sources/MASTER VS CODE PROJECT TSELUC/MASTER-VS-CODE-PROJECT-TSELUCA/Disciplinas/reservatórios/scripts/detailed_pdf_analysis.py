import pdfplumber
import os

# Detailed analysis of both history papers and the APOSTILA
pdfs_to_analyze = {
    'Paulo Isaac Abel (12pp)': 'histo/referências de meus colegas/História da Engenharia de Reservatórios (1).pdf',
    'Rocélio Da Silva (35pp)': 'histo/referências de meus colegas/historiadeengres (1).pdf',
    'APOSTILA-CURSO (62pp)': 'histo/referências de meus colegas/APOSTILA-CURSO-BASICO-Eng-RES-doc (1).pdf'
}

for title, pdf_path in pdfs_to_analyze.items():
    if os.path.exists(pdf_path):
        print(f"\n{'='*90}")
        print(f"FILE: {title}")
        print(f"{'='*90}")
        
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
            
            # Extract key information
            print("\n--- MAIN SECTIONS/TOPICS ---")
            lines = full_text.split('\n')
            
            # Look for section headers (typically all caps or numbered)
            section_count = 0
            for line in lines[:150]:  # First 150 lines
                line = line.strip()
                if line and (line.isupper() or line.startswith(tuple('0123456789'))):
                    if len(line) > 3 and not line.startswith('INSTITUTO') and not line.startswith('DEPARTAMENTO'):
                        print(f"  {line[:100]}")
                        section_count += 1
                        if section_count > 20:
                            break
            
            # Get abstract/summary
            print("\n--- ABSTRACT/SUMMARY (first 600 chars) ---")
            if 'ABSTRACT' in full_text or 'Resumo' in full_text:
                start = full_text.find('resumo') if 'resumo' in full_text.lower() else full_text.find('ABSTRACT')
                if start > 0:
                    print(full_text[start:start+600])
            else:
                print(full_text[500:1100])
