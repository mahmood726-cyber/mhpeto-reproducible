"""Regenerate or verify recut inventories; never regenerate upstream oracle pins."""
import argparse, hashlib, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {'.git', '__pycache__', 'node_modules', 'rerun', 'outputs'}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def dump(p, x): p.write_text(json.dumps(x, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
def sources():
    return sorted(p for p in ROOT.rglob('*') if p.is_file()
        and not any(x in EXCLUDED or x.startswith('.verify-') for x in p.relative_to(ROOT).parts)
        and p.name not in {'SOURCE_SHA256.json', 'PROGRESS.md'})
def inventory():
    return {p.relative_to(ROOT).as_posix(): sha(p) for p in sources()}
def app_inventory():
    return {p.relative_to(ROOT/'app').as_posix(): sha(p)
            for p in sorted((ROOT/'app').rglob('*'))
            if p.is_file() and p.name != 'app-sha256.json'}
def verify_run_evidence():
    man = read(ROOT/'RERUN_SHA256.json')
    # Pin only the release run; earlier attempts are not release evidence.
    evidence = ROOT/'rerun/v1.1.0'
    required = {
        'RUN_LOG.txt', 'compare.log', 'validate-R.log', 'plus-comparison.json',
        'results/comparison.json', 'results/comparison.tails.json',
        'results/app-patched-browser-errors.json'}
    large = {
        'results/app-patched.json', 'results/check-ledger.json',
        'outputs/validate_R_table.csv'}
    assert set(man) == {'required_files', 'large_files'}, 'Run evidence manifest sections'
    for section, names in [('required_files', required), ('large_files', large)]:
        assert set(man[section]) == names, 'Run evidence inventory: '+section
        for name, rec in man[section].items():
            assert set(rec) == {'sha256', 'bytes'}, name
            assert len(rec['sha256']) == 64 and all(c in '0123456789abcdef' for c in rec['sha256']), name
            assert isinstance(rec['bytes'], int) and rec['bytes'] > 0, name
            p = evidence/name
            if section == 'large_files' and not p.exists():
                continue  # Recorded hashes permit omitting these large release payloads.
            assert p.is_file(), 'Missing run evidence: '+name
            assert p.stat().st_size == rec['bytes'] and sha(p) == rec['sha256'], 'Run evidence changed: '+name
    print('RUN EVIDENCE PASS: 7 required files; 3 large-file hashes recorded and checked when present')
def verify_pins():
    verify_run_evidence()
    protected = read(ROOT/'ORIGINAL_INPUTS_SHA256.json')
    for name, digest in protected.items():
        assert sha(ROOT/name) == digest, 'Original evidence changed: '+name
    for directory, name, base in [
        ('app/mh-peto/validate', 'MANIFEST.json', ROOT/'app/mh-peto'),
        ('validation-plus', 'MANIFEST-plus.json', ROOT/'validation-plus')]:
        man = read(ROOT/directory/name)
        entries = list(man['files'])
        if 'claims' in man: entries.append(man['claims']['file'])
        for f in entries:
            p = base/f['path']
            assert sha(p) == f['sha256'] and p.stat().st_size == f['bytes'], str(p)
    man = read(ROOT/'validation-plus/MANIFEST-plus.json')
    assert (man['expectedPassed'], man['checks'], len(man['documentedFailures'])) == (120000,120010,10)
    assert (man['claims']['expectedPassed'],man['claims']['checks']) == (3793,3793)
    assert (ROOT/'validation-plus/corpus/corpus.json').read_bytes() == (ROOT/'app/mh-peto/validate/corpus/corpus.json').read_bytes()
    audit = read(ROOT/'APP_DEPENDENCIES.json')
    for parent, literal, target in audit['literal_dependency_edges'] + audit.get('dynamic_dependency_edges', []):
        assert (ROOT/'app'/parent).is_file() and (ROOT/'app'/target).is_file(), target
    base = ROOT/'app/r-shiny/shinylive/webr'
    runtime = read(base/'repo/manifest.json')
    records = {p['package']: p for p in runtime['packages']}
    seen = set()
    def visit(name):
        if name in seen or name not in records: return
        seen.add(name)
        rec = records[name]
        p = base/(rec.get('path') or ('repo/'+runtime['layout']+rec['file']))
        assert p.is_file() and sha(p)==rec['sha256'] and p.stat().st_size==rec['bytes'], str(p)
        for dep in rec.get('dependencies', []): visit(dep)
    visit('metafor')
    print('ORIGINAL INPUTS AND PLUS PINS PASS; app dependencies and webR package pins verified')
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--verify', action='store_true')
    args = ap.parse_args()
    if args.write:
        verify_pins()
        dump(ROOT/'app/app-sha256.json', app_inventory())
        dump(ROOT/'SOURCE_SHA256.json', inventory())
        print('Regenerated app/app-sha256.json and SOURCE_SHA256.json')
    else:
        assert read(ROOT/'app/app-sha256.json') == app_inventory(), 'App inventory/hash mismatch'
        assert read(ROOT/'SOURCE_SHA256.json') == inventory(), 'Source inventory/hash mismatch'
        verify_pins()
        print('MANIFEST PASS: app and archive inventories match')
if __name__ == '__main__': main()
