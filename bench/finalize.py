import csv, hashlib, json, subprocess, sys
from pathlib import Path

def load(p):return json.loads(Path(p).read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
corpus=load('corpus.json');audit=load('dataset-audit.json');ref=load('reference.json');frag=load('fragility-reference.json')
expected={c['id']+'|'+m for c in corpus for m in ['OR','RR','RD']}
eligible={c['id']+'|'+m for c in corpus if len(c['rows'])>=2 for m in ['OR','RR','RD']}
assert len({c['id'] for c in corpus})==len(corpus)
assert {r['id'] for r in frag}==eligible, 'Fragility reference is incomplete'
assert len(ref)==4*len(corpus)
for f in ['app.json','app-patched.json']:
    assert {a['id'] for a in load(f)}==expected, f+' incomplete'
    assert len(load(f))==len(expected)
    assert load(f.replace('.json','-browser-errors.json'))==[]
logs={};results={}
for label,f in [('original','app.json'),('patched','app-patched.json')]:
    run=subprocess.run([sys.executable,'compare.py',f,'results-'+label+'.json'],capture_output=True,text=True,check=True)
    Path('compare-'+label+'.log').write_text(run.stdout,encoding='utf8')
    logs[label]=run.stdout;results[label]=load('results-'+label+'.json')
    print(label+': '+run.stdout.splitlines()[-1])
src=Path('<ALLMETA_ROOT>')
commit=subprocess.check_output(['git','-C',str(src),'rev-parse','HEAD'],text=True).strip()
assert commit=='6036f3b6c1fd404b6da7916460faa8b3ebaf56bc'
for name,digest in load('source-hashes.json').items():assert sha(src/name)==digest, name+' source changed'
patchcheck=subprocess.run(['git','-C',str(src),'apply','--check','--ignore-space-change','--ignore-whitespace',str(Path('fix.patch').resolve())],capture_output=True,text=True)
assert patchcheck.returncode==0,patchcheck.stderr
used=[a for a in audit if a['configurations']];rows=[r for c in corpus for r in c['rows']]
zero=sum(any(r[k]==0 for k in ['ai','bi','ci','di']) for r in rows)
doublezero=sum((r['ai']==0 and r['ci']==0) or (r['bi']==0 and r['di']==0) for r in rows)
metadata={'source_commit':commit,'datasets_enumerated':len(audit),'datasets_used':len(used),'datasets_excluded':len(audit)-len(used),'outcome_comparison_configurations':len(corpus),'eligible_configurations':len(eligible)//3,'single_row_configurations':len(corpus)-len(eligible)//3,'page_runs_each':len(expected),'reference_fits':len(ref),'row_occurrences':len(rows),'zero_cell_row_occurrences':zero,'double_zero_or_double_all_event_occurrences':doublezero,'fragility_configurations':len(frag),'reference_errors':sum('error'in r for r in ref),'reference_warning_configurations':sum(bool(r['warnings']) for r in ref),'source_hashes_unchanged':True,'patch_applies_cleanly':True,'artifact_sha256':{p:sha(p) for p in ['corpus.json','reference.json','app.json','app-patched.json','fragility-reference.json','fix.patch']}}
combined={'metadata':metadata,**results}
Path('results.json').write_text(json.dumps(combined,indent=2,allow_nan=False),encoding='utf8')
with Path('configurations.csv').open('w',encoding='utf8',newline='') as f:
    w=csv.writer(f);w.writerow(['id','dataset','outcome','comparison','mapping','mode','valid_rows','page_status'])
    for c in corpus:w.writerow([c[k] for k in ['id','dataset','outcome','comparison','mapping','mode']]+[len(c['rows']),'eligible' if len(c['rows'])>=2 else 'single-row page refusal'])
with Path('dataset-audit.csv').open('w',encoding='utf8',newline='') as f:
    w=csv.writer(f);w.writerow(['dataset','configurations','reason','columns'])
    for a in audit:w.writerow([a['dataset'],a['configurations'],a['reason'],','.join(a['columns'])])

o=results['original'];p=results['patched']
text=f'''# MH/Peto validation against metafor

Actual local runs on 2026-10-12. The unchanged app fails: **{o['pass']}/{o['checks']} checks pass**. The patched copy: **{p['pass']}/{p['checks']} checks pass**. These totals include full-precision numerical checks, rounded UI checks, and structural/refusal checks; their tolerances are separated below. No reference values were embedded in the app.

Source commit: `{commit}` (`git -C <ALLMETA_ROOT> rev-parse HEAD`). R 4.6.0; metafor 5.2-1; metadat 1.6-0. See `session.txt`. Original source hashes were verified unchanged, and `git apply --check` accepts `fix.patch`. No changes were applied outside this job folder. This is a validation result, not a deployment or Overmind certification.

The initial O'Brien Peto reference calls overflowed R's integer arithmetic in three configurations. Their errors/warnings are preserved in `reference-integer-overflow.json`. Final `reference.R` explicitly stores the identical integer-valued counts as doubles before calling metafor. No counts were changed. This was a reference-harness correction, not an app defect or an excluded case.

## Corpus and coverage

`data(package="metadat")` enumerated **{len(audit)} datasets**. **{len(used)} datasets** supplied **{len(corpus)} outcome/comparison configurations**, and **{len(audit)-len(used)} datasets** were excluded with reasons in the table below. **{len(eligible)//3} configurations** have at least two valid rows. **{len(corpus)-len(eligible)//3}** have one valid row: R can fit these, but the page requires two; these are explicit scope exclusions from numerical pooling comparisons, not alleged matched R refusals.

Each browser run exercised **{len(expected)} page configurations** (OR, RR, RD); OR also computes Peto. R produced **{len(ref)} reference fit records**. Corpus row occurrences: **{len(rows)}**, including **{zero}** with at least one zero cell and **{doublezero}** with no events in both arms or all events in both arms. Counts are occurrences across outcome/comparison configurations, not independent trials. Some datasets overlap historically and multi-arm trials contribute to separate pairwise configurations; these are software test cases, not a new clinical meta-analysis.

`corpus.json` is the shared numerical input, with exact source row indices. `configurations.csv` records every outcome/comparison and column mapping. `excluded-rows.json` records missing, fractional, invalid, or empty-arm records without imputing counts. Binary outcomes are kept separately; arm-based data are paired within studies and split by treatment pair, with duplicate same-treatment arms summed. O'Brien comparisons use within-study BMI category rank (grp), whose exact BMI bounds vary between studies; they are numerical validation configurations, not common-cutpoint clinical estimates. The Frank genotype table uses an explicit, recorded ins/ins-versus-other-genotypes dichotomy; alternative genetic models are not enumerated. Higgins uses observed responses/nonresponses, excluding missing-outcome counts. Diagnostic tables use cases versus noncases and test positivity; Hart uses stroke counts over patient denominators for numerical coverage, not the original person-time incidence-rate interpretation. No synthetic fixtures were mixed into corpus counts.

## What the shipped page actually computes

The main pooling functions are inline in `mh-peto/index.html`, not in `shared/ma-core.js`. OR uses uncorrected Mantel–Haenszel pooling and Robins–Breslow–Greenland variance. RR uses the uncorrected MH estimator and Greenland–Robins variance. The original RD variance is a weighted sum of binomial within-study variances and differs from metafor's Greenland–Robins variance. Peto uses raw O−E and hypergeometric V. All main intervals use the exact 0.975 normal quantile.

For MH the reference settings are `add=c(0.5,0)`, `to=c("only0","none")`, `drop00=c(FALSE,FALSE)`, `correct=FALSE`. The second component disables correction/removal for pooling; the first controls ancillary study effect sizes. Peto uses `add=0`, `to="none"`, `drop00=TRUE`. Double-zero tables contribute zero to raw OR/RR/Peto sums; they are retained in MH RD. The displayed `k` is input-row count, not Peto's effective information-bearing study count. Per-study OR/RR displays use 0.5 in all four cells only when a table has a zero; per-study RD is uncorrected. The original RR display incorrectly retained the old arm totals after adding the correction.

The export exposes estimates, CIs, z and p, not pooled beta/SE. The runner recovers beta and SE algebraically from full-precision exported estimates/CIs; these are marked as recovered rather than direct function access. Per-study beta/SE come from the page's own cross-tool bus; zero-SE RD rows are intentionally omitted from that bus and are instead verified in the displayed table. Full-precision pooled outputs and actual table text are both checked.

**CMH/MH, Tarone, Breslow–Day, Q, Q p-value, I² and H² are not returned or displayed as MH/Peto statistics by this page.** The unused `Q = mh._Q` assignment reads an absent property. The shared DL engine computes heterogeneity internally for fragility, which does not provide MH/Peto heterogeneity outputs. `reference.json` records the R quantities where available, but no parity checks or successes are claimed for absent app outputs. Their `correct` choice affects R-only test statistics and cannot be inferred from an absent app test.

The L'Abbé plot is independently checked against metafor inverse-variance FE estimates and raw event-rate coordinates, including its reference curve. It uses RR when RR is selected, and OR for both OR and RD selections; it is not an MH/Peto curve. Original label “the pooled effect” obscured this distinction, and “point area proportional to study size” was inaccurate because the radius contains an additive offset. The patch clarifies both labels without changing that diagnostic's mathematics.

Fragility is a separate DL random-effects greedy diagnostic, with 0.5-to-zero-table correction and double-zero/double-all-event removal. The independent R greedy implementation validates FI/FQ for all **{len(frag)} eligible page configurations**; its initial and final fits are also checked with metafor::rma.uni at 1e-9. A greedy index is not a proof of the global minimum number of modifications. Non-significant results return an undefined FI, as designed. Main `reference.json` records **{metadata['reference_warning_configurations']} warning-bearing configurations** and **{metadata['reference_errors']} R errors** with messages. The ancillary greedy oracle suppresses routine rma.uni warnings but stops on baseline/final numerical disagreement. R startup reported unavailable C.UTF-8 locale settings; all final JSON parses successfully and source identifiers are row indices, not inferred clinical IDs.

## Failures and minimal fixes

1. `mh-peto/index.html:249–266`: MH RD SE uses weighted binomial variances rather than Greenland–Robins. This changes SE, CI, z and p. The patch uses the variance in the installed metafor rma.mh source (`rma-mh-source.txt`).
2. `mh-peto/index.html:204–208`: low-accuracy normal CDF approximation produces p-value errors above 1e-9. The patch uses a convergent normal-integral series with tail saturation beyond |z|=8 (absolute tail error below the required tolerance).
3. `mh-peto/index.html:297–301`: zero-cell RR display corrects a/c but divides by the original n1/n2. The patch uses corrected a+b and c+d in estimates and variances.
4. `mh-peto/index.html:336,370–389`: `pooled[0]` is assumed to be MH and Peto export assumes two pooled results. In `dat.axfors2021 | death | cq / Standard of Care`, MH OR is undefined but Peto is finite; the original export mislabels Peto as MH and omits the Peto fields. The patch selects results by method name.
5. `shared/fragility.js:55`, via `shared/ma-core.js:199–200,229`: DL CIs use the approximate inverse-normal quantile. Some discrepancies exceed 1e-9. The patch uses fragility.js's existing exact Z975 constant and the unchanged DL SE.
6. `mh-peto/index.html:318`: fewer than two rows clears export state but leaves old visible results. The patch clears result panels and shows the minimum-input message. This is tested separately from statistical parity.
7. `mh-peto/index.html:127,348–352`: diagnostic labels did not make the separate IV/DL models clear. The patch labels DL fragility and describes the L'Abbé model explicitly.

`fix.patch` changes only `mh-peto/index.html` and one return statement in `shared/fragility.js`. The shipped source is unchanged. The local `patched/` tree is runnable. The existing orientation test `mh-peto/tests/test_against_metafor.py` checks saved constants against R; it does not itself call the page and therefore does not cover these displayed-output issues.

## Tolerances and per-quantity results

For full-precision closed-form quantities: `abs(app-ref)/max(1,abs(ref)) <= 1e-9`; p-values use absolute difference. FI/FQ and structural checks use the same threshold (integer equality for counts in practice). Rounded UI values use absolute half a display unit plus 1e-10: 0.0005000001 for 3 decimals, 0.0050000001 for 2-decimal z. Rounded checks do not relax the full-precision tolerance. A missing/null value passes only against another undefined value; undefined mismatches are listed separately from finite maxima. There are no iterative-estimator tolerances in this task.

| Quantity | Original pass/checks | Original max finite error | Original undefined mismatches | Patched pass/checks | Patched max finite error | Tolerance |
|---|---:|---:|---:|---:|---:|---:|
'''
for q in sorted(set(o['quantities'])|set(p['quantities'])):
    a=o['quantities'].get(q,{'pass':0,'checks':0,'max_difference':0,'nonfinite_mismatches':0});b=p['quantities'].get(q,{'pass':0,'checks':0,'max_difference':0,'tolerance':0})
    text+=f"| {q} | {a['pass']}/{a['checks']} | {a['max_difference']:.12g} | {a['nonfinite_mismatches']} | {b['pass']}/{b['checks']} | {b['max_difference']:.12g} | {b['tolerance']} |\n"
text+='''
## Reproduction and verbatim final output

Run in this job folder (PowerShell); no installation or network access is needed:

```powershell
$env:R_LIBS_USER='<R_LIBS_USER>'
Rscript inspect.R
Rscript docs.R
Rscript build.R
Rscript reference.R
node run-app.cjs <ALLMETA_ROOT> app.json
Rscript fragility-reference.R
python make-fix.py
node run-app.cjs patched app-patched.json
python finalize.py
```

The runner resumes an existing output JSON by configuration ID. For a fresh rerun, give it a new output filename or archive the old output first. This was done for each patched round; `app-patched-round1.json` and `app-patched-round2.json` retain superseded intermediate runs. Final comparisons use only `app.json` and `app-patched.json`. Exploratory failures, including an initial Windows BOM parsing error in inspect.R, were resolved before the final scripts; all scripts now use UTF-8 without BOM.

Verbatim final lines (comparison stdout is also saved in compare-original.log and compare-patched.log):

```text
'''
text+=f"Enumerated {len(audit)} datasets; used {len(used)}; configurations {len(corpus)}; reference fits {len(ref)}\n"
text+=f"Completed {len(expected)} page configurations; 0 browser errors\n"
text+=f"Validated {len(frag)} greedy DL fragility configurations; initial and final fits agree with metafor at 1e-9\n"
text+=logs['original'].splitlines()[-1]+'\n'+logs['patched'].splitlines()[-1]+'\n```\n'
text+='''
Both actual Chrome page runs completed without uncaught JavaScript exceptions. The final patched screenshot was inspected for layout and labels. The corpus-driven browser runner plus DOM, export, diagnostic and refusal assertions serve as the E2E contract. No test assumes absent CMH/heterogeneity outputs exist.

## Static versus dynamic disclosure

| Element | Type | Source / validation |
|---|---|---|
| Column mappings, comparison grouping, tolerances, correction policies | Static | Explicit in build.R; checked against installed package documentation |
| Corpus counts and row values | Dynamic | Installed metadat 1.6-0; recorded source rows and exclusions |
| Statistical reference values | Dynamic | Executed metafor 5.2-1, full-precision JSON |
| Greedy FI/FQ | Dynamic | Independent R implementation, initial/final fits checked with metafor |
| Browser outputs and screenshots | Dynamic | Actual shipped page, then patched local copy; no method reimplementation in runner |
| Numerical constants in patch | Static | Standard normal quantile and numerical-series constants; no research outputs |
| Counts/maxima in report | Dynamic | finalize.py reads run artifacts; SHA-256 bindings in results.json |

## Dataset disposition

Configuration counts include single-row configurations recorded as page refusals. Dose-finding datasets (Roever/Ursino) are included as within-study pairs of dose cohorts for broad structural coverage; their sequential enrollment does not establish concurrent randomized treatment effects. Detailed mappings and source rows are in configurations.csv and corpus.json; detailed package descriptions are in dataset-docs/.

| Dataset | Configurations | Used / exclusion reason |
|---|---:|---|
'''
for a in audit:text+=f"| {a['dataset']} | {a['configurations']} | {a['reason']} |\n"
Path('RESULTS.md').write_text(text,encoding='utf8')
assert p['pass']==p['checks'], 'Patched comparisons fail; inspect results-patched.json'
Path('PROGRESS.md').write_text('Completed. See RESULTS.md and results.json for source-bound counts, tolerances, failures, patch and final validation. Original source unchanged.\n',encoding='utf8')
print('Final artifacts verified; patched comparison PASS; original source unchanged; patch applicability PASS')
