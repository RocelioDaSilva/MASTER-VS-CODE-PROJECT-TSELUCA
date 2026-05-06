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
    
    # Look for Portuguese author names and citations
    # Pattern: Author.S. (YEAR)
    citations = re.findall(r'([A-Z][a-z]+(?:\s+(?:da|de|do|e)\s+)?[A-Z][a-z]+)\s*\((\d{4})\)', full_text)
    
    print("=== ALL CITATIONS FOUND IN ROCÉLIO'S DOCUMENT ===\n")
    
    unique_citations = {}
    for author, year in citations:
        key = f"{author}-{year}"
        if key not in unique_citations:
            unique_citations[key] = (author, year)
    
    print(f"Total unique author-year citations: {len(unique_citations)}\n")
    
    # Separate by language characteristics
    pt_authors = []
    en_authors = []
    other_authors = []
    
    for (author, year) in unique_citations.values():
        if any(word in author for word in ['da', 'de', 'do', 'Silva', 'Santos', 'Rosa', 'Ramos', 'Pinto', 'Oliveira']):
            pt_authors.append((author, year))
        else:
            en_authors.append((author, year))
    
    print("=== PORTUGUESE-LANGUAGE AUTHOR CITATIONS ===")
    for author, year in sorted(set(pt_authors)):
        print(f"- {author} ({year})")
    
    print(f"\n=== ENGLISH/INTERNATIONAL AUTHOR CITATIONS ===")
    for author, year in sorted(set(en_authors)):
        print(f"- {author} ({year})")
    
    # Look for ???? markers (missing citations in text)
    missing_count = len(re.findall(r'\(\?\?\?\?\)', full_text))
    print(f"\n\nINFORMATION: Document has {missing_count} citations with missing references (marked as ????)")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
