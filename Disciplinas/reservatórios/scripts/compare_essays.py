import PyPDF2
import re

# Extract Rocélio's essay
pdf_path = r'c:\Users\PCGAME\Desktop\reservatórios\histo\referências de meus colegas\historiadeengres (1).pdf'
pdf = PyPDF2.PdfReader(pdf_path)

print("=" * 80)
print("ROCÉLIO'S ESSAY - COMPLETE STRUCTURE AND REFERENCES")
print("=" * 80)

# Extract all text
full_text = ""
for i in range(len(pdf.pages)):
    full_text += pdf.pages[i].extract_text()

# Find and print References section
ref_match = re.search(r'(?:REFERÊNCIAS|BIBLIOGRAPHY|References)(.*)', full_text, re.IGNORECASE | re.DOTALL)
if ref_match:
    references_text = ref_match.group(1)
    print("\n=== REFERENCES IN ROCÉLIO'S ESSAY ===\n")
    # Print first 4000 chars of references
    print(references_text[:4000])
    print("\n[...references continue...]")
else:
    print("No references section found")

# Extract chapter/section headings (major sections)
heading_pattern = r'^(\d+\.?\s+[A-Z][A-Za-zçãõéú\s\-:]+?)(?:\n|\r)'
sections = re.findall(heading_pattern, full_text, re.MULTILINE)

print("\n=== MAIN SECTIONS/CHAPTERS IN ROCÉLIO'S ESSAY ===\n")
for i, section in enumerate(sections, 1):
    print(f"{i}. {section.strip()}")

print(f"\n=== DOCUMENT STATS ===")
print(f"Total pages: {len(pdf.pages)}")
print(f"Approximate word count: {len(full_text.split())}")
