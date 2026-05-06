const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs');

const DB_PATH = path.join(__dirname, '..', 'data', 'database.sqlite');
const DATA_DIR = path.dirname(DB_PATH);
if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });

const db = new sqlite3.Database(DB_PATH);

function init() {
  return new Promise((resolve, reject) => {
    db.serialize(() => {
      db.run(`CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        company TEXT,
        service TEXT,
        message TEXT,
        createdAt TEXT NOT NULL
      )`);

      db.run(`CREATE TABLE IF NOT EXISTS newsletter (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        createdAt TEXT NOT NULL
      )`, (err) => {
        if (err) return reject(err);
        resolve();
      });
    });
  });
}

function insertContact(entry) {
  return new Promise((resolve, reject) => {
    const stmt = db.prepare('INSERT INTO contacts (name,email,company,service,message,createdAt) VALUES (?,?,?,?,?,?)');
    stmt.run(entry.name, entry.email, entry.company || '', entry.service || '', entry.message, entry.createdAt, function (err) {
      if (err) return reject(err);
      resolve({ id: this.lastID });
    });
    stmt.finalize();
  });
}

function insertNewsletter(entry) {
  return new Promise((resolve, reject) => {
    const stmt = db.prepare('INSERT INTO newsletter (email,createdAt) VALUES (?,?)');
    stmt.run(entry.email, entry.createdAt, function (err) {
      if (err) return reject(err);
      resolve({ id: this.lastID });
    });
    stmt.finalize();
  });
}

module.exports = { init, insertContact, insertNewsletter, DB_PATH };
