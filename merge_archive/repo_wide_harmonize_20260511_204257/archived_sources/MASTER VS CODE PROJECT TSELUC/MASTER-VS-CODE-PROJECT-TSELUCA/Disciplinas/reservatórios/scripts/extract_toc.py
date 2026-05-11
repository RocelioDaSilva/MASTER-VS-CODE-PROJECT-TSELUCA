import pdfplumber

pdf_path = 'histo/referências de meus colegas/historiadeengres (1).pdf'

with pdfplumber.open(pdf_path) as pdf:
    all_text = ""
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            all_text += text + "\n"
    
    # Find and extract table of contents
    lines = all_text.split('\n')
    
    print("ROCÉLIO DA SILVA - FULL TABLE OF CONTENTS:\n")
    in_toc = False
    toc_lines = []
    for i, line in enumerate(lines):
        # Look for table of contents marker
        if 'Sumário' in line or 'SUMÁRIO' in line or 'ÍNDICE' in line:
            in_toc = True
            continue
        
        if in_toc:
            # Stop when we hit the first chapter/introduction
            if line.strip().startswith('1 ') or 'Introdução' in line:
                break
            if line.strip():  # Only non-empty lines
                toc_lines.append(line)
    
    if toc_lines:
        for line in toc_lines[:50]:
            print(line)
    else:
        # Alternative: just grab first 50 lines after title pages
        print("Content from beginning:")
        for line in lines[30:80]:
            print(line)
