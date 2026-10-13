# Mantel-Haenszel and Peto meta-analysis in the browser: a tool validated against the R package metafor

Version 1.0.0. Creator: Ahmad, Mahmood. MIT archive code.
Allmeta commit: `7433ef7` (PR #105, squash-merged; seven fixes, direct upper-tail p-values and the Validate-in-R button); supplied source is the PR #105 fix on main 6036f3b6c1fd404b6da7916460faa8b3ebaf56bc. The archive app additionally includes this task's validation adapter/mount. No commit, push, deployment or Overmind certification is implied.

Reference environment: R 4.6.0, metafor 5.2-1, metadat 1.6-0, recorded in results/session.txt. Browser live R uses vendored webR 0.5.5 / metafor 4.8-0 and reports both versions. Package versions and source identifiers are supplied local evidence, not independently verified remote release claims.

The full primary comparison passes **68,461/68,461 checks after seven fixes**, versus **64,256/68,461 before fixes**. These are full-precision, rounded UI, fragility, L'Abbe and structural checks, not 68,461 independent statistical estimates. analysis/checks.py preserves bench/compare.py's check contract and derives the full ledger from recorded app/R values. See outputs/table1_by_quantity.csv for before/after counts per quantity and measure.

## Validate with one command

With R and existing installed metafor and jsonlite packages, from this folder:

    Rscript validate.R

No network, Python, Node or browser is needed. Set R_LIBS_USER / R_LIBS to your installed libraries if necessary. The command refits every configuration with rma.mh and rma.peto, recomputes ancillary study effects and inverse-variance L'Abbe references, compares them with results/app-patched.json, prints per-quantity totals and N/N checks pass, and writes outputs/validate_R_table.csv. Missing dependencies, incomplete scope and failures exit nonzero. Actual versions are printed.

Replayed rather than recomputed: browser outputs and rounded UI/structural evidence are archived; the independent R greedy FI/FQ and DL baseline records are replayed from results/fragility-reference.json. This command does not run a browser or the lengthy greedy search. Its per-row Mode field identifies that distinction. bench/fragility-reference.R retains the independently executed oracle, including initial/final metafor checks (these are provenance, not additional primary checks).

## Corpus and methods

The corpus is drawn from documented metadat tables supplying valid nonnegative integer 2x2 cells and nonempty arms. Explicit column mappings, source row indices, outcome/comparison splits, duplicate-arm regroupings, missing/fractional/invalid exclusions and dataset dispositions are archived in data/ and bench/build.R. No simulated rows are added. Repeated configurations and multi-arm pairings are computational cases, not independent trials. Table 2 includes excluded datasets with zero configurations and reasons.

MH settings: rma.mh(ai,bi,ci,di,measure=OR/RR/RD,add=c(0.5,0),to=c("only0","none"),drop00=c(FALSE,FALSE),correct=FALSE). Peto: rma.peto(ai,bi,ci,di,add=0,to="none",drop00=TRUE). Counts are converted to R doubles, preserving integer values and preventing the integer overflow encountered in three O'Brien Peto reference fits. The original erroneous reference is retained in results/reference-integer-overflow.json; this harness correction is not one of the seven app defects.

Full-precision tolerance: abs(App-R)/max(1,abs(R)) <= 1e-9, with absolute difference for p. Rounded UI tolerance is absolute 0.0005000001 (three decimals) or 0.0050000001 (two-decimal z). Null matches null only. Beta/SE are recovered algebraically from full-precision exported estimates and confidence limits. The tables retain finite maxima and undefined mismatches separately.

## Seven app fixes

1. RD variance changed from weighted binomial variance to Greenland-Robins.
2. Low-accuracy normal CDF replaced for p-value agreement.
3. Zero-cell RR study effects use corrected arm totals.
4. Export identifies MH and Peto by method name when MH is undefined.
5. DL fragility intervals use the exact normal quantile.
6. Single-row refusal clears previously visible results.
7. Diagnostic labels explicitly identify the separate DL and inverse-variance models.

The overall improvement is 64,256 to 68,461 passing checks out of 68,461. Label corrections are not separate numerical tests and defect-specific counts would overlap; the per-quantity table provides the measured breakdown. bench/fix.patch and results/HISTORICAL_RESULTS.md retain the original detailed findings.

## Limits

No CMH, Tarone, Breslow-Day, Q or I2 statistics are displayed or validated for MH/Peto. Displayed k counts input rows. Fragility is a DL random-effects greedy index, not a proven global minimum. L'Abbe uses an inverse-variance fixed-effect estimate (RR when selected, OR otherwise), not MH/Peto. Hart's person-time data were treated as counts solely for numerical coverage. O'Brien BMI rank groupings, Frank genotype dichotomy, diagnostic-case comparisons and dose-cohort pairs retain the supplied corpus interpretations; computational regroupings are not clinical analyses. See the historical report for all inclusion qualifications and warning/error records.

## Rebuild and verify the archive

    python analysis/make_outputs.py
    python analysis/verify_archive.py

Python requires matplotlib, Pillow and PyYAML. Expected values are assertions, never substituted for computed findings. Outputs include both CSV tables, before/after check ledgers, figure2_agreement and visual_abstract in PNG/TIFF (300 dpi, 170 mm, minimum 8 pt), dimensions, numerical provenance and reproduction_report.md.

app/ contains byte-identical files from the supplied allmeta worktree after adding validation, including dynamically fetched webR runtime and metafor dependency archives. app/app-sha256.json pins the complete snapshot. SOURCE_SHA256.json pins archive source files, excluding generated outputs, caches, rerun/, git metadata and itself. Browser test request logs establish fetched asset coverage. No manuscript drafts are included and the verifier permits .git.

| Element | Static / dynamic | Source |
|---|---|---|
| Models, tolerances, mappings and seven-defect classification | Static protocol | bench scripts and historical report |
| Corpus and reference records | Static recorded evidence | supplied final run and source-row mappings |
| Fits in validate.R | Dynamic | installed metafor, current execution |
| Publication counts, differences and plots | Dynamic | comparison of full-precision records |
| Browser Tier 2 app values | Dynamic | current page parser, engine and DOM |
| Tier 2 independent R oracle | Replayed recorded evidence | hash-pinned reference files |

Derived from https://github.com/mahmood726-cyber/allmeta and allmeta v1.2.1 DOI 10.5281/zenodo.23288388 (isDerivedFrom). These are supplied identifiers. The MIT license covers archive code; vendored R, packages, data and documentation retain their upstream licenses and attribution.

Final-page tail regression guard: in addition to the unchanged 68,461 primary checks, every pooled R p-value below 1e-12 is checked with abs(App-R)/abs(R) <= 1e-9. If R underflows to zero, only an app zero matches. Supplemental checks are reported separately; the original primary denominator is unchanged. The final page uses direct normal upper-tail probabilities. Browser Tier 2, bench/compare.py and validate.R enforce this guard. outputs/tail_checks.json and outputs/validate_R_tails.csv record Python and recomputed-R evidence.
