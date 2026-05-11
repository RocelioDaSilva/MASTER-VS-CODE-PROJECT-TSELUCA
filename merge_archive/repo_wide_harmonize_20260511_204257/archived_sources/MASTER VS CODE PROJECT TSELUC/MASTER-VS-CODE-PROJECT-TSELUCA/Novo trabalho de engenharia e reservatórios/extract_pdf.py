#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json

try:
    import PyPDF2
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'PyPDF2', '-q'])
    import PyPDF2

pdf_path = r'c:\Users\rocel\Downloads\12-Article Text-58-1-10-20210418 pt-PT (1).pdf'
text = ''

try:
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    
    with open('pdf_content.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    
    print("PDF extracted successfully to pdf_content.txt")
    print(f"Total length: {len(text)} characters")
    
except Exception as e:
    print(f"Erro: {e}", file=sys.stderr)
    sys.exit(1)
