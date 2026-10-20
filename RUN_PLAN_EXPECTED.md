# Expected second-pass results

Run RUN_PLAN.cmd from the archive root in Windows cmd. Every executable line
prints its label first and stops on error. Node, Python, Rscript, installed
Playwright with Chrome, matplotlib, Pillow and PyYAML must already be available.
No installation or download is performed by the plan. Before running, set
R_HOME to the installed R 4.6.0 directory (without the bin suffix), and set
R_LIBS_USER and R_LIBS to the libraries containing the required packages.
RUN_PLAN.cmd prepends %R_HOME%\bin to PATH and preserves the caller's library
variables; it disables user R environment files with R_ENVIRON_USER=NUL.
Console output should be retained; comparison and R logs go under rerun/v1.1.0.
RERUN_SHA256.json pins the release evidence in rerun/v1.1.0 only. The plan
preserves an existing verified replay in the sibling attempts directory before
preparing a fresh replay. No outputs are deleted or silently repinned.
After a new replay, its redacted RUN_LOG.txt and explicitly reviewed evidence
manifest must be finalized before the final integrity checks can pass.
The release replay completed on 2026-10-20 against allmeta 1cb3f84;
see [provenance/run_plan-2026-10-20-release.log](provenance/run_plan-2026-10-20-release.log).

| Label | Expected result |
|---|---|
| R PATH / R user library / R additional library / R environment / runtime note | Set the supplied environment; no validation count. |
| UTF-8 console | Python UTF-8 output; no validation count. |
| Verify prepared manifests | MANIFEST PASS and ORIGINAL INPUTS AND PLUS PINS PASS; all source/app hashes and oracle pins match. |
| Check native R versions | R PACKAGE VERSIONS PASS; metafor 5.2.1 and meta 8.5.0 (package spelling of 5.2-1 / 8.5-0), plus printed R/jsonlite versions. |
| Preserve previous replay | Verify release evidence, then preserve rerun/v1.1.0 in the sibling attempts directory with a unique numbered name; never overwrite or delete prior outputs. |
| Prepare original replay | Fresh scratch layout; original corpus, references and validate.R copied unchanged. Refuses an existing browser output to prevent silent resumption. The preceding preservation step supplies the clean state. |
| Replay original browser | 1,008/1,008 page configurations, zero browser errors. This is page coverage, not the statistical check count. Fresh results/app-patched.json under rerun/v1.1.0. |
| Compare original protocol | **68,461/68,461** and **106/106 tails**. bench/compare.py and analysis/checks.py must agree; unchanged denominators and tolerances. |
| Recompute original R validation | **68,461/68,461** and **106/106 tails**, against fresh release browser values. Recomputes native R fits; FI/FQ and DL oracle values are replayed as in v1.0.0. |
| Check extras and text claims | **120,000/120,010**, exactly **10 documented**, **0 unexpected**; CONTRACT PASS. Separate **3,793/3,793** claims and CLAIMS CONTRACT PASS. Exit 0 permits only the exact pinned documented failure identities. |
| Verify retained publication outputs | ARCHIVE PASS; **68,461/68,461** historical final checks, **106/106** tails, hashes, unchanged creator metadata, numerical ledgers, output images and reproducibility. This does not substitute for the fresh replay above. |
| Verify final manifests | Same manifest success as before execution; scratch outputs are excluded. |

The original baseline before seven fixes remains 64,256/68,461 in the historical
publication evidence. It is not a target for the new replay.
## Measured release run: 2026-10-20, allmeta 1cb3f84

| Release-run stage | Measured result |
|---|---|
| Browser coverage | 1,008 page configurations; 0 browser errors |
| Original browser-to-Python checks | 68,461/68,461; supplemental tails 106/106 (94 with absolute z at least 8) |
| Original browser-to-R checks | 68,461/68,461; supplemental tails 106/106 |
| Extras | 120,000/120,010; 10 documented failures, 0 unexpected; CONTRACT PASS |
| Text claims | 3,793/3,793; CLAIMS CONTRACT PASS |
| Retained publication checks | 10/10 paper-value assertions; 68,461/68,461 final checks; 64,256/68,461 before fixes |
| Integrity and outputs | ARCHIVE PASS (56 app hashes, 250 source hashes at execution); MANIFEST PASS |

Evidence: [provenance/run_plan-2026-10-20-release.log](provenance/run_plan-2026-10-20-release.log). The counts match the unchanged expected
contracts above and MANIFEST-plus.json. Release results are under rerun/v1.1.0;
earlier candidate attempts are excluded from the archive.

Release identifiers are 1cb3f8409c7af75ed41f7e1811f9c502f900fc79 and 10.5281/zenodo.23515177.
The upstream embedded build identity distinction is documented in RECUT_NOTES.md.

## Final Git-blob packaging

From the parent task folder, the human-side runner executes:

    FINAL_BLOBS.cmd

The command needs Git and Python on PATH and the sibling allmeta checkout.
It uses no machine-specific paths or network access. It checks that short
commit 1cb3f84 resolves to the full release SHA, restores all 65 mapped files
with binary-safe subprocess output, checks their bytes, prints BLOB PASS 65/65,
then runs the archive's own scripts:

    python analysis/recut_manifest.py --write
    python analysis/recut_manifest.py --verify

The helper rejects non-line-ending source changes and any change to an
immutable original input. Repeating it is safe. For a read-only final check,
run python finalize_blobs.py --verify-only from the parent task folder.
The full publication-output verifier remains:

    python analysis/verify_archive.py

Do not change original or plus oracle pins, expected values or tolerances.
The release log's ARCHIVE PASS establishes the numerical/output checks for
the release run; it is not a new verification of subsequent metadata edits.
