import PyPDF2
import re

# Extract bibliography from Rocélio's PDF
pdf_path = r'c:\Users\PCGAME\Desktop\reservatórios\histo\referências de meus colegas\historiadeengres (1).pdf'

try:
    pdf = PyPDF2.PdfReader(pdf_path)
    total_pages = len(pdf.pages)
    print(f"Total pages: {total_pages}")
    
    # Extract from last 10 pages (bibliography usually near end)
    all_text = ''
    for page_num in range(max(0, total_pages - 15), total_pages):
        page = pdf.pages[page_num]
        try:
            all_text += f"\n--- PAGE {page_num + 1} ---\n"
            all_text += page.extract_text() + '\n'
        except:
            pass
    
    # Save full end section
    with open(r'c:\Users\PCGAME\Desktop\reservatórios\rocelio_end_pages.txt', 'w', encoding='utf-8') as f:
        f.write(all_text)
    
    # Find bibliography section
    bib_start = max(
        all_text.find('REFERÊNCIAS'),
        all_text.find('Referências'),
        all_text.find('BIBLIOGRAPHY'),
        all_text.find('Bibliography')
    )
    
    if bib_start != -1:
        bibliography = all_text[bib_start:]
        
        # Save bibliography only
        with open(r'c:\Users\PCGAME\Desktop\reservatórios\rocelio_bibliography.txt', 'w', encoding='utf-8') as f:
            f.write(bibliography)
        
        # Extract individual references
        # Look for numbered references (1. Author... or [1] Author...)
        lines = bibliography.split('\n')
        
        print("\n=== ROCÉLIO'S BIBLIOGRAPHY ENTRIES ===\n")
        
        entries = []
        current_entry = ''
        
        for line in lines[:150]:  # First 150 lines of bibliography section
            line = line.strip()
            if line:
                # Check if this is a new entry (starts with number or letter)
                if re.match(r'^[\[\(]?\d+[\]\)]?\s+[A-Z]', line) or re.match(r'^[A-Z]{1,3}\.\s', line):
                    if current_entry:
                        entries.append(current_entry)
                    current_entry = line
                elif current_entry:
                    current_entry += ' ' + line
        
        if current_entry:
            entries.append(current_entry)
        
        for i, entry in enumerate(entries, 1):
            if len(entry) > 10:
                print(f"{i}. {entry[:200]}")
                print()
        
        print(f"\nTotal entries found: {len(entries)}")
        
    else:
        print("Bibliography section not found")
        print("\nShowing end of document:")
        print(all_text[-2000:])

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
