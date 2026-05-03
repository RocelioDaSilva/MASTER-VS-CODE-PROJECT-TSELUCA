const fs = require('fs');
const path = require('path');
const child_process = require('child_process');
require('dotenv').config();

const OUT_RASTER = path.join(__dirname, 'outputs', 'headers_raster');
const OUT_SVG = path.join(__dirname, 'outputs', 'headers_svg');

function abort(msg){
  console.error(msg);
  process.exit(1);
}

let axios, PNG, ImageTracer;
try{
  axios = require('axios');
  PNG = require('pngjs').PNG;
}catch(e){
  abort('Missing dependencies. Run `npm install` in tools/image_pipeline/');
}

// Attempt to load ImageTracerJS: prefer installed package, else local lib file
try{
  ImageTracer = require('imagetracerjs');
}catch(e){
  try{
    ImageTracer = require('./lib/imagetracer_v1.2.6');
  }catch(e2){
    console.warn('ImageTracerJS not found. Either `npm install imagetracerjs` or download imagetracer_v1.2.6.js into tools/image_pipeline/lib/');
  }
}

function sleep(ms){ return new Promise(r => setTimeout(r, ms)); }

async function generateImageReplicate(prompt, baseName){
  const token = process.env.REPLICATE_API_TOKEN;
  const modelVersion = process.env.REPLICATE_MODEL_VERSION;
  if(!token || !modelVersion) abort('Set REPLICATE_API_TOKEN and REPLICATE_MODEL_VERSION in .env');

  const create = await axios.post('https://api.replicate.com/v1/predictions', {
    version: modelVersion,
    input: { prompt, width: 2400, height: 400 }
  },{
    headers: { Authorization: `Token ${token}`, 'Content-Type':'application/json' }
  });

  const id = create.data.id;
  console.log('Created prediction', id);
  let status = create.data.status;
  while(status !== 'succeeded' && status !== 'failed'){
    await sleep(2000);
    const poll = await axios.get(`https://api.replicate.com/v1/predictions/${id}`, { headers: { Authorization: `Token ${token}` } });
    status = poll.data.status;
    if(status === 'succeeded'){
      const output = Array.isArray(poll.data.output) ? poll.data.output[0] : poll.data.output;
      if(!output) throw new Error('No output URL returned');
      const img = await axios.get(output, { responseType: 'arraybuffer' });
      fs.mkdirSync(OUT_RASTER, { recursive: true });
      const pngPath = path.join(OUT_RASTER, baseName + '.png');
      fs.writeFileSync(pngPath, Buffer.from(img.data));
      console.log('Saved raster:', pngPath);
      return pngPath;
    }
  }
  throw new Error('Generation failed: ' + status);
}

function pngBufferToImageData(buffer){
  return new Promise((resolve, reject) => {
    new PNG().parse(buffer, function(err, data){
      if(err) return reject(err);
      const imagedata = { width: data.width, height: data.height, data: new Uint8Array(data.data) };
      resolve(imagedata);
    });
  });
}

async function traceToSVG(pngPath, svgPath){
  if(!ImageTracer) abort('ImageTracerJS not available. See tools/image_pipeline/lib/README.md');
  const buf = fs.readFileSync(pngPath);
  const imgd = await pngBufferToImageData(buf);
  const svg = ImageTracer.imagedataToSVG(imgd, 'posterized2');
  fs.mkdirSync(path.dirname(svgPath), { recursive: true });
  fs.writeFileSync(svgPath, svg, 'utf8');
  console.log('Wrote', svgPath);
}

async function optimizeSVG(svgPath){
  try{
    child_process.execSync(`npx svgo "${svgPath}" -o "${path.join(path.dirname(svgPath),'optimized', path.basename(svgPath))}"`, { stdio: 'inherit' });
    console.log('Optimized:', svgPath);
  }catch(e){
    console.warn('SVGO optimize failed or not installed. You can run `npm install` in tools/image_pipeline and try again.');
  }
}

async function main(){
  const promptsFile = path.join(__dirname, 'prompts.txt');
  const prompts = fs.existsSync(promptsFile) ? fs.readFileSync(promptsFile,'utf8').split(/\r?\n/).filter(Boolean) : [
    'Wide fantasy banner, stylized silhouettes, vector-friendly shapes, dusk teal and burnt orange, chain-weapon motif, negative space composition, no text'
  ];

  for(let i=0;i<prompts.length;i++){
    const p = prompts[i];
    const base = String(i+1).padStart(2,'0');
    console.log('Generating', base);
    const png = await generateImageReplicate(p, base);
    const svgPath = path.join(OUT_SVG, base + '.svg');
    await traceToSVG(png, svgPath);
    await optimizeSVG(svgPath);
  }
  console.log('Done. Outputs at', OUT_SVG);
}

if(require.main === module){
  main().catch(err => { console.error(err); process.exit(1); });
}
