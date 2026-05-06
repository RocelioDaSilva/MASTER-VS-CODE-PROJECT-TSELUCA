# Merged Report — Corhed site
Date: 2026-04-18

**Summary**
- **Backend:** Express backend with `/api/contact`, `/api/newsletter`, `/api/test-email` — see [server/index.js](server/index.js). Storage: SQLite at `data/database.sqlite` (JSON fallback).
- **Email:** Ethereal test SMTP created; test email sent (preview URL returned by server logs).
- **Export:** Editable Word export created at [corhed/Corhed_Landing_FullText_Edit.docx](corhed/Corhed_Landing_FullText_Edit.docx) (generator: [scripts/generate_docx.py](scripts/generate_docx.py)).
- **Frontend:** `corhed/index.html` updated to POST forms to backend ([corhed/index.html](corhed/index.html)).

**Completed (high level)**
- **Fixes:** template asset paths and `server.ps1` doc root corrected.
- **Backend:** implemented validation, rate-limiting, helmet, SQLite support, Ethereal SMTP helper and test-email route.
- **Tests:** integration POST tests for contact/newsletter succeeded locally.
- **Repo:** changes committed locally.

**Outstanding / Incomplete items**
- **Add reCAPTCHA token to front-end forms:** NOT IMPLEMENTED. The backend expects a `recaptchaToken` (POST body `recaptchaToken` or header `x-recaptcha-token`) when `RECAPTCHA_SECRET` is set. The front-end currently does not request or send a token. Target file: [corhed/index.html](corhed/index.html).
  - Implementation notes: use Google reCAPTCHA v3 (recommended) or v2. For v3, include the site script and call `grecaptcha.execute(siteKey, {action:'contact'})` to get a token, then include `recaptchaToken` in the JSON body sent by `handleSubmit` and `handleNewsletter`.

- **Tune rate-limiting / CAPTCHA UX:** NOT STARTED. Adjust `RATE_WINDOW_MS` and `RATE_MAX` in `server/.env` (see [/.env.example](.env.example)). Consider adding a client-side captcha widget if human verification is needed for UX.

- **Push commits to remote:** NOT PUSHED. A remote `origin` exists: `https://github.com/RocelioDaSilva/website-building.git`. Run `git push origin main` (or current branch) to publish commits.

**Checks performed now**
- Scanned front-end: `corhed/index.html` — form handlers `handleSubmit` and `handleNewsletter` do NOT include any reCAPTCHA token handling.
- Searched repo for `recaptcha` — only server-side verification and README notes found (no front-end integration).
- Git remotes: origin -> `https://github.com/RocelioDaSilva/website-building.git` (push/fetch configured).

**Recommended next steps (pick one or more)**
1. Add client-side reCAPTCHA to `corhed/index.html` and include `recaptchaToken` in form POSTs (I can patch this and test).  
2. Tune `RATE_WINDOW_MS` / `RATE_MAX` in `server/.env` and retest high-volume scenarios.  
3. Push commits to GitHub: `git push origin main` (I can push if you want).  

If you want, I can implement (1) now: patch `corhed/index.html` to load Google reCAPTCHA (site-key placeholder), obtain token, and include it in both `handleSubmit` and `handleNewsletter`, then run a test. Reply which option to do next.
