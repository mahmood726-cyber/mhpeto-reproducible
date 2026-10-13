const fs=require('fs'), path=require('path');
const {pathToFileURL}=require('url');
const {chromium}=require('playwright');
const corpus=JSON.parse(fs.readFileSync('corpus.json','utf8'));
const root=process.argv[2]||'<ALLMETA_ROOT>';
const output=process.argv[3]||'app.json';
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true});
 const page=await browser.newPage();const errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto(pathToFileURL(path.resolve(root,'mh-peto/index.html')).href);
 await page.waitForFunction(()=>typeof window.__almLoad==='function');
 // Capture the unchanged diagnostic function's return value during the actual page run.
 await page.evaluate(()=>{const f=AlmFragility.fragility;AlmFragility.fragility=function(...args){return window.__capturedFrag=f.apply(this,args)};});
 const out=fs.existsSync(output)?JSON.parse(fs.readFileSync(output,'utf8')):[];let count=out.length;
 const done=new Set(out.map(r=>r.id));
 for(const cfg of corpus)for(const measure of ['OR','RR','RD']){
  const id=cfg.id+'|'+measure;
  if(done.has(id))continue;
  const entry=await page.evaluate(({cfg,measure})=>{
   document.getElementById('measure').value=measure;
   window.__capturedFrag=null;window.__almLabbe=null;
   window.__almLoad(cfg.rows.map((r,i)=>({study:'source-row-'+r.source_row,e1:r.ai,n1:r.ai+r.bi,e2:r.ci,n2:r.ci+r.di})));
   return {result:window._almLastMhPeto(),studies:window.__mhPetoBusStudies(),labbe:window.__almLabbe,frag:window.__capturedFrag,
    pooledText:document.getElementById('pooled-body').innerText,studyText:document.getElementById('per-body').innerText,fragText:document.getElementById('fragility-note').innerText,
    forestMarks:document.querySelectorAll('#forest polygon').length};
  },{cfg,measure});
  out.push({id,...entry});fs.writeFileSync(output,JSON.stringify(out,null,2));
  if(++count%30===0)console.log(`${output}: ${count}/${corpus.length*3} page configurations`);
 }
 await page.screenshot({path:output.replace('.json','-screenshot.png'),fullPage:true});
 fs.writeFileSync(output.replace('.json','-browser-errors.json'),JSON.stringify(errors,null,2));
 await browser.close();console.log(`Completed ${out.length} page configurations; ${errors.length} browser errors`);
})().catch(e=>{console.error(e);process.exit(1)});
