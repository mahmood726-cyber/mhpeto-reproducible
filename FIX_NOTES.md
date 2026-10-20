# Review fixes F1-F8

All paths below are relative to archive/. Only required review fixes were applied.
No corpus, oracle, expected value, tolerance, original protocol/evidence, app byte,
existing attribution or licence was changed. No .git access or public release action
was performed.

## F1

Replaced the unresolved extras count with measured 120,000/120,010 (10 documented metabin-reml-refusal, 0 unexpected); claims 3,793/3,793, and linked run 4 evidence. Removed stale execution-pending wording.

Locations: `validation-plus/README.md:9`, `RUN_PLAN_EXPECTED.md:31`, `RECUT_NOTES.md:92`.

## F2

Recorded the completed fresh browser-to-Python and browser-to-R results (68,461/68,461 plus 106/106 tails), extras and claims with evidence pointers. At this historical review stage, final allmeta SHA/DOI fields were still deferred; they are now resolved in current metadata.

Locations: `README.md:11`, `.zenodo.json:29`, `CITATION.cff:34`, `CHANGELOG.md:5`, `SOURCE_VERSION.json:8`, `RECUT_NOTES.md:104`.

## F3

Added Ahmad/Mahmood authors to the allmeta 1.8.0 reference (the three lines immediately before the version). Existing archive creator/authors and licence are unchanged.

Locations: `CITATION.cff:32`.

## F4

Replaced machine paths with caller-set R_HOME, R_LIBS_USER and R_LIBS, documented their use, and included .cmd in source hygiene. A planted Windows user path in RUN_PLAN.cmd raised the expected Machine path assertion; exact command bytes were restored and the gate passed. Since Pillow prevents importing the full verifier, the test compiled and executed the exact source-hygiene for-loop from verify_archive.py's AST with recut_manifest.sources and re; no substitute regex or weakened assertion was used.

Locations: `RUN_PLAN.cmd:2`, `RUN_PLAN_EXPECTED.md:7`, `analysis/verify_archive.py:19`.

## F5

Added the run log with only its three user-profile prefixes redacted. Pinned all seven required shipped evidence files and recorded hashes/byte sizes for the three large files (optional release payloads, verified when present). Both manifest modes and the full verifier call these evidence checks. Missing and tampered required summaries were rejected and restored. Evidence files are present in the working tree; staging/commit remains with the coordinator under the instruction not to touch .git.

Locations: `RERUN_SHA256.json:2`, `analysis/recut_manifest.py:19`, `README.md:26`, `RECUT_NOTES.md:129`, `rerun/v1.1.0/RUN_LOG.txt:1`.

## F6

Recorded Node 24.13.0, Playwright 1.59.1 / Chrome 155.0.8059.85, Python 3.13.13 / PyYAML 6.0.3, and R 4.6.0 / metafor 5.2-1 / meta 8.5-0 / jsonlite 2.0.0. Disclosed which versions were inspected after the run rather than printed in its log. Recorded the git-ignored node_modules junction, all four attempts, the fresh records behind the unchanged R banner, and that regenerate-plus.R was not executed.

Locations: `README.md:49`, `RECUT_NOTES.md:106`.

## F7

Documented the d04b0a9 Windows working tree, core.autocrlf=true, CRLF, 35/53 differences from raw git blobs, and upstream *.min.js binary treatment. Corrected the three EOL-only inventory rows to line endings only (LF to CRLF); disclosed the verifier's CRLF-to-LF preparation conversion. Confirmed all 53 app files still equal the candidate bytes.

Locations: `README.md:65`, `RECUT_NOTES.md:122`, `RECUT_NOTES.md:189`, `RECUT_NOTES.md:192`, `RECUT_NOTES.md:197`.

## F8

Ran --write followed by --verify successfully (PASS lines below). Invoked analysis/verify_archive.py, but it exited 1 before verification because Pillow's _imaging DLL could not initialize. A second installed Python (3.14.2) also failed to import Pillow. Full ARCHIVE PASS for this edited tree is NOT claimed; RUN_FIX.cmd records the outstanding command. The historical run 4 ARCHIVE PASS remains in RUN_LOG.txt as original evidence only.

Locations: `analysis/recut_manifest.py:75`, `RUN_FIX.cmd:3`.

## Recorded check output

The manifest commands were run in the required order from the archive root:

    python analysis/recut_manifest.py --write
    python analysis/recut_manifest.py --verify
    python analysis/verify_archive.py

Printed by --write and --verify:

```text
RUN EVIDENCE PASS: 7 required files; 3 large-file hashes recorded and checked when present
ORIGINAL INPUTS AND PLUS PINS PASS; app dependencies and webR package pins verified
```

Printed by --verify:

```text
MANIFEST PASS: app and archive inventories match
```

Additional actual checks during the fixes:

```text
MACHINE PATH NEGATIVE PASS: planted RUN_PLAN.cmd path rejected by the verifier's source-hygiene loop
MACHINE PATH RESTORED PASS: original command bytes restored; source-hygiene loop passes
RUN EVIDENCE MISSING NEGATIVE PASS: required summary absence rejected
RUN EVIDENCE TAMPER NEGATIVE PASS: changed summary rejected
APP BYTE EQUALITY PASS: all 53 app files match the candidate working tree
RUN LOG REDACTION PASS: only the three user-profile prefixes changed
CITATION AUTHORS PASS: all three references and archive attribution verified
```

Full-verifier error (exit 1; no current ARCHIVE PASS):

```text
ImportError: DLL load failed while importing _imaging: A dynamic link library (DLL) initialization routine failed.
```

No git/node/R command was required for these edits or rerun here. The previously
completed browser/R replay is supported by the shipped evidence, not claimed as
a new execution during review fixes. RUN_FIX.cmd contains the Python command
that remains blocked by this environment.

## Release follow-up

The later re-sync and Finalize section in RECUT_NOTES.md supersede this
historical review's deferred identity, build-stamp and numerical-replay status.
The final release log is provenance/run_plan-2026-10-20-release.log.
The publication runner performs FINAL_BLOBS.cmd from the parent task folder,
then the full Python archive verifier before staging, tagging and depositing.
No publication operation is performed by the finalization task.
