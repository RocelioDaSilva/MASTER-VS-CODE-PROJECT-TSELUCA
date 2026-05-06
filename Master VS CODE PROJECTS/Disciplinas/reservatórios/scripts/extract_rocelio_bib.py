import PyPDF2
import re
import json

# Extract bibliography from Rocélio's PDF
pdf_path = r'c:\Users\PCGAME\Desktop\reservatórios\histo\referências de meus colegas\historiadeengres (1).pdf'

try:
    pdf = PyPDF2.PdfReader(pdf_path)
    
    full_text = ''
    for page_num in range(len(pdf.pages)):
        page = pdf.pages[page_num]
        try:
            full_text += f"\n--- PAGE {page_num + 1} ---\n"
            full_text += page.extract_text() + '\n'
        except:
            pass
    
    # Find bibliography section
    bib_indicators = ['REFERÊNCIAS', 'Referências', 'BIBLIOGRAPHY', 'Bibliography', 'REFERENCES', 'References']
    bib_start = -1
    
    for indicator in bib_indicators:
        pos = full_text.find(indicator)
        if pos != -1:
            bib_start = pos
            break
    
    if bib_start != -1:
        bibliography_section = full_text[bib_start:]
        
        # Save raw bibliography for inspection
        with open(r'c:\Users\PCGAME\Desktop\reservatórios\rocelio_bibliography_raw.txt', 'w', encoding='utf-8') as f:
            f.write(bibliography_section[:5000])
        
        print("=== ROCÉLIO'S BIBLIOGRAPHY (RAW EXTRACTION) ===\n")
        print(bibliography_section[:3000])
        print("\n...[Full text saved to rocelio_bibliography_raw.txt]")
    else:
        print("Bibliography section not found")
        print("\nSearching entire text for references pattern...")
        # Try to find any reference-like patterns
        refs = re.findall(r'[A-Z][a-z]+[,\s].*?(?:\(\d{4}\))\.*', full_text[:8000])
        for ref in refs[:20]:
            print(f"- {ref}")

except Exception as e:
    print(f"Error: {e}")
