"""Fail-closed source, output, numerical ledger and image verification."""
import csv,hashlib,json,math,re,tempfile
from pathlib import Path
from PIL import Image
import yaml
from make_outputs import ROOT,read,build
EXCLUDED={'.git','__pycache__','node_modules','rerun','outputs'}
def sources():
    return sorted(p for p in ROOT.rglob('*') if p.is_file() and not any(x in EXCLUDED or x.startswith('.verify-') for x in p.relative_to(ROOT).parts) and p.name not in {'SOURCE_SHA256.json','PROGRESS.md'})
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def csvread(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def main():
    manifest=read(ROOT/'SOURCE_SHA256.json')
    assert manifest=={p.relative_to(ROOT).as_posix():sha(p) for p in sources()},'Source inventory/hash mismatch'
    app=read(ROOT/'app/app-sha256.json')
    assert app=={p.relative_to(ROOT/'app').as_posix():sha(p) for p in (ROOT/'app').rglob('*') if p.is_file() and p.name!='app-sha256.json'}
    for p in sources():
        if p.suffix.lower() in {'.json','.js','.mjs','.py','.r','.md','.csv','.txt','.html','.cff','.patch','.css'}:
            raw=p.read_bytes();assert not raw.startswith(b'\xef\xbb\xbf'),p
            text=raw.decode('utf-8')
            assert not re.search(r'\b[A-Za-z]:[\\/](?:Users|Projects|claude-temp|E156|ProjectIndex)[\\/]',text),'Machine path: '+str(p)
        assert p.name not in {'paper.md','paper_v2_dictated_text.md'},'Manuscript draft'
    page=ROOT/'app/mh-peto/index.html'
    for ref in re.findall(r'(?:src|href)="([^"]+)"',page.read_text(encoding='utf-8')):
        if ref.endswith(('.js','.css')) and not re.match(r'^\w+:',ref):
            target=(page.parent/ref).resolve();assert target.is_relative_to(ROOT/'app') and target.is_file(),ref
    pins=read(ROOT/'app/mh-peto/validate/MANIFEST.json')['files']
    adapter=(ROOT/'app/mh-peto/validate/adapter.js').read_text()
    for item in pins:
        p=page.parent/item['path'];assert sha(p)==item['sha256'] and p.stat().st_size==item['bytes']
        assert b'\r' not in p.read_bytes() and item['sha256'] in adapter
    # Every recorded HTTP request must have a byte-identical archived asset.
    for evidence in (ROOT/'results').glob('*.requests.json'):
        from urllib.parse import urlsplit,unquote
        ev=read(evidence);assert ev['status']=='passed',evidence
        for url in ev['requests']:
            if url.startswith('http'):
                rel=unquote(urlsplit(url).path).lstrip('/')
                assert rel in app,'Fetched asset absent: '+rel
    with tempfile.TemporaryDirectory(prefix='.verify-',dir=ROOT) as tmp:
        out=Path(tmp);build(out)
        expected={p.name for p in (ROOT/'outputs').iterdir() if p.is_file() and p.name not in {'validate_R_table.csv','validate_R_tails.csv'}}
        assert {p.name for p in out.iterdir()}==expected
        for p in out.iterdir():assert p.read_bytes()==(ROOT/'outputs'/p.name).read_bytes(),'Nonreproducible: '+p.name
    table=csvread(ROOT/'outputs/table1_by_quantity.csv');total=table[-1]
    for key,n in [('checks',68461),('passed_before',64256),('passed_after',68461)]:
        assert int(total[key])==sum(int(r[key]) for r in table[:-1])==n
    sizes=read(ROOT/'outputs/sizes.json')
    for name,v in sizes.items():
        with Image.open(ROOT/'outputs'/name) as im:
            assert [im.width,im.height]==[v['width_pixels'],v['height_pixels']]
            assert abs(im.width/300*25.4-170)<.1
            assert all(abs(float(d)-300)<.001 for d in im.info['dpi'])
    for stem in ['figure2_agreement','visual_abstract']:
        with Image.open(ROOT/'outputs'/f'{stem}.png') as a,Image.open(ROOT/'outputs'/f'{stem}.tif') as b:assert a.convert('RGB').tobytes()==b.convert('RGB').tobytes()
    rtable=ROOT/'outputs/validate_R_table.csv'
    if rtable.exists():
        rows=csvread(rtable);assert len(rows)==68461
        expected=read(ROOT/'outputs/check_ledger.json')
        assert [(r['configuration'],r['quantity']) for r in rows]==[(r['configuration'],r['quantity']) for r in expected]
        for r in rows:
            a,b=r['App'],r['R'];tol=float(r['Tolerance']);q=r['quantity']
            d=0 if a==b=='NA' else math.inf if 'NA' in [a,b] else abs(float(a)-float(b))/(1 if q.endswith('.p') or '.display_' in q and not q.endswith('_defined') else max(1,abs(float(b))))
            assert math.isclose(d,float(r['Difference']),rel_tol=1e-4,abs_tol=1e-12),r
            assert r['Result']==('PASS' if d<=tol else 'FAIL')=='PASS'
    tails=read(ROOT/'outputs/tail_checks.json')
    assert tails['checks']>0 and tails['passed']==tails['checks']
    rt=csvread(ROOT/'outputs/validate_R_tails.csv')
    assert [(r['configuration'],r['quantity']) for r in rt]==[(r['configuration'],r['quantity']) for r in tails['rows']]
    for r in rt:
        a,b=float(r['App']),float(r['R'])
        d=abs(a-b)/b if b>0 else 0 if a==0 else math.inf
        assert d<=1e-9 and r['Result']=='PASS' and float(r['Tolerance'])==1e-9
        assert math.isclose(d,float(r['Difference']),rel_tol=1e-4,abs_tol=1e-12)
    print(f"TAIL ARCHIVE PASS: {tails['passed']}/{tails['checks']} relative p-value checks; {tails['z_ge_8']} with |z| >= 8; R tail table verified.")
    z=read(ROOT/'.zenodo.json');cff=yaml.safe_load((ROOT/'CITATION.cff').read_text())
    assert z['title']==cff['title']=='Mantel-Haenszel and Peto meta-analysis in the browser: a tool validated against the R package metafor'
    assert z['creators']==[{'name':'Ahmad, Mahmood'}] and cff['authors']==[{'family-names':'Ahmad','given-names':'Mahmood'}]
    assert z['version']==cff['version']=='1.0.0' and z['license']==cff['license']=='MIT'
    assert {(r['identifier'],r['relation']) for r in z['related_identifiers']}=={('https://github.com/mahmood726-cyber/allmeta','isDerivedFrom'),('10.5281/zenodo.23288388','isDerivedFrom')}
    assert (ROOT/'.gitattributes').read_text().strip()=='* -text'
    print(f'ARCHIVE PASS: {len(app)} app hashes; {len(manifest)} source hashes; 68461/68461 final checks; tables, paired image pixels and reproducible outputs verified.')
if __name__=='__main__':main()
