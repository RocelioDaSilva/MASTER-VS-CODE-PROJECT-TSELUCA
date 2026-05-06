#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract text content from colleague documents for integration.
Supports: .docx, .tex (already readable), .pdf (basic text extraction)
"""

import os
from pathlib import Path
from docx import Document
import sys

colleague_dir = Path("c:/Users/PCGAME/Desktop/reservatórios/histo/referências de meus colegas")

# Extract from .docx files
docx_files = list(colleague_dir.glob("*.docx"))
print(f"Found {len(docx_files)} .docx files\n")

for docx_file in docx_files:
    print(f"\n{'='*80}")
    print(f"FILE: {docx_file.name}")
    print(f"{'='*80}\n")
    
    try:
        doc = Document(docx_file)
        
        # Extract all text
        all_text = []
        for para in doc.paragraphs:
            if para.text.strip():
                all_text.append(para.text)
        
        # Print first 100 lines or all if fewer
        text_to_print = all_text[:100]
        for i, line in enumerate(text_to_print, 1):
            print(f"{i:3d}: {line[:150]}")
        
        if len(all_text) > 100:
            print(f"\n... ({len(all_text) - 100} more paragraphs) ...")
            print(f"\nTotal paragraphs: {len(all_text)}")
            
    except Exception as e:
        print(f"ERROR extracting from {docx_file.name}: {e}")

# Also check .tex files
tex_files = list(colleague_dir.glob("*.tex"))
print(f"\n\nFound {len(tex_files)} .tex files")
for tex_file in tex_files:
    print(f"  - {tex_file.name}")

# Check PDF files
pdf_files = list(colleague_dir.glob("*.pdf"))
print(f"\nFound {len(pdf_files)} .pdf files")
for pdf_file in pdf_files:
    size_mb = pdf_file.stat().st_size / (1024*1024)
    print(f"  - {pdf_file.name} ({size_mb:.2f} MB)")
