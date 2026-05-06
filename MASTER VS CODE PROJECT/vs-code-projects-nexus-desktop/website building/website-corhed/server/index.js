const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const dotenv = require('dotenv');
const nodemailer = require('nodemailer');
const axios = require('axios');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const { body, validationResult } = require('express-validator');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3001;

app.use(helmet());
app.use(cors({ origin: process.env.CORS_ORIGIN || '*' }));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const DATA_DIR = path.join(__dirname, '..', 'data');
if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });

const CONTACTS_FILE = path.join(DATA_DIR, 'contacts.json');
const NEWS_FILE = path.join(DATA_DIR, 'newsletter.json');

function ensureFile(fp) {
  if (!fs.existsSync(fp)) fs.writeFileSync(fp, '[]', 'utf8');
}

ensureFile(CONTACTS_FILE);
ensureFile(NEWS_FILE);

function appendJson(fp, obj) {
  const raw = fs.readFileSync(fp, 'utf8') || '[]';
  let arr = [];
  try { arr = JSON.parse(raw); } catch (e) { arr = []; }
  arr.push(obj);
  fs.writeFileSync(fp, JSON.stringify(arr, null, 2), 'utf8');
}

// Optional mailer setup
let transporter = null;
if (process.env.SMTP_HOST && process.env.SMTP_USER) {
  transporter = nodemailer.createTransport({
    host: process.env.SMTP_HOST,
    port: parseInt(process.env.SMTP_PORT || '587', 10),
    secure: process.env.SMTP_SECURE === 'true',
    auth: {
      user: process.env.SMTP_USER,
      pass: process.env.SMTP_PASS
    }
  });
}

const useSqlite = (process.env.USE_DB || 'sqlite') === 'sqlite';
let db = null;
if (useSqlite) {
  db = require('./db');
}

const contactLimiter = rateLimit({
  windowMs: parseInt(process.env.RATE_WINDOW_MS || '60000', 10),
  max: parseInt(process.env.RATE_MAX || '10', 10),
  standardHeaders: true,
  legacyHeaders: false,
});

app.get('/api/health', (req, res) => res.json({ ok: true }));

app.post('/api/contact', contactLimiter, [
  body('name').trim().isLength({ min: 2 }).escape(),
  body('email').trim().isEmail().normalizeEmail(),
  body('message').trim().isLength({ min: 3 }).escape(),
  body('company').optional().trim().escape(),
  body('service').optional().trim().escape()
], async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) return res.status(400).json({ errors: errors.array() });

  // If reCAPTCHA is configured, require and verify token
  if (process.env.RECAPTCHA_SECRET) {
    const token = req.body?.recaptchaToken || req.headers['x-recaptcha-token'];
    if (!token) return res.status(400).json({ error: 'recaptcha token required' });
    try {
      const verify = await axios.post('https://www.google.com/recaptcha/api/siteverify', null, {
        params: { secret: process.env.RECAPTCHA_SECRET, response: token }
      });
      if (!verify.data || !verify.data.success) return res.status(400).json({ error: 'recaptcha verification failed' });
    } catch (err) {
      console.error('Recaptcha verify error', err?.message || err);
      return res.status(500).json({ error: 'recaptcha verification error' });
    }
  }

  const { name, email, company, service, message } = req.body || {};
  const entry = {
    name, email, company: company || '', service: service || '', message,
    createdAt: new Date().toISOString()
  };

  try {
    if (useSqlite && db) {
      const result = await db.insertContact(entry);
      entry.id = result.id;
    } else {
      entry.id = Date.now();
      appendJson(CONTACTS_FILE, entry);
    }

    if (transporter) {
      const mailOptions = {
        from: process.env.EMAIL_FROM || `Website <no-reply@${req.hostname}>`,
        to: process.env.CONTACT_TO || process.env.EMAIL_TO || 'admin@example.com',
        subject: `Novo contacto: ${name}`,
        text: `Name: ${name}\nEmail: ${email}\nCompany: ${company || ''}\nService: ${service || ''}\n\nMessage:\n${message}`
      };
      const info = await transporter.sendMail(mailOptions);
      const preview = nodemailer.getTestMessageUrl ? nodemailer.getTestMessageUrl(info) : null;
      if (preview) console.log('Contact email preview URL:', preview);
    }

    return res.json({ success: true, id: entry.id });
  } catch (err) {
    console.error('Contact error', err);
    return res.status(500).json({ error: 'Server error' });
  }
});

app.post('/api/newsletter', contactLimiter, [
  body('email').trim().isEmail().normalizeEmail()
], async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) return res.status(400).json({ errors: errors.array() });

  // If reCAPTCHA is configured, require and verify token
  if (process.env.RECAPTCHA_SECRET) {
    const token = req.body?.recaptchaToken || req.headers['x-recaptcha-token'];
    if (!token) return res.status(400).json({ error: 'recaptcha token required' });
    try {
      const verify = await axios.post('https://www.google.com/recaptcha/api/siteverify', null, {
        params: { secret: process.env.RECAPTCHA_SECRET, response: token }
      });
      if (!verify.data || !verify.data.success) return res.status(400).json({ error: 'recaptcha verification failed' });
    } catch (err) {
      console.error('Recaptcha verify error', err?.message || err);
      return res.status(500).json({ error: 'recaptcha verification error' });
    }
  }
  const { email } = req.body || {};
  const entry = { email, createdAt: new Date().toISOString() };
  try {
    if (useSqlite && db) {
      const result = await db.insertNewsletter(entry);
      entry.id = result.id;
    } else {
      entry.id = Date.now();
      appendJson(NEWS_FILE, entry);
    }
    return res.json({ success: true, id: entry.id });
  } catch (err) {
    console.error('Newsletter error', err);
    return res.status(500).json({ error: 'Server error' });
  }
});

app.post('/api/test-email', async (req, res) => {
  if (!transporter) return res.status(400).json({ error: 'SMTP not configured' });
  try {
    const info = await transporter.sendMail({
      from: process.env.EMAIL_FROM || `Website <no-reply@localhost>`,
      to: process.env.CONTACT_TO || process.env.EMAIL_TO || 'admin@example.com',
      subject: 'Test email from Corhed backend',
      text: 'This is a test email sent from the Corhed backend.'
    });
    const preview = nodemailer.getTestMessageUrl ? nodemailer.getTestMessageUrl(info) : null;
    if (preview) console.log('Test email preview URL:', preview);
    return res.json({ success: true, previewUrl: preview || null });
  } catch (err) {
    console.error('Test email error', err);
    return res.status(500).json({ error: 'Error sending test email' });
  }
});

function startServer() {
  app.listen(PORT, () => {
    console.log(`Corhed backend listening on http://localhost:${PORT}`);
    console.log(`Data directory: ${DATA_DIR}`);
    console.log(`Storage: ${useSqlite ? 'sqlite' : 'json files'}`);
  });
}

if (useSqlite && db && db.init) {
  db.init().then(() => startServer()).catch(err => {
    console.error('Failed to initialize database', err);
    process.exit(1);
  });
} else {
  startServer();
}
