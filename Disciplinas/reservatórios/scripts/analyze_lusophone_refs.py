import PyPDF2
import re

# Extract full text from Rocélio's PDF
pdf_path = r'c:\Users\PCGAME\Desktop\reservatórios\histo\referências de meus colegas\historiadeengres (1).pdf'

try:
    pdf = PyPDF2.PdfReader(pdf_path)
    
    full_text = ''
    for page_num in range(len(pdf.pages)):
        page = pdf.pages[page_num]
        try:
            full_text += page.extract_text() + '\n'
        except:
            pass
    
    # Search for key phrases that might indicate citations with authors
    # Look for patterns like "segundo...", "conforme", "obra de", "por", followed by author names
    
    print("=== SEARCHING FOR PORTUGUESE LANGUAGE REFERENCES ===\n")
    
    # Portuguese phrases that indicate citations
    pt_citation_phrases = [
        r'(?:segundo|conforme|obra\s+de|por|baseado\s+em|segundo\s+a\s+obra\s+de)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        r'(?:emLinguaportuguesa).*?(?:de|por)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
    ]
    
    found_pt_refs = []
    for phrase in pt_citation_phrases:
        matches = re.findall(phrase, full_text, re.IGNORECASE)
        found_pt_refs.extend(matches)
    
    if found_pt_refs:
        print("Portuguese-language references mentioned:")
        for ref in set(found_pt_refs):
            if len(ref) > 2:
                print(f"  - {ref}")
    
    # Search for specific keywords indicating Portuguese or Angolan sources
    keywords = ['português', 'português', 'Angolan', 'Lusófono', 'lusófono', 'ISPTEC', 'Luanda']
    
    print("\n=== CONTEXT WITH PORTUGUESE/LUSOPHONE KEYWORDS ===\n")
    
    for keyword in keywords:
        if keyword.lower() in full_text.lower():
            # Find sentences containing the keyword
            pattern = f'[^.!?]*{keyword}[^.!?]*[.!?]'
            sentences = re.findall(pattern, full_text, re.IGNORECASE)
            if sentences:
                print(f"\nContext with '{keyword}':")
                for sent in sentences[:2]:
                    clean_sent = sent.replace('\n', ' ').strip()
                    if len(clean_sent) > 20:
                        print(f"  \"{clean_sent[:150]}...\"")
    
    # Look for the specific mention of Ramos works (which are Portuguese)
    print("\n\n=== RAMOS WORKS (PORTUGUESE-LANGUAGE) ===\n")
    ramos_pattern = r'Ramos.*?(?:2016|2020|Métodos|Fundamentos|Engenharia)[^.]*\.'
    ramos_refs = re.findall(ramos_pattern, full_text, re.IGNORECASE)
    for ref in ramos_refs:
        clean = ref.replace('\n', ' ').strip()
        print(f"  - {clean[:180]}")
    
    # Check if the document mentions any unique technical areas
    print("\n\n=== SPECIALIZED TECHNICAL AREAS MENTIONED ===\n")
    tech_areas = ['CCS', 'hidrocarbone', 'pré-sal', 'ultra-profund', 'shale', 'AI', 'IoT', 'digital twin', 'EOR']
    
    for area in tech_areas:
        if area.lower() in full_text.lower():
            count = len(re.findall(area, full_text, re.IGNORECASE))
            print(f"  {area}: mentioned {count} times")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
