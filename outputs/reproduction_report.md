# Reproduction report

Comparisons are recomputed from app and R records; expected numbers are assertions only.

Figure 2 plots per-quantity finite maxima (relative except p-values and rounded UI); undefined mismatches are triangles. Exact zeros and differences below 1e-16 are plotted at -16. All text is at least 8 pt; images are 300 dpi, nominal width 170 mm. Tables include all checks, including archived UI/refusal evidence.

| Element | Static / dynamic | Source |
|---|---|---|
| Tolerances and seven-defect classification | Static | bench/compare.py and historical report |
| Counts, differences, plots and verdicts | Dynamic | Full-precision records, analysis/checks.py |
| Expected totals | Static assertions | expected/paper_values.json |

PASS: 10/10 paper-value assertions; 68461/68461 final checks; 64256/68461 before fixes.
