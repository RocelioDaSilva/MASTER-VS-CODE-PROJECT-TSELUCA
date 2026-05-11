const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

function safeExec(cmd){
  try{ return execSync(cmd, { encoding: 'utf8' }).trim(); }
  catch(e){ return null; }
}

console.log('Node:', process.version);
const npmv = safeExec('npm -v');
console.log('npm:', npmv || 'not found');

console.log('\nChecking external tools:');
console.log('inkscape:', safeExec('inkscape --version') || 'not found');
console.log('magick:', safeExec('magick -version') || safeExec('convert -version') || 'not found');

const outDir = path.join(__dirname, 'outputs', 'headers_svg');
if(fs.existsSync(outDir)){
  const files = fs.readdirSync(outDir).filter(f => !f.includes('_preview'));
  console.log('\nFound SVGs in outputs/headers_svg/:', files.length);
  files.slice(0,10).forEach(f => {
    const p = path.join(outDir, f);
    const head = fs.readFileSync(p, 'utf8').split(/\r?\n/).slice(0,2).join(' ');
    console.log(' -', f, head.substring(0,200));
  });
} else {
  console.log('\nNo SVG outputs found yet at outputs/headers_svg/');
}

console.log('\nTest complete. To proceed: run `npm install` in this folder and add API keys to .env.');
