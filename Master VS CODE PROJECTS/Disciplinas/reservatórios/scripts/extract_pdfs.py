#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract text from PDF files for analysis
"""

import os
from pathlib import Path
from PyPDF2 import PdfReader

colleague_dir = Path("c:/Users/PCGAME/Desktop/reservatórios/histo/referências de meus colegas")

# List of PDFs to extract (exclude the template model)
pdf_files_to_extract = [
    "APOSTILA-CURSO-BASICO-Eng-RES-doc (1).pdf",
    "historiadeengres (1).pdf",
    "História_de_engenharia_de_reservatório (1).pdf",
    "História da Engenharia de Reservatórios (1).pdf"
]

for pdf_name in pdf_files_to_extract:
    pdf_path = colleague_dir / pdf_name
    if not pdf_path.exists():
        print(f"\n[MISSING] {pdf_name}\n")
        continue
        
    print(f"\n{'='*80}")
    print(f"FILE: {pdf_name}")
    print(f"{'='*80}\n")
    
    try:
        reader = PdfReader(str(pdf_path))
        print(f"Total pages: {len(reader.pages)}\n")
        
        # Extract text from first 5 pages (or all if fewer)
        max_pages = min(5, len(reader.pages))
        for page_num in range(max_pages):
            page = reader.pages[page_num]
            text = page.extract_text()
            
            # Split text into lines and show first 30 lines
            lines = text.split('\n')[:30]
            print(f"--- PAGE {page_num + 1} ---")
            for line in lines:
                if line.strip():
                    print(line[:120])
            print()
            
    except Exception as e:
        print(f"ERROR extracting {pdf_name}: {e}\n")
