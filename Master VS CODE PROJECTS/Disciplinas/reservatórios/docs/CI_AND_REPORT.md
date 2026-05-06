CI and report notes

- CI: a GitHub Actions workflow was added at `.github/workflows/python-tests.yml`.
  It runs `python -m unittest discover -v tests` on pushes and pull requests to `main`.

- GUI: the original script `projecto_de_codigo/projecto de código/projeto_z_factor.py` now prefers
  the refactored GUI in `src/main.py` and will fall back to the legacy GUI if needed.

- Report template: `docs/report_template.tex` contains a minimal LaTeX template. Generate CSV from the GUI and paste the table in the `Results` section or load via `pgfplotstable`.

- To run tests locally:

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -v tests
```
