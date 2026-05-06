import os
from pypdf import PdfReader

workspace_root = os.path.abspath(os.path.dirname(__file__))
refs_dir = os.path.join(workspace_root, 'referências para o estudo')
output_file = os.path.join(workspace_root, 'full info.md')

collected = []
for root_dir, dirs, files in os.walk(refs_dir):
    for f in sorted(files):
        if f.lower().endswith('.pdf'):
            path = os.path.join(root_dir, f)
            collected.append((f, path))

content_lines = []
if not collected:
    print(f"Nenhum PDF encontrado em: {refs_dir}")
else:
    for fname, path in collected:
        content_lines.append(f"## Arquivo: {fname}")
        content_lines.append("")
        try:
            reader = PdfReader(path)
            text_parts = []
            for page in reader.pages:
                try:
                    t = page.extract_text() or ""
                except Exception:
                    t = ""
                text_parts.append(t)
            text = "\n".join(text_parts).strip()
            if not text:
                content_lines.append("_(sem texto extraído)_")
            else:
                content_lines.append(text)
        except Exception as e:
            content_lines.append(f"_(Erro ao ler PDF: {e})_")
        content_lines.append("\n---\n")

with open(output_file, 'w', encoding='utf-8') as f:
    f.write("\n".join(content_lines))

print(f"Transcrição gravada em: {output_file}")
