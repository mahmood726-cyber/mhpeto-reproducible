# MH/Peto validation against metafor

Actual local runs on 2026-10-12. The unchanged app fails: **64256/68461 checks pass**. The patched copy: **68461/68461 checks pass**. These totals include full-precision numerical checks, rounded UI checks, and structural/refusal checks; their tolerances are separated below. No reference values were embedded in the app.

Source commit: `6036f3b6c1fd404b6da7916460faa8b3ebaf56bc` (`git -C <ALLMETA_ROOT> rev-parse HEAD`). R 4.6.0; metafor 5.2-1; metadat 1.6-0. See `session.txt`. Original source hashes were verified unchanged, and `git apply --check` accepts `fix.patch`. No changes were applied outside this job folder. This is a validation result, not a deployment or Overmind certification.

The initial O'Brien Peto reference calls overflowed R's integer arithmetic in three configurations. Their errors/warnings are preserved in `reference-integer-overflow.json`. Final `reference.R` explicitly stores the identical integer-valued counts as doubles before calling metafor. No counts were changed. This was a reference-harness correction, not an app defect or an excluded case.

## Corpus and coverage

`data(package="metadat")` enumerated **114 datasets**. **55 datasets** supplied **336 outcome/comparison configurations**, and **59 datasets** were excluded with reasons in the table below. **252 configurations** have at least two valid rows. **84** have one valid row: R can fit these, but the page requires two; these are explicit scope exclusions from numerical pooling comparisons, not alleged matched R refusals.

Each browser run exercised **1008 page configurations** (OR, RR, RD); OR also computes Peto. R produced **1344 reference fit records**. Corpus row occurrences: **2473**, including **429** with at least one zero cell and **155** with no events in both arms or all events in both arms. Counts are occurrences across outcome/comparison configurations, not independent trials. Some datasets overlap historically and multi-arm trials contribute to separate pairwise configurations; these are software test cases, not a new clinical meta-analysis.

`corpus.json` is the shared numerical input, with exact source row indices. `configurations.csv` records every outcome/comparison and column mapping. `excluded-rows.json` records missing, fractional, invalid, or empty-arm records without imputing counts. Binary outcomes are kept separately; arm-based data are paired within studies and split by treatment pair, with duplicate same-treatment arms summed. O'Brien comparisons use within-study BMI category rank (grp), whose exact BMI bounds vary between studies; they are numerical validation configurations, not common-cutpoint clinical estimates. The Frank genotype table uses an explicit, recorded ins/ins-versus-other-genotypes dichotomy; alternative genetic models are not enumerated. Higgins uses observed responses/nonresponses, excluding missing-outcome counts. Diagnostic tables use cases versus noncases and test positivity; Hart uses stroke counts over patient denominators for numerical coverage, not the original person-time incidence-rate interpretation. No synthetic fixtures were mixed into corpus counts.

## What the shipped page actually computes

The main pooling functions are inline in `mh-peto/index.html`, not in `shared/ma-core.js`. OR uses uncorrected Mantel–Haenszel pooling and Robins–Breslow–Greenland variance. RR uses the uncorrected MH estimator and Greenland–Robins variance. The original RD variance is a weighted sum of binomial within-study variances and differs from metafor's Greenland–Robins variance. Peto uses raw O−E and hypergeometric V. All main intervals use the exact 0.975 normal quantile.

For MH the reference settings are `add=c(0.5,0)`, `to=c("only0","none")`, `drop00=c(FALSE,FALSE)`, `correct=FALSE`. The second component disables correction/removal for pooling; the first controls ancillary study effect sizes. Peto uses `add=0`, `to="none"`, `drop00=TRUE`. Double-zero tables contribute zero to raw OR/RR/Peto sums; they are retained in MH RD. The displayed `k` is input-row count, not Peto's effective information-bearing study count. Per-study OR/RR displays use 0.5 in all four cells only when a table has a zero; per-study RD is uncorrected. The original RR display incorrectly retained the old arm totals after adding the correction.

The export exposes estimates, CIs, z and p, not pooled beta/SE. The runner recovers beta and SE algebraically from full-precision exported estimates/CIs; these are marked as recovered rather than direct function access. Per-study beta/SE come from the page's own cross-tool bus; zero-SE RD rows are intentionally omitted from that bus and are instead verified in the displayed table. Full-precision pooled outputs and actual table text are both checked.

**CMH/MH, Tarone, Breslow–Day, Q, Q p-value, I² and H² are not returned or displayed as MH/Peto statistics by this page.** The unused `Q = mh._Q` assignment reads an absent property. The shared DL engine computes heterogeneity internally for fragility, which does not provide MH/Peto heterogeneity outputs. `reference.json` records the R quantities where available, but no parity checks or successes are claimed for absent app outputs. Their `correct` choice affects R-only test statistics and cannot be inferred from an absent app test.

The L'Abbé plot is independently checked against metafor inverse-variance FE estimates and raw event-rate coordinates, including its reference curve. It uses RR when RR is selected, and OR for both OR and RD selections; it is not an MH/Peto curve. Original label “the pooled effect” obscured this distinction, and “point area proportional to study size” was inaccurate because the radius contains an additive offset. The patch clarifies both labels without changing that diagnostic's mathematics.

Fragility is a separate DL random-effects greedy diagnostic, with 0.5-to-zero-table correction and double-zero/double-all-event removal. The independent R greedy implementation validates FI/FQ for all **756 eligible page configurations**; its initial and final fits are also checked with metafor::rma.uni at 1e-9. A greedy index is not a proof of the global minimum number of modifications. Non-significant results return an undefined FI, as designed. Main `reference.json` records **62 warning-bearing configurations** and **4 R errors** with messages. The ancillary greedy oracle suppresses routine rma.uni warnings but stops on baseline/final numerical disagreement. R startup reported unavailable C.UTF-8 locale settings; all final JSON parses successfully and source identifiers are row indices, not inferred clinical IDs.

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
| OR.beta | 247/252 | 6.99618321432e-16 | 5 | 252/252 | 6.99618321432e-16 | 1e-09 |
| OR.display_pooled_est | 247/247 | 0.000497961657733 | 0 | 247/247 | 0.000497961657733 | 0.0005000001 |
| OR.display_pooled_hi | 247/247 | 0.000497948057179 | 0 | 247/247 | 0.000497948057179 | 0.0005000001 |
| OR.display_pooled_lo | 247/247 | 0.000492760697925 | 0 | 247/247 | 0.000492760697925 | 0.0005000001 |
| OR.display_pooled_pval | 247/247 | 0.000499304598841 | 0 | 247/247 | 0.000499304598841 | 0.0005000001 |
| OR.display_pooled_zval | 247/247 | 0.00497915889744 | 0 | 247/247 | 0.00497915889744 | 0.0050000001 |
| OR.display_study_est | 2389/2389 | 0.000500000000002 | 0 | 2389/2389 | 0.000500000000002 | 0.0005000001 |
| OR.display_study_hi | 2389/2389 | 0.000499621934688 | 0 | 2389/2389 | 0.000499621934688 | 0.0005000001 |
| OR.display_study_lo | 2389/2389 | 0.000499986651637 | 0 | 2389/2389 | 0.000499986651637 | 0.0005000001 |
| OR.est | 247/252 | 7.48646125503e-16 | 5 | 252/252 | 7.48646125503e-16 | 1e-09 |
| OR.fragility_DL_beta | 252/252 | 1.22124532709e-15 | 0 | 252/252 | 1.22124532709e-15 | 1e-09 |
| OR.fragility_DL_hi | 237/252 | 1.83847315149e-09 | 0 | 252/252 | 1.75301718783e-15 | 1e-09 |
| OR.fragility_DL_lo | 247/252 | 1.51209144486e-09 | 0 | 252/252 | 2.10942374679e-15 | 1e-09 |
| OR.fragility_FI | 252/252 | 0 | 0 | 252/252 | 0 | 1e-09 |
| OR.fragility_FQ | 252/252 | 0 | 0 | 252/252 | 0 | 1e-09 |
| OR.hi | 247/252 | 9.71297141272e-16 | 5 | 252/252 | 9.71297141272e-16 | 1e-09 |
| OR.labbe_curve_max_abs_error | 252/252 | 4.4408920985e-16 | 0 | 252/252 | 4.4408920985e-16 | 1e-09 |
| OR.labbe_logEff | 252/252 | 7.5691279285e-16 | 0 | 252/252 | 7.5691279285e-16 | 1e-09 |
| OR.labbe_pc | 2389/2389 | 0 | 0 | 2389/2389 | 0 | 1e-09 |
| OR.labbe_pt | 2389/2389 | 0 | 0 | 2389/2389 | 0 | 1e-09 |
| OR.lo | 247/252 | 9.16970699703e-16 | 5 | 252/252 | 9.16970699703e-16 | 1e-09 |
| OR.p | 48/252 | 1.38502365257e-07 | 5 | 252/252 | 3.92741394961e-15 | 1e-09 |
| OR.se | 247/252 | 2.1151887884e-16 | 5 | 252/252 | 2.1151887884e-16 | 1e-09 |
| OR.single_row_UI_clear | 0/84 | 1 | 0 | 84/84 | 0 | 1e-09 |
| OR.single_row_refusal | 84/84 | 0 | 0 | 84/84 | 0 | 1e-09 |
| OR.study_beta | 2389/2389 | 2.68434954051e-15 | 0 | 2389/2389 | 2.68434954051e-15 | 1e-09 |
| OR.study_count | 252/252 | 0 | 0 | 252/252 | 0 | 1e-09 |
| OR.study_se | 2389/2389 | 2.68709363115e-16 | 0 | 2389/2389 | 2.68709363115e-16 | 1e-09 |
| OR.z | 247/252 | 2.16004695159e-14 | 5 | 252/252 | 2.16004695159e-14 | 1e-09 |
| PETO.beta | 247/252 | 3.70118025037e-16 | 5 | 252/252 | 3.70118025037e-16 | 1e-09 |
| PETO.display_pooled_est | 252/252 | 0.000497088207265 | 0 | 252/252 | 0.000497088207265 | 0.0005000001 |
| PETO.display_pooled_hi | 252/252 | 0.000498799712962 | 0 | 252/252 | 0.000498799712962 | 0.0005000001 |
| PETO.display_pooled_lo | 252/252 | 0.000496835515323 | 0 | 252/252 | 0.000496835515323 | 0.0005000001 |
| PETO.display_pooled_pval | 252/252 | 0.000498901591333 | 0 | 252/252 | 0.000498901591333 | 0.0005000001 |
| PETO.display_pooled_zval | 252/252 | 0.00498506133097 | 0 | 252/252 | 0.00498506133097 | 0.0050000001 |
| PETO.est | 247/252 | 1.32153214983e-15 | 5 | 252/252 | 1.32153214983e-15 | 1e-09 |
| PETO.hi | 247/252 | 1.25411398128e-15 | 5 | 252/252 | 1.25411398128e-15 | 1e-09 |
| PETO.lo | 247/252 | 1.37081558044e-15 | 5 | 252/252 | 1.37081558044e-15 | 1e-09 |
| PETO.p | 47/252 | 1.38766765856e-07 | 5 | 252/252 | 1.1174138852e-15 | 1e-09 |
| PETO.se | 247/252 | 2.07879244428e-16 | 5 | 252/252 | 2.07879244428e-16 | 1e-09 |
| PETO.z | 247/252 | 4.56690469495e-16 | 5 | 252/252 | 4.56690469495e-16 | 1e-09 |
| RD.beta | 252/252 | 1.66533453694e-16 | 0 | 252/252 | 1.12757025938e-16 | 1e-09 |
| RD.display_pooled_est | 252/252 | 0.000498927805575 | 0 | 252/252 | 0.000498927805575 | 0.0005000001 |
| RD.display_pooled_hi | 159/252 | 0.220621380026 | 0 | 252/252 | 0.000496946513652 | 0.0005000001 |
| RD.display_pooled_lo | 157/252 | 0.220699811398 | 0 | 252/252 | 0.000496695035259 | 0.0005000001 |
| RD.display_pooled_pval | 142/252 | 0.33003035627 | 0 | 252/252 | 0.000498809886995 | 0.0005000001 |
| RD.display_pooled_zval | 95/252 | 4.62955213933 | 0 | 252/252 | 0.00494045422341 | 0.0050000001 |
| RD.display_study_est | 2389/2389 | 0.0005 | 0 | 2389/2389 | 0.0005 | 0.0005000001 |
| RD.display_study_hi | 2389/2389 | 0.000499242351819 | 0 | 2389/2389 | 0.000499242351819 | 0.0005000001 |
| RD.display_study_lo | 2389/2389 | 0.000499776787572 | 0 | 2389/2389 | 0.000499776787572 | 0.0005000001 |
| RD.est | 252/252 | 1.66533453694e-16 | 0 | 252/252 | 1.12757025938e-16 | 1e-09 |
| RD.fragility_DL_beta | 252/252 | 3.33066907388e-16 | 0 | 252/252 | 3.33066907388e-16 | 1e-09 |
| RD.fragility_DL_hi | 252/252 | 5.24398413582e-10 | 0 | 252/252 | 3.33066907388e-16 | 1e-09 |
| RD.fragility_DL_lo | 252/252 | 5.24398635626e-10 | 0 | 252/252 | 4.4408920985e-16 | 1e-09 |
| RD.fragility_FI | 252/252 | 0 | 0 | 252/252 | 0 | 1e-09 |
| RD.fragility_FQ | 252/252 | 0 | 0 | 252/252 | 0 | 1e-09 |
| RD.hi | 0/252 | 0.220948593459 | 0 | 252/252 | 1.11022302463e-16 | 1e-09 |
| RD.labbe_curve_max_abs_error | 252/252 | 4.4408920985e-16 | 0 | 252/252 | 4.4408920985e-16 | 1e-09 |
| RD.labbe_logEff | 252/252 | 7.5691279285e-16 | 0 | 252/252 | 7.5691279285e-16 | 1e-09 |
| RD.labbe_pc | 2389/2389 | 0 | 0 | 2389/2389 | 0 | 1e-09 |
| RD.labbe_pt | 2389/2389 | 0 | 0 | 2389/2389 | 0 | 1e-09 |
| RD.lo | 0/252 | 0.220948593459 | 0 | 252/252 | 2.22044604925e-16 | 1e-09 |
| RD.p | 35/252 | 0.330464450959 | 0 | 252/252 | 3.60822483003e-15 | 1e-09 |
| RD.se | 0/252 | 0.112730945671 | 0 | 252/252 | 2.77555756156e-17 | 1e-09 |
| RD.single_row_UI_clear | 0/84 | 1 | 0 | 84/84 | 0 | 1e-09 |
| RD.single_row_refusal | 84/84 | 0 | 0 | 84/84 | 0 | 1e-09 |
| RD.study_beta | 2236/2236 | 0 | 0 | 2236/2236 | 0 | 1e-09 |
| RD.study_count | 252/252 | 0 | 0 | 252/252 | 0 | 1e-09 |
| RD.study_se | 2236/2236 | 5.55111512313e-17 | 0 | 2236/2236 | 5.55111512313e-17 | 1e-09 |
| RD.z | 0/252 | 0.805385882965 | 0 | 252/252 | 5.88418203051e-15 | 1e-09 |
| RR.beta | 252/252 | 6.10622663544e-16 | 0 | 252/252 | 6.10622663544e-16 | 1e-09 |
| RR.display_pooled_est | 247/247 | 0.000499770200062 | 0 | 247/247 | 0.000499770200062 | 0.0005000001 |
| RR.display_pooled_hi | 247/247 | 0.000499768603358 | 0 | 247/247 | 0.000499768603358 | 0.0005000001 |
| RR.display_pooled_lo | 247/247 | 0.000498651159897 | 0 | 247/247 | 0.000498651159897 | 0.0005000001 |
| RR.display_pooled_pval | 247/247 | 0.000499799829331 | 0 | 247/247 | 0.000499799829331 | 0.0005000001 |
| RR.display_pooled_zval | 247/247 | 0.00496711498443 | 0 | 247/247 | 0.00496711498443 | 0.0050000001 |
| RR.display_study_est | 2129/2389 | 4.891 | 0 | 2389/2389 | 0.000500000000001 | 0.0005000001 |
| RR.display_study_hi | 1993/2389 | 76.4923055735 | 0 | 2389/2389 | 0.000498892433989 | 0.0005000001 |
| RR.display_study_lo | 2253/2389 | 0.311951914509 | 0 | 2389/2389 | 0.000499863723528 | 0.0005000001 |
| RR.est | 248/252 | 6.1964379849e-16 | 4 | 252/252 | 6.1964379849e-16 | 1e-09 |
| RR.fragility_DL_beta | 252/252 | 2.83106871279e-15 | 0 | 252/252 | 2.83106871279e-15 | 1e-09 |
| RR.fragility_DL_hi | 243/252 | 1.53355839139e-09 | 0 | 252/252 | 9.54791801178e-15 | 1e-09 |
| RR.fragility_DL_lo | 249/252 | 1.46390909574e-09 | 0 | 252/252 | 3.83026943496e-15 | 1e-09 |
| RR.fragility_FI | 252/252 | 0 | 0 | 252/252 | 0 | 1e-09 |
| RR.fragility_FQ | 252/252 | 0 | 0 | 252/252 | 0 | 1e-09 |
| RR.hi | 252/252 | 9.48673429904e-16 | 0 | 252/252 | 9.48673429904e-16 | 1e-09 |
| RR.labbe_curve_max_abs_error | 252/252 | 9.99200722163e-16 | 0 | 252/252 | 9.99200722163e-16 | 1e-09 |
| RR.labbe_logEff | 252/252 | 7.88718100487e-16 | 0 | 252/252 | 7.88718100487e-16 | 1e-09 |
| RR.labbe_pc | 2389/2389 | 0 | 0 | 2389/2389 | 0 | 1e-09 |
| RR.labbe_pt | 2389/2389 | 0 | 0 | 2389/2389 | 0 | 1e-09 |
| RR.lo | 248/252 | 6.66133814775e-16 | 4 | 252/252 | 6.66133814775e-16 | 1e-09 |
| RR.p | 50/252 | 1.38582439579e-07 | 0 | 252/252 | 1.01585406753e-14 | 1e-09 |
| RR.se | 252/252 | 2.16819447962e-16 | 0 | 252/252 | 2.16819447962e-16 | 1e-09 |
| RR.single_row_UI_clear | 0/84 | 1 | 0 | 84/84 | 0 | 1e-09 |
| RR.single_row_refusal | 84/84 | 0 | 0 | 84/84 | 0 | 1e-09 |
| RR.study_beta | 2038/2389 | 0.264151575042 | 4 | 2389/2389 | 8.29197821517e-16 | 1e-09 |
| RR.study_count | 248/252 | 0.142857142857 | 0 | 252/252 | 0 | 1e-09 |
| RR.study_se | 1974/2389 | 0.183503419072 | 4 | 2389/2389 | 2.91289925646e-16 | 1e-09 |
| RR.z | 252/252 | 3.22327853772e-14 | 0 | 252/252 | 3.22327853772e-14 | 1e-09 |

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
Enumerated 114 datasets; used 55; configurations 336; reference fits 1344
Completed 1008 page configurations; 0 browser errors
Validated 756 greedy DL fragility configurations; initial and final fits agree with metafor at 1e-9
64256/68461 checks pass
68461/68461 checks pass
```

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
| dat.aloe2013 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.anand1999 | 1 | Documented binary counts; mappings and source rows in corpus.json |
| dat.anker2025 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.assink2016 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.axfors2021 | 4 | Documented binary counts; mappings and source rows in corpus.json |
| dat.bakdash2021 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.baker2009 | 16 | Documented binary counts; mappings and source rows in corpus.json |
| dat.bangertdrowns2004 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.bartos2023 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.baskerville2012 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.bassler2004 | 1 | Documented binary counts; mappings and source rows in corpus.json |
| dat.bauer2002 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.bcg | 1 | Documented binary counts; mappings and source rows in corpus.json |
| dat.begg1989 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.berkey1998 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.berkey1998r | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.besson2016 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.bonett2010 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.bornmann2007 | 1 | Documented binary counts; mappings and source rows in corpus.json |
| dat.bourassa1996 | 1 | Documented binary counts; mappings and source rows in corpus.json |
| dat.cannon2006 | 6 | Documented binary counts; mappings and source rows in corpus.json |
| dat.chiarito2020 | 4 | Documented binary counts; mappings and source rows in corpus.json |
| dat.cohen1981 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.colditz1994 | 1 | Documented binary counts; mappings and source rows in corpus.json |
| dat.collins1985a | 14 | Documented binary counts; mappings and source rows in corpus.json |
| dat.collins1985b | 4 | Documented binary counts; mappings and source rows in corpus.json |
| dat.craft2003 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.crede2010 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.crisafulli2020 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.curtin2002 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.curtis1998 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.dagostino1998 | 8 | Documented binary counts; mappings and source rows in corpus.json |
| dat.damico2009 | 1 | Documented binary counts; mappings and source rows in corpus.json |
| dat.debruin2009 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.demir2022 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.dogliotti2014 | 11 | Documented binary counts; mappings and source rows in corpus.json |
| dat.dong2013 | 10 | Documented binary counts; mappings and source rows in corpus.json |
| dat.dorn2007 | 1 | Documented binary counts; mappings and source rows in corpus.json |
| dat.dumouchel1994 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.egger2001 | 1 | Documented binary counts; mappings and source rows in corpus.json |
| dat.feng2019 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.fine1993 | 4 | Documented binary counts; mappings and source rows in corpus.json |
| dat.franchini2012 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.frank2008 | 1 | Documented binary counts; mappings and source rows in corpus.json |
| dat.furukawa2003 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.gibson2002 | 1 | Documented binary counts; mappings and source rows in corpus.json |
| dat.graves2010 | 1 | Documented binary counts; mappings and source rows in corpus.json |
| dat.greb2008 | 1 | Documented binary counts; mappings and source rows in corpus.json |
| dat.greenland1992 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.gurusamy2011 | 8 | Documented binary counts; mappings and source rows in corpus.json |
| dat.hackshaw1998 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.hahn2001 | 1 | Documented binary counts; mappings and source rows in corpus.json |
| dat.hannum2020 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.hart1999 | 2 | Structural counts over patient denominators; validates numerical 2x2 calculation, not original person-time incidence-rate analysis |
| dat.hartmannboyce2018 | 11 | Documented binary counts; mappings and source rows in corpus.json |
| dat.hasselblad1998 | 6 | Documented binary counts; mappings and source rows in corpus.json |
| dat.higgins2008 | 1 | Documented binary counts; mappings and source rows in corpus.json |
| dat.hine1989 | 1 | Documented binary counts; mappings and source rows in corpus.json |
| dat.huber2000 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.ishak2007 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.kalaian1996 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.karner2014 | 6 | Documented binary counts; mappings and source rows in corpus.json |
| dat.kearon1998 | 2 | Structural diagnostic 2x2 tables; cases versus noncases as groups, test positivity as outcome; not a treatment-effect interpretation |
| dat.knapp2017 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.konstantopoulos2011 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.landenberger2005 | 1 | Documented binary counts; mappings and source rows in corpus.json |
| dat.laopaiboon2015 | 1 | Documented binary counts; mappings and source rows in corpus.json |
| dat.lau1992 | 1 | Documented binary counts; mappings and source rows in corpus.json |
| dat.lee2004 | 1 | Documented binary counts; mappings and source rows in corpus.json |
| dat.lehmann2018 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.li2007 | 1 | Documented binary counts; mappings and source rows in corpus.json |
| dat.lim2014 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.linde2005 | 4 | Documented binary counts; mappings and source rows in corpus.json |
| dat.linde2015 | 76 | Documented binary counts; mappings and source rows in corpus.json |
| dat.linde2016 | 41 | Documented binary counts; mappings and source rows in corpus.json |
| dat.lloyd2010 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.lopez2019 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.maire2019 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.mccurdy2020 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.mcdaniel1994 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.meeker2017 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.metap | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.michael2013 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.molloy2014 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.moore1998 | 1 | Documented binary counts; mappings and source rows in corpus.json |
| dat.moura2021 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.nakagawa2007 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.nielweise2007 | 1 | Documented binary counts; mappings and source rows in corpus.json |
| dat.nielweise2008 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.nissen2007 | 2 | Documented binary counts; mappings and source rows in corpus.json |
| dat.normand1999 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.obrien2003 | 10 | Documented binary counts; mappings and source rows in corpus.json |
| dat.pagliaro1992 | 3 | Documented binary counts; mappings and source rows in corpus.json |
| dat.pignon2000 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.poole2003 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.pritz1997 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.quan2000 | 1 | Documented binary counts; mappings and source rows in corpus.json |
| dat.raudenbush1985 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.riley2003 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.rivera2025 | 1 | Structural diagnostic 2x2 tables; cases versus noncases as groups, test positivity as outcome; not a treatment-effect interpretation |
| dat.roever2022 | 23 | Within-study dose cohort pairs; numerical 2x2 validation only, not randomized concurrent treatment contrasts |
| dat.senn2013 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.spooner2002 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.steurer2006 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.stowe2010 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.tannersmith2016 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.thompson1999 | 1 | Documented binary counts; mappings and source rows in corpus.json |
| dat.tian2009 | 2 | Documented binary counts; mappings and source rows in corpus.json |
| dat.ursino2021 | 19 | Within-study dose cohort pairs; numerical 2x2 validation only, not randomized concurrent treatment contrasts |
| dat.vanhowe1999 | 1 | Documented binary counts; mappings and source rows in corpus.json |
| dat.viechtbauer2021 | 1 | Documented binary counts; mappings and source rows in corpus.json |
| dat.white2020 | 0 | No documented two-group binary count structure; see inventory and package documentation |
| dat.woods2010 | 6 | Documented binary counts; mappings and source rows in corpus.json |
| dat.yusuf1985 | 6 | Documented binary counts; mappings and source rows in corpus.json |
