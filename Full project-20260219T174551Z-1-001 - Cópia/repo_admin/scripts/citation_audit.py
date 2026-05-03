#!/usr/bin/env python3
import re
from pathlib import Path

tex_path = Path('manuscript_unified/science_manuscript/manuscript/SOL.tex')
bib_path = Path('manuscript_unified/science_manuscript/manuscript/referencias.bib')

if not tex_path.exists():
    print(f"ERROR: TeX file not found: {tex_path}")
    raise SystemExit(1)
if not bib_path.exists():
    print(f"ERROR: Bib file not found: {bib_path}")
    raise SystemExit(1)

tex = tex_path.read_text(encoding='utf-8')
bib = bib_path.read_text(encoding='utf-8')

# extract citation keys from TeX (handles multiple keys inside braces)
cite_matches = re.findall(r"\\cite[a-zA-Z]*\*?{([^}]*)}", tex)
cited = set()
for m in cite_matches:
    parts = [p.strip() for p in m.split(',') if p.strip()]
    for p in parts:
        cited.add(p)

# extract bib keys from .bib
bib_matches = re.findall(r"@[^\{]+\{([^,]+),", bib)
bibkeys = set([k.strip() for k in bib_matches if k.strip()])

missing = sorted(cited - bibkeys)
unused = sorted(bibkeys - cited)

out_lines = []
out_lines.append(f"Citation audit for TeX: {tex_path}")
out_lines.append(f"Bib file: {bib_path}")
out_lines.append("")
out_lines.append(f"Unique cited keys in TeX: {len(cited)}")
out_lines.append(f"Total BibTeX entries: {len(bibkeys)}")
out_lines.append("")

out_lines.append(f"Missing keys (cited in TeX but NOT in .bib): {len(missing)}")
for k in missing:
    out_lines.append(f" - {k}")
out_lines.append("")

out_lines.append(f"Unused keys (in .bib but not cited): {len(unused)}")
for k in unused:
    out_lines.append(f" - {k}")

# write report
report_path = Path('repo_admin/reports/citation_audit.txt')
report_path.parent.mkdir(parents=True, exist_ok=True)
report_path.write_text('\n'.join(out_lines), encoding='utf-8')

print('\n'.join(out_lines))
print(f"\nReport written to: {report_path}")
