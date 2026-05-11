const nodemailer = require('nodemailer');
const fs = require('fs');
const path = require('path');

async function main() {
  const account = await nodemailer.createTestAccount();
  const smtp = account.smtp || {};
  const env = [];
  env.push(`SMTP_HOST=${smtp.host}`);
  env.push(`SMTP_PORT=${smtp.port}`);
  env.push(`SMTP_SECURE=${smtp.secure}`);
  env.push(`SMTP_USER=${account.user}`);
  env.push(`SMTP_PASS=${account.pass}`);
  env.push(`EMAIL_FROM=\"Corhed Test\" <${account.user}>`);
  env.push(`CONTACT_TO=${account.user}`);
  env.push(`USE_DB=sqlite`);

  const out = env.join('\n') + '\n';
  const envPath = path.join(__dirname, '.env');
  fs.writeFileSync(envPath, out, 'utf8');
  console.log('Wrote test SMTP .env to', envPath);
  console.log('Test SMTP user:', account.user);
  console.log('Run the server and call POST /api/test-email to send a test message.');
  console.log('You can view Ethereal messages at the preview URL logged by the server.');
}

main().catch(err => {
  console.error('Failed to create ethereal account', err);
  process.exit(1);
});
