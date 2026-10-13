from pathlib import Path
import shutil,difflib,hashlib,json
src=Path('<ALLMETA_ROOT>');dst=Path('patched')
for sub in ['mh-peto','shared','hub/shared']:
    shutil.copytree(src/sub,dst/sub,dirs_exist_ok=True,ignore=shutil.ignore_patterns('node_modules','.git','tests'))
p=dst/'mh-peto/index.html';old=p.read_text(encoding='utf8');new=old
start=new.index('    function pnorm(x) {');end=new.index('    function fmt',start)
new=new[:start]+'''    function pnorm(x) {
      // Convergent normal-integral series (absolute error below 1e-14).
      if (x >= 8) return 1;
      if (x <= -8) return 0;
      var term = x, sum = x, q = x * x;
      for (var i = 3; i < 1000; i += 2) {
        term *= q / i;
        var next = sum + term;
        if (next === sum) break;
        sum = next;
      }
      return Math.max(0, Math.min(1, 0.5 + sum * Math.exp(-q / 2) / Math.sqrt(2 * Math.PI)));
    }
''' + new[end:]
new=new.replace('if (denom === 0) return null;\n      var rr', 'if (denom === 0 || num === 0) return null;\n      var rr')
start=new.index('    function mhRD(rows) {');end=new.index('    function peto',start)
new=new[:start]+'''    function mhRD(rows) {
      var num = 0, denom = 0, va = 0, vb = 0;
      for (var i = 0; i < rows.length; i++) {
        var r = rows[i], a = r.e1, c = r.e2;
        var n1 = r.n1, n2 = r.n2, n = n1 + n2;
        num += a * n2 / n - c * n1 / n;
        denom += n1 * n2 / n;
        // Greenland-Robins variance used by metafor::rma.mh(measure="RD").
        va += c * Math.pow(n1 / n, 2) - a * Math.pow(n2 / n, 2)
          + (n1 / n) * (n2 / n) * (n2 - n1) / 2;
        vb += (a * (n2 - c) / n + c * (n1 - a) / n) / 2;
      }
      if (denom === 0) return null;
      var rd = num / denom;
      var se = Math.sqrt(rd * va + vb) / denom;
      return { est: rd, se: se, lo: rd - Z975 * se, hi: rd + Z975 * se };
    }

''' + new[end:]
new=new.replace('var rr = (a / r.n1) / (c / r.n2);','var rr = (a / (a + b)) / (c / (c + d));').replace('var varLogRR = 1 / a - 1 / r.n1 + 1 / c - 1 / r.n2;','var varLogRR = 1 / a - 1 / (a + b) + 1 / c - 1 / (c + d);')
new=new.replace("'Fragility index = '","'DL fragility index = '").replace("'Fragility index: '","'DL fragility index: '")
new=new.replace('point area ∝ study size','point size increases with study size').replace('the curve is the pooled effect held constant. Matches <code>metafor::labbe</code>.','the curve holds an inverse-variance fixed-effect estimate constant (RR for the RR selection, OR otherwise, including the RD selection). It is separate from the MH/Peto estimates above.')
new=new.replace('if (rows.length < 2) { _lastResults = null; return; }', '''if (rows.length < 2) {
        _lastResults = null;
        ['pooled-body', 'per-body', 'forest', 'labbe'].forEach(function (id) { document.getElementById(id).innerHTML = ''; });
        document.getElementById('fragility-note').textContent = 'Enter at least two valid studies.';
        return;
      }''')
# Export the correct method even when only Peto is estimable.
new=new.replace('var firstPooled = pooled[0] || null;',"var firstPooled = pooled.find(function (p) { return p.name.indexOf('MH ') === 0; }) || null;")
new=new.replace("if (measure === 'OR' && pooled.length >= 2) {\n        var pe2 = pooled[1];", "var pe2 = pooled.find(function (p) { return p.name === 'Peto OR'; });\n      if (measure === 'OR' && pe2) {")
p.write_text(new,encoding='utf8',newline='')
f=dst/'shared/fragility.js';fold=f.read_text(encoding='utf8')
fnew=fold.replace('return { mu: r.mu, ciLo: r.ciLo, ciHi: r.ciHi };','return { mu: r.mu, ciLo: r.mu - Z975 * r.se, ciHi: r.mu + Z975 * r.se };')
assert fnew!=fold
f.write_text(fnew,encoding='utf8',newline='')
patch=''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='a/mh-peto/index.html',tofile='b/mh-peto/index.html'))
patch+=''.join(difflib.unified_diff(fold.splitlines(True),fnew.splitlines(True),fromfile='a/shared/fragility.js',tofile='b/shared/fragility.js'))
Path('fix.patch').write_text(patch,encoding='utf8')
manifest={str(f.relative_to(src)):hashlib.sha256(f.read_bytes()).hexdigest() for sub in ['mh-peto','shared','hub/shared'] for f in (src/sub).glob('*') if f.is_file()}
Path('source-hashes.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
print('Created fix.patch and patched page; original source untouched')
