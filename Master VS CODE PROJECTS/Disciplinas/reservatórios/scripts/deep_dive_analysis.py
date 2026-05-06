import pdfplumber
import os

# Focus on deep comparison of the two history student papers
pdfs = {
    'Paulo Isaac Abel (12pp)': 'histo/referências de meus colegas/História da Engenharia de Reservatórios (1).pdf',
    'Rocélio Da Silva (35pp)': 'histo/referências de meus colegas/historiadeengres (1).pdf',
}

for name, pdf_path in pdfs.items():
    if os.path.exists(pdf_path):
        print(f"\n{'='*100}")
        print(f"DEEP DIVE: {name}")
        print(f"{'='*100}\n")
        
        with pdfplumber.open(pdf_path) as pdf:
            all_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    all_text += text + "\n"
            
            # Extract key sections
            lines = all_text.split('\n')
            
            # Find table of contents
            toc_start = -1
            toc_end = -1
            for i, line in enumerate(lines):
                if 'ÍNDICE' in line.upper() or 'TABLE OF CONTENTS' in line:
                    toc_start = i
                if toc_start > 0 and (line.strip() == '' or line.startswith('1.') or line.startswith('CAPITULO') or 'INTRODUÇÃO' in line.upper()):
                    if i > toc_start + 2:
                        toc_end = i
                        break
            
            if toc_start >= 0:
                print("TABLE OF CONTENTS:")
                print('\n'.join(lines[toc_start:min(toc_end if toc_end > 0 else toc_start+30, len(lines))]))
            
            # Extract methodology
            print("\n\nMETHODOLOGY SECTION:")
            for i, line in enumerate(lines):
                if 'METODOLOG' in line.upper() or 'METHODOLOGY' in line.upper():
                    print('\n'.join(lines[i:min(i+15, len(lines))]))
                    break
            
            # Check for specific technical topics
            print("\n\nTECHNICAL TOPICS COVERED:")
            keywords = [
                'DARCY', 'balanço de materiais', 'simulação', 'EOR', 'recuperação',
                'porosidade', 'permeabilidade', 'pressão', 'IoT', 'inteligência artificial',
                'machine learning', 'transient', 'interpretação'
            ]
            found_topics = set()
            for line in lines:
                for keyword in keywords:
                    if keyword.lower() in line.lower():
                        found_topics.add(keyword)
            
            print(f"Found topics: {', '.join(sorted(found_topics))}")
            
            # Extract conclusion
            print("\n\nCONCLUSION/KEY FINDINGS:")
            for i, line in enumerate(lines):
                if 'CONCLUS' in line.upper() or 'REMARK' in line.upper():
                    conclusion_text = '\n'.join(lines[i:min(i+20, len(lines))])
                    print(conclusion_text[:600])
                    break
