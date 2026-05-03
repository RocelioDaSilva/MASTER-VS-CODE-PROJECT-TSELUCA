# Dashboard refactor

This folder contains a modular Streamlit dashboard split into pages and reusable components.

Run locally:

```bash
cd "Full project/Coding parts/geesp-angola"
streamlit run dashboard/app_runner.py
```

Structure:
- `dashboard/pages/` — page modules with `render()` entrypoint
- `dashboard/components/` — reusable components (map renderer, metric cards)
- `dashboard/utils/` — small helpers and caching wrapper

Testing:

```bash
python -m pytest -q
```
