# Reports

Generated PDF reports from the repository data.

| File | Source | How to Rebuild |
|---|---|---|
| `anpg-local-content-full-data.pdf` | [tex/anpg-local-content-full-data.tex](../tex/anpg-local-content-full-data.tex) | Run `xelatex` on the `.tex` file (requires MiKTeX) |

To regenerate KPI values before building the PDF:

```bash
python scripts/preprocess-anpg-data.py
```
