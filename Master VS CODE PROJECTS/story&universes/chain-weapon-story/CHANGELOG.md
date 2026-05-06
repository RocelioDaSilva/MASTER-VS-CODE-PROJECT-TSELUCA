# Changelog

## Unreleased

### Added
- CI: Added Black & Flake8 checks and test run to `.github/workflows/manuscript-ci.yml`.
- Developer requirements: `requirements-dev.txt` (Black, Flake8, PyTest) and `pyproject.toml` config.
- Tests: `tests/test_check_front_matter.py` — basic front-matter smoke test.
- Documentation: Updated `README.md` manuscript status to 105 chapters and added developer instructions to `CONTRIBUTING.md`.

### Updated
- `CONTRIBUTING.md`: Developer tools & local checks section (Black/Flake8/pytest instructions).
- `.github/PULL_REQUEST_TEMPLATE.md`: Added formatting/linting/testing checklist items.

### Notes
- Run `python -m pip install -r requirements-dev.txt` locally to run checks and tests.
- CI will run Black, Flake8, and PyTest on PRs.

