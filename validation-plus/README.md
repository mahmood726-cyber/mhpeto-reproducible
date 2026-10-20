# Extras validation for archive v1.1.0

PR #159 checks MH/Peto Q, Q p-values, I2 and H2; OR CMH, Tarone and
Breslow-Day; leave-one-out fits and significance crossing flags; and the
rare-event conventions table. It also checks the page's text claims about
R defaults. Native reference versions are R 4.6.0, metafor 5.2-1 and meta
8.5-0 (JSON uses 5.2.1 and 8.5.0); jsonlite 2.0.0 serializes the oracles.

The **2026-10-20 release run against allmeta 1cb3f84** measured
**120,000/120,010 (10 documented \`metabin-reml-refusal\`, 0 unexpected);
claims 3,793/3,793**.
See [release evidence](../provenance/run_plan-2026-10-20-release.log) and
[comparison summary](../rerun/v1.1.0/plus-comparison.json).
The identities, counts, input sizes and SHA-256 pins are in MANIFEST-plus.json.
Earlier candidate attempts are excluded from this archive.

From the archive root:

    node validation-plus/run-plus.mjs
    python analysis/recut_manifest.py --verify

The wrapper supplies the archived app's absolute index path to the unchanged
check-plus.mjs. It retains the generator, checker, manifest, README-plus.md and
plus-corpus files byte-for-byte. corpus/corpus.json is the unchanged original
corpus, copied to the relative location required by the checker. README-plus.md
and comparison-plus.json describe upstream runs, not a new archive run.
The Node check recomputes app values against stored R outputs; it does not run R.

Optional fresh R oracle generation, after the R environment lines in RUN_PLAN.cmd:

    Rscript validation-plus/regenerate-plus.R

This wrapper checks package versions and creates the layout expected by the
unchanged generate-plus.R under rerun/plus-oracle. It refuses an existing
directory and writes only fresh scratch references. Compare them with the pinned
oracle separately; do not overwrite the archive or regenerate upstream pins
to accept different values. The upstream generator says it enforces package
versions, but its implementation only prints them; the archive wrapper adds
the actual version guard. Standard RUN_PLAN.cmd replays the pinned oracle.

The original 68,461 checks and 106 tail checks remain separate and unchanged.
