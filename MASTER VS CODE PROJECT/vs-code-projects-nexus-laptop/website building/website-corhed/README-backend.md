# Backend for Corhed site

This simple Express backend provides two endpoints:

- `POST /api/contact` — accepts `{ name, email, company, service, message }` and stores it in `data/contacts.json`. If SMTP is configured it will also send an email.
- `POST /api/newsletter` — accepts `{ email }` and stores it in `data/newsletter.json`.

Notes:
- The backend supports two storage modes: JSON files (default) and SQLite. Set `USE_DB=sqlite` in your `.env` (or leave unset) to use SQLite. The database file will be created at `data/database.sqlite`.
- Input is validated and sanitized using `express-validator`.
- Rate limiting is enabled for contact/newsletter endpoints. Configure `RATE_WINDOW_MS` and `RATE_MAX` in `.env` to change limits.
- There is a test route `POST /api/test-email` to verify SMTP configuration (returns an error if SMTP is not configured).

reCAPTCHA:
- To enable server-side reCAPTCHA verification set `RECAPTCHA_SECRET` in `server/.env` (the secret key from Google reCAPTCHA). When set the backend requires a `recaptchaToken` (POST body or `x-recaptcha-token` header) for `POST /api/contact` and `POST /api/newsletter` and validates it with Google's API.
- Frontend integration: add the Google reCAPTCHA site script and include the generated token in the form submission as `recaptchaToken`.

How to run:

```powershell
cd server
npm install
npm start
```

By default the backend listens on port `3001`. Configure SMTP by creating `server/.env` (copy from `/.env.example`) and setting `SMTP_HOST`, `SMTP_USER`, `SMTP_PASS`, etc. To enable SQLite storage set `USE_DB=sqlite` in the `.env` file (the default). The server will create `data/database.sqlite` automatically.
