"""Run the unchanged original comparison and R validator against fresh browser records."""
import csv, json, shutil, subprocess, sys
from pathlib import Path
from checks import compare, compare_tails
ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT/'rerun/v1.1.0'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def run(cmd, log):
    with (WORK/log).open('w', encoding='utf-8') as out:
        p = subprocess.Popen(cmd, cwd=WORK, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             text=True, encoding='utf-8', errors='replace')
        for line in p.stdout:
            print(line, end=''); out.write(line)
        if p.wait(): raise SystemExit(p.returncode)
def preserve():
    # Verify the pinned release evidence before preserving it outside the archive.
    from recut_manifest import verify_run_evidence
    verify_run_evidence()
    if not WORK.exists():
        print('No previous replay folder to preserve')
        return
    base = (ROOT.parent/'attempts').resolve()
    assert base.parent == ROOT.parent.resolve(), 'Attempts must stay beside the archive'
    assert WORK.resolve() == ROOT.resolve()/'rerun/v1.1.0', 'Replay folder must not redirect elsewhere'
    base.mkdir(exist_ok=True)
    attempt = 1
    dest = base/f'v1.1.0-attempt-{attempt}'
    while dest.exists():
        attempt += 1
        dest = base/f'v1.1.0-attempt-{attempt}'
    assert dest.resolve().parent == base, 'Backup must stay inside attempts'
    WORK.rename(dest)
    print('Preserved previous replay as '+'../'+dest.relative_to(ROOT.parent).as_posix())
def prepare():
    if (WORK/'results/app-patched.json').exists():
        raise SystemExit('Fresh run required: move rerun/v1.1.0 elsewhere before restarting. No browser resumption allowed.')
    for folder in ['data', 'results', 'outputs']: (WORK/folder).mkdir(parents=True, exist_ok=True)
    for f in ['data/corpus.json','results/reference.json','results/fragility-reference.json','validate.R']:
        shutil.copyfile(ROOT/f, WORK/f)
    for src,dst in [('data/corpus.json','corpus.json'),('results/reference.json','reference.json'),
                    ('results/fragility-reference.json','fragility-reference.json')]:
        shutil.copyfile(ROOT/src,WORK/dst)
    print('Prepared fresh original protocol with unchanged corpus, references and validate.R')
def compare_fresh():
    assert read(WORK/'results/app-patched-browser-errors.json') == [], 'Browser page errors'
    run([sys.executable,str(ROOT/'bench/compare.py'),'results/app-patched.json','results/comparison.json'],'compare.log')
    apps = read(WORK/'results/app-patched.json'); refs = read(WORK/'reference.json')
    summary, ledger = compare(refs, read(WORK/'corpus.json'), apps, read(WORK/'fragility-reference.json'))
    tails = compare_tails(refs, apps)
    assert summary == read(WORK/'results/comparison.json')
    assert tails == read(WORK/'results/comparison.tails.json')
    assert (summary['pass'],summary['checks']) == (68461,68461)
    assert (tails['passed'],tails['checks']) == (106,106)
    (WORK/'results/check-ledger.json').write_text(json.dumps(ledger,indent=2)+'\n',encoding='utf-8')
    print('FRESH ORIGINAL PASS: 68461/68461; tails 106/106')
def r_validate():
    assert (WORK/'results/check-ledger.json').is_file(), 'Run fresh comparison first'
    run(['Rscript','validate.R'],'validate-R.log')
    for name,n in [('validate_R_table.csv',68461),('validate_R_tails.csv',106)]:
        with (WORK/'outputs'/name).open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f))
        assert len(rows)==n and all(r['Result']=='PASS' for r in rows),name
    print('FRESH R PASS: 68461/68461; tails 106/106')
if __name__ == '__main__':
    actions={'preserve':preserve,'prepare':prepare,'compare':compare_fresh,'r':r_validate}
    if len(sys.argv)!=2 or sys.argv[1] not in actions: raise SystemExit('Usage: recut_runner.py preserve|prepare|compare|r')
    actions[sys.argv[1]]()
