# Recut notes: paper 10, archive v1.1.0

Finalized on 2026-10-20 for archive v1.1.0 against allmeta v1.8.0,
commit `1cb3f8409c7af75ed41f7e1811f9c502f900fc79`, DOI 10.5281/zenodo.23515177
(concept DOI 10.5281/zenodo.20516880).
The release RUN_PLAN.cmd execution passed on 2026-10-20 against allmeta 1cb3f84.
See the Finalize section for the current results, packaging status and privacy audit.

The preparation and review records below are historical: d04b0a9 was the
earlier snapshot. Earlier candidate attempt files are excluded from this archive.
The re-sync and Finalize sections supersede their earlier source/build status.

## How the archive is built and verified

The original bench/build.R enumerates documented metadat tables, applies the
recorded mappings/exclusions, and writes the corpus and audit files. It calls
bench/reference.R for metafor MH/Peto fits, study effects and inverse-variance
L'Abbe references. bench/fragility-reference.R supplies the independent greedy
DL FI/FQ oracle. bench/run-app.cjs runs the actual page in Playwright/Chrome for
336 configurations x OR/RR/RD = 1,008 page configurations. bench/compare.py
compares those values with the recorded R oracle; analysis/checks.py exposes
the same contract and the separate relative p-value tail guard.

bench/finalize.py and make-fix.py are historical build/patch provenance, with
old checkout assumptions and path placeholders; they are not the recut
manifest generator. bench/docs.R and inspect.R produce dataset documentation,
inventory, source and environment records; split-reference.py records the
historical harness extraction. No corpus or oracle generator is run during
the recut. Original data/, expected/, bench/, results/, outputs/, validate.R,
analysis/checks.py and in-app corpus/reference JSON are byte-identical to the
starting archive. ORIGINAL_INPUTS_SHA256.json pins these 176 files.

validate.R refits native R models against results/app-patched.json; it replays
the existing FI/FQ/DL oracle and archived browser/UI evidence. It alone does
not exercise a new app snapshot. RUN_PLAN.cmd therefore first captures fresh
browser evidence, then compares it with both original Python implementations,
then runs the unchanged R validator on those fresh records in rerun/v1.1.0.
The original numerical target is 68,461/68,461 plus 106/106 tail checks.
Existing results/ and outputs/ are historical evidence, not recut results.

analysis/make_outputs.py reconstructs ledgers, tables, counts, provenance and
publication PNG/TIFF images from the recorded values. analysis/verify_archive.py
checks inventories, primary input pins, historical request-path coverage,
reproducible outputs, numerical ledgers, images, metadata and creator identity.
Its numerical assertions and tolerances remain unchanged; only release metadata
and additional recut pin verification were updated.

No supported Python SOURCE_SHA256.json generator existed in v1.0.0.
analysis/recut_manifest.py now regenerates app/app-sha256.json and
SOURCE_SHA256.json with --write, and verifies them with --verify.
The source inventory retains the existing exclusions: outputs, rerun, caches,
node_modules, git metadata, temporary .verify-* directories, SOURCE_SHA256.json
itself and PROGRESS.md. Original and extras pins are checked before regeneration;
upstream MANIFEST files are never rewritten to accept different reference data.

## App identity and dependency coverage

Every previously archived app file was copied from the matching candidate path,
including unchanged files and the existing webR runtime/package archives.
No previously archived source path was absent; no app file was removed.
The candidate page's script src and link href dependencies were parsed, then
literal import/fetch/configured resource and new URL paths were followed through
shared JavaScript. APP_DEPENDENCIES.json records 33 resolved literal edges.
The new required files are analysis-lifecycle.js, plot-export.js and its lazy
vendor/jspdf.min.js dependency.

The dynamic chain alm-validate.js -> webr-runner.js -> local webr.mjs and its
runtime assets is retained. The MH/Peto live-R adapter requests metafor only.
Its nine repository package archives, including transitive dependencies,
were checked against the updated runtime manifest for bytes and SHA-256.
Other apps' packages listed in that shared manifest are not needed by MH/Peto.
Historical browser request logs are preserved as old path-coverage evidence.

At that preparation stage, app/app-sha256.json pinned the d04b0a9 bytes. SOURCE_VERSION.json,
README.md, CITATION.cff and .zenodo.json identify the intended release.
Historical v1.0.0 commit references, results/source-hashes.json, combined-results
metadata and bench/finalize.py remain labelled historical provenance.

At that preparation stage, supplied shared/build-info.js reported v1.7.0 and an older build SHA.
It was copied byte-for-byte as required, not rewritten into a fictitious v1.8.0
build. Exported receipts can therefore carry that old embedded identity.
The later release re-sync and replay resolved this version discrepancy;
the embedded build SHA still differs from the release SHA, as recorded below.

## Extras and execution status

All eight upstream extras files were copied without modification: README-plus.md,
MANIFEST-plus.json, check-plus.mjs, generate-plus.R and the four plus-corpus JSON
files. corpus/corpus.json is an additional byte-identical original-corpus copy
at the relative path the checker expects. run-plus.mjs supplies the archived
index path using the supported --index option. regenerate-plus.R creates the
generator's expected layout only in scratch and enforces metafor/meta versions.
The upstream generator's header claims a version guard, but its body only
prints versions; the archive wrapper supplies the missing guard.

Measured extras: 120,000/120,010 (10 documented `metabin-reml-refusal`,
0 unexpected); claims 3,793/3,793. This is a historical candidate result.
The optional R regeneration command never overwrites the pinned oracle.

Completed here: app and extras byte equality against the supplied candidate;
unchanged original evidence; all original/plus hashes and byte sizes; app
dependency and nine webR package pins; source-text hygiene; Python syntax;
JSON metadata parsing, CFF text inspection, version/date and unchanged creators; scratch staging; and
historical numerical recomputation (64,256/68,461 before fixes,
68,461/68,461 after fixes, 106/106 tails). Scratch staging was cleaned afterwards.
Manifests were regenerated and verified with Python.

Fresh browser-to-Python and browser-to-R checks passed 68,461/68,461 plus 106/106 tails; extras measured 120,000/120,010 (10 documented metabin-reml-refusal, 0 unexpected), with claims 3,793/3,793. Historical candidate result only; earlier attempt files are excluded from this archive.

Run 4 environment: Node 24.13.0; Playwright 1.59.1 with Google Chrome
155.0.8059.85 (the runner selects channel 'chrome'); Python 3.13.13 and
PyYAML 6.0.3; R 4.6.0, metafor 5.2-1, meta 8.5-0 and jsonlite 2.0.0.
R/package versions are printed in RUN_LOG.txt:14-18. Node's executable version,
the installed Chrome version directory, Python runtime and Python/Playwright
package metadata were inspected during review fixes; those versions were not
captured by the original run log. Playwright was provided through a git-ignored
node_modules junction.
Four attempts were needed: run 1 lacked Playwright; run 2 reached 68,461/68,461
before stopping for missing PyYAML; run 3 refused to resume a partial replay;
run 4 passed. None of runs 1-3 stopped for a numerical failure.
validate.R's unchanged "Replayed: archived browser numerical outputs" banner
refers here to the fresh rerun/v1.1.0/results/app-patched.json records because
the R validator ran with rerun/v1.1.0 as its working directory.
The optional regenerate-plus.R was not executed; extras used the stored R oracle.

App bytes equal the allmeta d04b0a9 Windows working tree with
core.autocrlf=true: 49 of 53 app files contain CRLF, and 35 of 53 differ from
raw git blobs. Upstream .gitattributes treats *.min.js as binary.
The url-state.js, validate/MANIFEST.json and diagnostic-plots.js refreshes
changed line endings only (LF to CRLF). analysis/verify_archive.py was converted
from CRLF to LF during preparation.

RERUN_SHA256.json pins RUN_LOG.txt (the original run_plan.log with the three
user-profile prefixes on lines 11-13 redacted) and six small summaries:
compare.log, validate-R.log, plus-comparison.json, results/comparison.json,
results/comparison.tails.json and results/app-patched-browser-errors.json.
It records SHA-256 and byte sizes for results/app-patched.json,
results/check-ledger.json and outputs/validate_R_table.csv; these large files
are optional release payloads, verified when present. The evidence manifest
is itself included in SOURCE_SHA256.json and is checked by verify_pins even
during --write, so source regeneration cannot silently repin run evidence.

## Resolved identifiers and historical redaction markers

The allmeta release SHA and DOI fields are now 1cb3f8409c7af75ed41f7e1811f9c502f900fc79 and
10.5281/zenodo.23515177. All release identifier placeholders have been replaced.
Extras and claims are resolved at 120,000/120,010 and 3,793/3,793.

Historical `<ALLMETA_ROOT>` and `<R_LIBS_USER>` markers are intentional
redactions in bench/finalize.py, bench/make-fix.py, bench/run-app.cjs,
bench/README.md, results/HISTORICAL_RESULTS.md and the historical file-picker
request log. `<USERPROFILE>` in the historical run log and `<LOCAL>` in
the release log are intentional privacy markers. They cannot be filled with
local paths in the publication. No unresolved release count remains.

## Complete source change inventory

Paths below are relative to archive/. Unchanged files were also refreshed from
the candidate where required. Generated caches and temporary staging are not
release sources. No source files were removed.

| Status | Path | Reason |
|---|---|---|
| Changed | .zenodo.json | Version, new scope and v1.8.0 related identifier; existing creators and links retained. |
| Added | APP_DEPENDENCIES.json | Resolved recursive literal dependencies and dynamic webR package closure. |
| Changed | CHANGELOG.md | Dated v1.1.0 entry. |
| Changed | CITATION.cff | Version 1.1.0, release date and resolved allmeta v1.8.0 reference; existing authors retained. |
| Added | ORIGINAL_INPUTS_SHA256.json | Pin 176 original protocol/evidence files without altering their values. |
| Changed | README.md | Release changes, fresh replay commands, historical/current scope and identity. |
| Added | RECUT_NOTES.md | Build/provenance review, complete change list, placeholders and measured results. |
| Added | RUN_PLAN.cmd | Exact labelled Windows second-pass commands and supplied R environment. |
| Added | RUN_PLAN_EXPECTED.md | Expected counts per command and execution limitations. |
| Changed | SOURCE_SHA256.json | Regenerated source inventory. |
| Added | SOURCE_VERSION.json | Separate final release identity from historical preparation identity. |
| Added | analysis/check-r-versions.R | Enforce metafor 5.2-1 and meta 8.5-0 before execution. |
| Added | analysis/recut_manifest.py | Portable inventory regeneration and original/plus/dependency pin verification. |
| Added | analysis/recut_runner.py | Fresh scratch preparation, original comparison and unchanged native R replay. |
| Added | analysis/replay-app.cjs | Path-only copy of original browser runner; refuses resuming old output. |
| Changed | analysis/verify_archive.py | v1.1.0 metadata expectations and recut pin checks; original numerical assertions retained. |
| Changed | app/app-sha256.json | Regenerated candidate app inventory. |
| Added | app/hub/shared/analysis-lifecycle.js | New page or recursively loaded shared-script dependency. |
| Changed | app/hub/shared/chart-download.js | Byte-identical candidate app refresh. |
| Changed | app/hub/shared/csv-upload.js | Byte-identical candidate app refresh. |
| Added | app/hub/shared/plot-export.js | New page or recursively loaded shared-script dependency. |
| Changed | app/hub/shared/url-state.js | line endings only (LF→CRLF). |
| Added | app/hub/shared/vendor/jspdf.min.js | New page or recursively loaded shared-script dependency. |
| Changed | app/mh-peto/index.html | Byte-identical candidate app refresh. |
| Changed | app/mh-peto/validate/MANIFEST.json | line endings only (LF→CRLF). |
| Changed | app/mh-peto/validate/adapter.js | Byte-identical candidate app refresh. |
| Changed | app/r-shiny/shinylive/webr/repo/manifest.json | Byte-identical candidate app refresh. |
| Changed | app/shared/alm-validate.js | Byte-identical candidate app refresh. |
| Changed | app/shared/build-info.js | Byte-identical candidate app refresh. |
| Changed | app/shared/diagnostic-plots.js | line endings only (LF→CRLF). |
| Changed | app/shared/ma-comparisons-v1.js | Byte-identical candidate app refresh. |
| Changed | app/shared/ma-core.js | Byte-identical candidate app refresh. |
| Added | validation-plus/MANIFEST-plus.json | Byte-identical upstream PR #159 extras evidence or script. |
| Added | validation-plus/README-plus.md | Byte-identical upstream PR #159 extras evidence or script. |
| Added | validation-plus/README.md | Archive extras scope, package versions, commands and measured counts. |
| Added | validation-plus/check-plus.mjs | Byte-identical upstream PR #159 extras evidence or script. |
| Added | validation-plus/corpus/corpus.json | Unchanged corpus at the relative path required by upstream scripts. |
| Added | validation-plus/generate-plus.R | Byte-identical upstream PR #159 extras evidence or script. |
| Added | validation-plus/plus-corpus/claims-plus.json | Byte-identical upstream PR #159 extras evidence or script. |
| Added | validation-plus/plus-corpus/comparison-plus.json | Byte-identical upstream PR #159 extras evidence or script. |
| Added | validation-plus/plus-corpus/reference-plus.json | Byte-identical upstream PR #159 extras evidence or script. |
| Added | validation-plus/plus-corpus/versions-plus.json | Byte-identical upstream PR #159 extras evidence or script. |
| Added | validation-plus/regenerate-plus.R | Optional native R oracle generation in scratch with version checks. |
| Added | validation-plus/run-plus.mjs | Supply the archived page path to unchanged upstream checker. |

Preparation inventory before review fixes: 25 added, 19 changed, 0 removed source files.
Review additions and edits are recorded per F1-F8 in FIX_NOTES.md.


## Re-sync to allmeta v1.8.0 (1cb3f84)

Re-synced from the supplied read-only allmeta working tree at
1cb3f8409c7af75ed41f7e1811f9c502f900fc79. Git was not invoked.
The release commit and DOI are now resolved in current metadata and source provenance.

Compared all 53 existing upstream app copies and all nine upstream
validation-plus copies byte-for-byte against their matching allmeta paths.
Only three existing copies differed. All nine extras copies were identical:
the eight plus files and the supporting corpus/corpus.json. Archive-authored
validation-plus/README.md, run-plus.mjs and regenerate-plus.R are not upstream
copies; the README was updated only to distinguish candidate and release runs.

Re-parsed mh-peto/index.html script/link attributes and configured resources,
then recursively scanned loaded shared JS/CSS for literal resource paths,
including import/fetch/new URL dependencies. APP_DEPENDENCIES.json records
35 resolved literal edges (including conservative documentation references)
and three explicit dynamic glossary edges. Reviewed the dynamic webR base,
existing runtime/worker/library assets, and nine manifest-pinned metafor
package dependencies. The optional es/ar/zh glossary URLs are constructed by
tooltips.js; those three files were missing from the earlier archive and
have now been added. There are 56 upstream app copies after the re-sync.

Every copied or added upstream file is listed below. Paths are relative to
archive/; hashes are SHA-256 of the actual bytes, including line endings.
Copies used read_bytes/write_bytes without decoding or re-encoding.

| Path | SHA-256 before -> after | Why |
|---|---|---|
| app/hub/shared/results-export.js | `8fd30b46fc6e0d09b98326f69edf14757659dbcf2cf1434ca8c5de60c057cc71` -> `16ffa76bc74275565214c2e142d7f0d0847a5a8eded2614efb04aa172acd71f4` | Upstream export-bar CSS wrapping and maximum width. |
| app/shared/alm-validate.js | `3de6a685c77fa26d68ae39b1da9619c5ada49fd22ef5170237268e1401a09fb7` -> `b451c1377164842466aa0d7ad4cb6dd7a1340456a61e891a01646b4375c4ed87` | Upstream live-R version-label formatting; no comparison logic changes. |
| app/shared/build-info.js | `f75a435e283d007883ce8fb2f66da7a1cf6132cd5a391a57419b137a69c9c238` -> `44c8a7d1e2cdad4d4b1c4806cffdd4f9817dc39161cd0de5374761a71bd19177` | Upstream v1.8.0 build version, embedded SHA and timestamp. |
| app/hub/shared/glossary.es.json | `absent` -> `d529dd603967580e038d5b272c794822de934bacb2363a36e3ad7d6b36df82d1` | Language-selectable glossary fetched dynamically by tooltips.js; missing from earlier snapshot. |
| app/hub/shared/glossary.ar.json | `absent` -> `0efb4eb408dc876da85c836b46d4fc6a92a43220027e1daf9cb5e18eddfff676` | Language-selectable glossary fetched dynamically by tooltips.js; missing from earlier snapshot. |
| app/hub/shared/glossary.zh.json | `absent` -> `896ec12cd34bfd7d2a37ec45b5318e716328d9a614b71aec25638515f0457034` | Language-selectable glossary fetched dynamically by tooltips.js; missing from earlier snapshot. |

No files were removed. All other app files, including mh-peto/index.html,
the validation adapter, original corpus and R references, are byte-identical
to both the prior archive and supplied release. shared/stats-qt.js,
shared/canonical-datasets.js and shared/hero-examples.js are neither held by
this MH/Peto archive nor loaded through its dependency graph, so they were
not copied merely because they changed elsewhere in allmeta.

Numerical impact: none of the three recopied files changes model calculations,
validated inputs, expected values, tolerances, or comparisons. results-export.js
changes only CSS; alm-validate.js changes only the displayed R version string;
build-info.js changes receipt provenance. The added glossaries change translated
help text only. No copied change is expected to alter a validated number.
The runner's authoritative release replay completed on 2026-10-20 against
allmeta 1cb3f84: 68,461/68,461 plus 106/106 tails; extras 120,000/120,010
(10 documented, zero unexpected); claims 3,793/3,793. The earlier d04b0a9
run has the same totals and remains separately preserved.
All original protocol inputs and extras expected counts remain unchanged.

The upstream build stamp now reports version v1.8.0, embedded SHA
42a94da2110a02200d0b5bff4c56f636b9cbffa9 and builtAt
2026-10-20T20:32:27Z. That embedded SHA is different from the supplied
release commit 1cb3f84. It is preserved exactly, not rewritten. The previous
v1.7.0 stamp described above applies only to the candidate preparation.

RUN_PLAN.cmd includes a preservation command before Prepare original replay.
The preservation helper now verifies the release evidence and moves an existing
replay to a unique numbered directory under the sibling attempts directory,
outside the published archive. It never deletes or overwrites prior outputs.
The optional plus-oracle regeneration remains separate; no corpus/oracle
regeneration was added.

analysis/recut_manifest.py checks RERUN_SHA256.json against rerun/v1.1.0 only.
The manifest now pins the 2026-10-20 release run against allmeta 1cb3f84.
A future replay requires explicit review and finalization of its redacted log
and evidence manifest before final integrity checks; hashes are never silently
updated to accept new results. Historical candidate run links in earlier
review records are superseded by the release evidence documented below.

Archive-authored changes in this re-sync:

- APP_DEPENDENCIES.json: refreshed dependency audit and supplied release provenance.
- SOURCE_VERSION.json: supplied release commit, actual build stamp and retained
  historical result; finalization now records the completed release replay.
- README.md, RUN_PLAN_EXPECTED.md and validation-plus/README.md: current source,
  release replay and preservation instructions; expected counts unchanged.
- RUN_PLAN.cmd: the one preservation command described above.
- analysis/recut_runner.py: preservation action with numbered collision avoidance
  and resolved path checks confining backups to the sibling attempts directory.
- analysis/recut_manifest.py: release evidence location handling and checks for
  the added dynamic dependencies; original pins and numerical assertions unchanged.
- RECUT_NOTES.md: this audit and clarification that earlier results are historical.
- app/app-sha256.json and SOURCE_SHA256.json: regenerated by the archive's own
  python analysis/recut_manifest.py --write, followed by --verify.

Python checks completed: 56 app copies and nine upstream extras copies match
allmeta byte-for-byte; all 176 original input pins, original/plus manifest
hashes and byte sizes, nine webR package pins and historical run evidence pins
pass. Expected counts, original tolerances and creators are unchanged;
finalization subsequently resolved both coordinator identifiers. Changed Python modules compile. An isolated
scratch test exercised first-run preservation, an occupied backup name,
preserving a partial later attempt, absence of an active folder, and rejection
of tampered historical evidence before any rename. No real outputs were moved.


Final local verification: source text hygiene and JSON parsing passed. Removing
the sole added preservation line from RUN_PLAN.cmd reproduces the original
plan's SHA-256 exactly. The full analysis/verify_archive.py attempt could not
start because Pillow's _imaging native DLL cannot initialize in this sandbox.
Its existing RUN_PLAN.cmd stage remains unchanged for the external runner.
That earlier sandbox attempt did not establish reproducibility. The subsequent
2026-10-20 release log records ARCHIVE PASS and the fresh release numerical pass.
The first scratch-test attempt also hit the Windows restrictive ACL applied
by Python TemporaryDirectory; the successful isolated test used a normal
mkdir scratch directory instead and cleaned its test contents afterwards.

The regenerated app and source inventories passed --verify, including all
original, extras, dependency and historical evidence pins. The failed initial
TemporaryDirectory test left an empty resync-test-spqyzr94 directory outside
archive/; Windows denied its removal. It contains no validation outputs and
is excluded from the archive entirely. All other task scratch files were removed.

## Finalize

Finalization date: 2026-10-20. Release run: 2026-10-20 against allmeta v1.8.0,
1cb3f8409c7af75ed41f7e1811f9c502f900fc79 (1cb3f84).
Upstream release DOI: 10.5281/zenodo.23515177; concept DOI:
10.5281/zenodo.20516880.

### Changes and measured results

- Replaced every allmeta release SHA/DOI placeholder in metadata and notes.
  CITATION.cff and .zenodo.json remain version 1.1.0; CFF release date is
  2026-10-20. Creator and reference author lists are unchanged.
- README.md, RUN_PLAN_EXPECTED.md, validation-plus/README.md, CHANGELOG.md,
  SOURCE_VERSION.json and APP_DEPENDENCIES.json now distinguish the completed
  release run from the historical d04b0a9 preparation. FIX_NOTES.md points to
  this final audit. Historical descriptions remain labelled as historical.
- Copied archive/../run_plan.log to provenance/run_plan-2026-10-20-release.log.
  Only the three profile prefixes on lines 11, 12 and 13 were replaced with
  the literal redaction marker followed by a backslash. Every other byte,
  including CRLF line endings and all numerical output, is unchanged.
- Added parent-folder COPY_MAP.json (56 app files and 9 validation-plus copies),
  finalize_blobs.py and FINAL_BLOBS.cmd. The helper resolves the pinned commit,
  fetches all blobs before writing, refuses non-line-ending differences or
  immutable-input changes, writes binary bytes and verifies each copy, prints
  BLOB PASS 65/65, then calls recut_manifest.py --write and --verify.
  Its --verify-only mode checks blobs and manifests without rewriting.
  No Git, Node or R executable was invoked during this finalization.
- Regenerated app/app-sha256.json and SOURCE_SHA256.json using the archive's
  own script. Original-input pins, historical replay pins, expected values,
  tolerances, corpus, reference records and publication outputs are unchanged.
- RUN_PLAN.cmd already obtains R paths from R_HOME, R_LIBS_USER and R_LIBS.
  It contains no machine-specific paths and was left byte-identical.
  RUN_PLAN_EXPECTED.md documents those variables and executable dependencies.

| Release-run stage | Measured result |
|---|---|
| Browser coverage | 1,008 page configurations, 0 browser errors |
| Python comparison | 68,461/68,461; 106/106 supplemental tails; 94 with absolute z at least 8 |
| Native R comparison | 68,461/68,461; 106/106 supplemental tails |
| Extras | 120,000/120,010; 10 documented failures, 0 unexpected; CONTRACT PASS |
| Text claims | 3,793/3,793; CLAIMS CONTRACT PASS |
| Historical paper assertions | 10/10; 68,461/68,461 final; 64,256/68,461 before fixes |
| Run integrity | ARCHIVE PASS: 56 app hashes, 250 source hashes at execution; MANIFEST PASS |

These counts are transcribed from provenance/run_plan-2026-10-20-release.log.
README numerical differences from the release log: **none**. Corrected the
run attribution, obsolete pending status and evidence links, without changing
any expected value, tolerance, corpus or count. The run-time inventory count
is historical; the finalized source inventory also includes the new log.

### Verification and remaining publication steps

The JSON/CFF metadata parse, version/date checks and unchanged creator checks
pass. The 65-copy map is complete and every current copy equals its supplied
upstream working-tree file. The helper's isolated Python tests pass for CRLF
restoration, unchanged binary bytes, repeat execution, read-only verification,
content-mismatch refusal, immutable-input refusal and path confinement.
These are helper tests, not an actual Git BLOB PASS.

The archive's manifest regeneration and verification pass, including all 176
original input hashes, upstream original/plus manifests, nine webR package
pins, dependency coverage and the preserved historical replay pins.
The full analysis/verify_archive.py cannot start in this sandbox because
Pillow's native imaging DLL fails to initialize. The release run's full
ARCHIVE PASS is retained as execution evidence; no new full-verifier pass
for this metadata-edited tree is claimed.

Before publication, the human-side runner must execute FINAL_BLOBS.cmd from
the parent task folder, then python analysis/verify_archive.py from archive/.
The current checkout retains the CRLF upstream working-tree bytes until the
blob helper succeeds. No commit, tag or public deposit was performed.

The archive v1.0.0 DOI was not supplied and is not present in the local
metadata. The existing 10.5281/zenodo.23288388 is explicitly labelled allmeta
v1.2.1, so it was retained as isDerivedFrom and not relabelled as the archive
v1.0.0 DOI. The requested prior-archive-version DOI relation remains unresolved
pending that identifier; the current allmeta v1.8.0 DOI relation is populated.
No DOI was invented.

Remaining angle-bracket strings are intentional historical redaction markers
listed above, the numbered backup marker in run-plan documentation, markup,
R diagnostic strings (including its internal FIXME marker), or encoded
characters in retained dataset documentation. No release SHA, DOI or numerical
count placeholder remains. The missing prior-version DOI is stated explicitly
rather than represented by a fabricated identifier.

### Publication privacy audit

Scanned every non-ignored archive file, including rerun/, outputs/, binary
runtime assets and dependency archives, for the requested path, identity,
email and credential patterns. Git metadata is not a publication file.
The only ignore rules are the existing cache directories, bytecode files,
PROGRESS.md and node_modules. Source manifests exclude additional generated
directories, but this privacy scan does not.

The three private profile prefixes in the incoming release log were redacted.
No other local account/host identity or apparent credential was identified.
Broad matches also include public creators and repository attribution,
third-party author contact notices, standard environment variables, ordinary
UI/runtime words, the webR virtual filesystem home, and accidental credential
prefix substrings in prose or compressed bytes. These are listed below with
their dispositions; substring matches alone are not credentials.

Public attribution, third-party contact notices, functional runtime strings,
and unchanged dataset documentation have been retained to preserve the
task's creator, upstream-blob and immutable-evidence requirements. Clarification
was requested about the conflict with literal removal of every email/path
match; no answer had arrived at finalization. Therefore this is an explicit
exception audit, not a claim that every broad pattern has been erased.
Removing upstream contact notices would violate exact blob identity and would
be reversed by FINAL_BLOBS.cmd; changing the virtual home strings would alter
the runtime. No private email address or actual key was found.

The audit below groups repeated matches on the same file and line, with a
count covering every occurrence. Binary-file lines count raw newline bytes.
Rows for excluded candidate attempts have been removed. Remaining locations
refer to the finalization tree before the blob-copy runner; CRLF
restoration does not change line numbers. Audit descriptions intentionally
avoid reproducing contact addresses or private path text.

| File:line | What | Matches | Action |
|---|---|---:|---|
| provenance/run_plan-2026-10-20-release.log:11 | Private profile prefix in incoming log | 1 | Replaced prefix; retained all remaining bytes. |
| provenance/run_plan-2026-10-20-release.log:12 | Private profile prefix in incoming log | 1 | Replaced prefix; retained all remaining bytes. |
| provenance/run_plan-2026-10-20-release.log:13 | Private profile prefix in incoming log | 1 | Replaced prefix; retained all remaining bytes. |
| .zenodo.json:5 | Public creator or repository attribution | 1 | Retained: creator identity and public provenance. |
| .zenodo.json:14 | Public creator or repository attribution | 1 | Retained: creator identity and public provenance. |
| CITATION.cff:7 | Public creator or repository attribution | 1 | Retained: creator identity and public provenance. |
| CITATION.cff:16 | Public creator or repository attribution | 1 | Retained: creator identity and public provenance. |
| CITATION.cff:17 | Public creator or repository attribution | 1 | Retained: creator identity and public provenance. |
| CITATION.cff:23 | Public creator or repository attribution | 1 | Retained: creator identity and public provenance. |
| CITATION.cff:31 | Public creator or repository attribution | 1 | Retained: creator identity and public provenance. |
| FIX_NOTES.md:22 | Public creator or repository attribution | 1 | Retained: creator identity and public provenance. |
| FIX_NOTES.md:28 | Generic word or runtime/environment identifier | 2 | Retained: functional identifier, ordinary text or prior redaction marker. |
| FIX_NOTES.md:34 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| FIX_NOTES.md:85 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| LICENSE:3 | Public creator or repository attribution | 1 | Retained: creator identity and public provenance. |
| README.md:3 | Public creator or repository attribution | 1 | Retained: creator identity and public provenance. |
| README.md:76 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| README.md:123 | Public creator or repository attribution | 1 | Retained: creator identity and public provenance. |
| RECUT_NOTES.md:134 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| RECUT_NOTES.md:149 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| RECUT_NOTES.md:152 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| RECUT_NOTES.md:365 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| RUN_PLAN.cmd:3 | Generic word or runtime/environment identifier | 2 | Retained: functional identifier, ordinary text or prior redaction marker. |
| RUN_PLAN.cmd:5 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| RUN_PLAN_EXPECTED.md:8 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| RUN_PLAN_EXPECTED.md:10 | Generic word or runtime/environment identifier | 2 | Retained: functional identifier, ordinary text or prior redaction marker. |
| RUN_PLAN_EXPECTED.md:23 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| analysis/check-r-versions.R:2 | Generic word or runtime/environment identifier | 2 | Retained: functional identifier, ordinary text or prior redaction marker. |
| analysis/check-r-versions.R:3 | Generic word or runtime/environment identifier | 2 | Retained: functional identifier, ordinary text or prior redaction marker. |
| analysis/verify_archive.py:22 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| analysis/verify_archive.py:79 | Public creator or repository attribution | 2 | Retained: creator identity and public provenance. |
| analysis/verify_archive.py:81 | Public creator or repository attribution | 1 | Retained: creator identity and public provenance. |
| app/hub/shared/vendor/jspdf.min.js:7 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/hub/shared/vendor/jspdf.min.js:9 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/hub/shared/vendor/jspdf.min.js:10 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/hub/shared/vendor/jspdf.min.js:51 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/hub/shared/vendor/jspdf.min.js:54 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/hub/shared/vendor/jspdf.min.js:86 | Generic word or runtime/environment identifier | 16 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/hub/shared/vendor/jspdf.min.js:89 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/hub/shared/vendor/jspdf.min.js:112 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/hub/shared/vendor/jspdf.min.js:129 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/hub/shared/vendor/jspdf.min.js:134 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/hub/shared/vendor/jspdf.min.js:138 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/hub/shared/vendor/jspdf.min.js:163 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/hub/shared/vendor/jspdf.min.js:203 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/hub/shared/vendor/jspdf.min.js:275 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/hub/shared/vendor/jspdf.min.js:335 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/hub/shared/vendor/jspdf.min.js:361 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/mh-peto/index.html:745 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/mh-peto/validate/adapter.js:208 | Public creator or repository attribution | 1 | Retained: creator identity and public provenance. |
| app/mh-peto/validate/adapter.js:210 | Public creator or repository attribution | 1 | Retained: creator identity and public provenance. |
| app/r-shiny/shinylive/webr/R.js:1823 | Generic word or runtime/environment identifier | 233 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.js:1823 | Virtual filesystem path | 2 | Retained: upstream runtime path, not a local machine path. |
| app/r-shiny/shinylive/webr/R.wasm:216 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:219 | Generic word or runtime/environment identifier | 2 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:229 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:574 | Generic word or runtime/environment identifier | 3 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:575 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:29456 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:29466 | Generic word or runtime/environment identifier | 10 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:29467 | Generic word or runtime/environment identifier | 3 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:29471 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:29474 | Generic word or runtime/environment identifier | 2 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:29885 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:30654 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:30655 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:30689 | Generic word or runtime/environment identifier | 2 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:30769 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:30770 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:30829 | Generic word or runtime/environment identifier | 2 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:30841 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:31463 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:31470 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:31521 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:31522 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:31601 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:31618 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:31619 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:36544 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:36545 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:36546 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:37320 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:37321 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:38082 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:38083 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:40425 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:41054 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:41055 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:42977 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:42978 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:42979 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:43232 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:46793 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:46794 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:52327 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:52328 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:52329 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:52330 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:52696 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:52697 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:60136 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:60137 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:60140 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:60171 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:63801 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:63802 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:64419 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:64420 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:64433 | Generic word or runtime/environment identifier | 2 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:64471 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:64474 | Generic word or runtime/environment identifier | 2 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:64572 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:64614 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:73370 | Generic word or runtime/environment identifier | 2 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:73371 | Generic word or runtime/environment identifier | 12 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:73904 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:73975 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:73976 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:74005 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:74153 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:79703 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/R.wasm:79838 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:79839 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:79857 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/R.wasm:81345 | Generic word or runtime/environment identifier | 2 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/library.data.gz:44924 | Credential-prefix substring | 1 | Retained: accidental compressed-byte match, not a key. |
| app/r-shiny/shinylive/webr/library.js.metadata:1 | Generic word or runtime/environment identifier | 9 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/packages/numDeriv/numDeriv_2016.8-1.1.tgz:179 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/translations/DESCRIPTION:5 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/webr-worker.js:2 | Generic word or runtime/environment identifier | 2 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/webr-worker.js:3 | Generic word or runtime/environment identifier | 2 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/webr-worker.js:35 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/webr-worker.js:36 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| app/r-shiny/shinylive/webr/webr.mjs:2 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/r-shiny/shinylive/webr/webr.mjs:2 | Virtual filesystem path | 1 | Retained: upstream runtime path, not a local machine path. |
| app/shared/alm-validate.js:3 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/shared/alm-validate.js:4 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/shared/autosave.js:4 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/shared/autosave.js:58 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/shared/build-info.js:28 | Public creator or repository attribution | 1 | Retained: creator identity and public provenance. |
| app/shared/ma-studies-v1.js:350 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/shared/ma-studies-v1.js:351 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/shared/ma-studies-v1.js:398 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/shared/ma-studies-v1.js:608 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/shared/truthcert-export.js:4 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| app/shared/truthcert-export.js:6 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| bench/README.md:3 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| bench/docs/dat.aloe2013.txt:54 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.anand1999.txt:51 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.anker2025.txt:68 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.assink2016.txt:56 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.axfors2021.txt:44 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.bakdash2021.txt:90 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.bakdash2021.txt:91 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.bakdash2021.txt:92 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.bakdash2021.txt:93 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.baker2009.txt:45 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.bangertdrowns2004.txt:58 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.bartos2023.txt:42 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.baskerville2012.txt:64 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.bassler2004.txt:42 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.bauer2002.txt:50 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.bcg.txt:48 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.begg1989.txt:49 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.berkey1998.txt:66 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.berkey1998r.txt:66 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.besson2016.txt:99 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.bonett2010.txt:42 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.bornmann2007.txt:45 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.bourassa1996.txt:67 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.cannon2006.txt:48 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.chiarito2020.txt:6 | Credential-prefix substring | 1 | Retained: ordinary prose or filename substring, not a key. |
| bench/docs/dat.chiarito2020.txt:64 | Credential-prefix substring | 1 | Retained: ordinary prose or filename substring, not a key. |
| bench/docs/dat.chiarito2020.txt:70 | Credential-prefix substring | 1 | Retained: ordinary prose or filename substring, not a key. |
| bench/docs/dat.chiarito2020.txt:74 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.cohen1981.txt:45 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.colditz1994.txt:48 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.collins1985a.txt:50 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.collins1985b.txt:45 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.craft2003.txt:47 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.crede2010.txt:45 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.crisafulli2020.txt:46 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.curtin2002.txt:38 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.curtis1998.txt:86 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.dagostino1998.txt:70 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.damico2009.txt:39 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.debruin2009.txt:53 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.demir2022.txt:40 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.dogliotti2014.txt:41 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.dong2013.txt:44 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.dorn2007.txt:49 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.dumouchel1994.txt:50 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.egger2001.txt:50 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.feng2019.txt:43 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.fine1993.txt:50 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.franchini2012.txt:51 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.frank2008.txt:47 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.furukawa2003.txt:47 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.gibson2002.txt:78 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.graves2010.txt:41 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.greb2008.txt:42 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.greenland1992.txt:40 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.gurusamy2011.txt:51 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.hackshaw1998.txt:54 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.hahn2001.txt:41 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.hannum2020.txt:46 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.hart1999.txt:46 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.hartmannboyce2018.txt:42 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.hasselblad1998.txt:46 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.higgins2008.txt:46 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.hine1989.txt:45 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.huber2000.txt:45 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.ishak2007.txt:64 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.kalaian1996.txt:59 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.karner2014.txt:5 | Credential-prefix substring | 1 | Retained: ordinary prose or filename substring, not a key. |
| bench/docs/dat.karner2014.txt:64 | Credential-prefix substring | 1 | Retained: ordinary prose or filename substring, not a key. |
| bench/docs/dat.karner2014.txt:71 | Credential-prefix substring | 1 | Retained: ordinary prose or filename substring, not a key. |
| bench/docs/dat.karner2014.txt:75 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.kearon1998.txt:48 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.knapp2017.txt:74 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.konstantopoulos2011.txt:58 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.landenberger2005.txt:66 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.laopaiboon2015.txt:47 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.lau1992.txt:38 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.lee2004.txt:40 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.lehmann2018.txt:89 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.li2007.txt:40 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.lim2014.txt:51 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.linde2005.txt:80 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.linde2015.txt:65 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.linde2016.txt:63 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.lloyd2010.txt:39 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.lopez2019.txt:75 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.maire2019.txt:55 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.mccurdy2020.txt:89 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.mcdaniel1994.txt:62 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.meeker2017.txt:37 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.michael2013.txt:69 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.molloy2014.txt:32 | Credential-prefix substring | 1 | Retained: ordinary prose or filename substring, not a key. |
| bench/docs/dat.molloy2014.txt:61 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.moore1998.txt:45 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.moura2021.txt:46 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.nakagawa2007.txt:35 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.nielweise2007.txt:48 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.nielweise2008.txt:49 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.nissen2007.txt:67 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.normand1999.txt:41 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.obrien2003.txt:47 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.pagliaro1992.txt:42 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.pignon2000.txt:49 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.poole2003.txt:48 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.pritz1997.txt:40 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.quan2000.txt:40 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.raudenbush1985.txt:78 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.riley2003.txt:49 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.rivera2025.txt:52 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.roever2022.txt:41 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.senn2013.txt:47 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.spooner2002.txt:53 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.steurer2006.txt:45 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.stowe2010.txt:57 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.tannersmith2016.txt:57 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.thompson1999.txt:40 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.tian2009.txt:52 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.ursino2021.txt:40 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.vanhowe1999.txt:50 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.viechtbauer2021.txt:36 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.white2020.txt:51 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.woods2010.txt:34 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/docs/dat.yusuf1985.txt:48 | Public third-party contact | 1 | Retained: public upstream notice; exact blob or original-evidence identity. |
| bench/finalize.py:100 | Generic word or runtime/environment identifier | 2 | Retained: functional identifier, ordinary text or prior redaction marker. |
| provenance/run_plan-2026-10-20-release.log:2 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| rerun/v1.1.0/validate.R:3 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| rerun/v1.1.0/validate.R:4 | Generic word or runtime/environment identifier | 2 | Retained: functional identifier, ordinary text or prior redaction marker. |
| rerun/v1.1.0/validate.R:5 | Generic word or runtime/environment identifier | 2 | Retained: functional identifier, ordinary text or prior redaction marker. |
| results/HISTORICAL_RESULTS.md:154 | Generic word or runtime/environment identifier | 2 | Retained: functional identifier, ordinary text or prior redaction marker. |
| results/source-hashes.json:13 | Credential-prefix substring | 1 | Retained: ordinary prose or filename substring, not a key. |
| validate.R:3 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| validate.R:4 | Generic word or runtime/environment identifier | 2 | Retained: functional identifier, ordinary text or prior redaction marker. |
| validate.R:5 | Generic word or runtime/environment identifier | 2 | Retained: functional identifier, ordinary text or prior redaction marker. |
| validation-plus/README-plus.md:4 | Public creator or repository attribution | 1 | Retained: creator identity and public provenance. |
| validation-plus/README-plus.md:99 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| validation-plus/generate-plus.R:81 | Generic word or runtime/environment identifier | 1 | Retained: functional identifier, ordinary text or prior redaction marker. |
| validation-plus/regenerate-plus.R:2 | Generic word or runtime/environment identifier | 2 | Retained: functional identifier, ordinary text or prior redaction marker. |
| validation-plus/regenerate-plus.R:3 | Generic word or runtime/environment identifier | 2 | Retained: functional identifier, ordinary text or prior redaction marker. |

Historical finalization scan coverage (before exclusion of earlier attempts): 303 publishable files; 595 broad-pattern occurrences grouped into 289 file/line/disposition rows, plus the three incoming-log redactions listed above. No private-path or credential finding remains unresolved; the public-notice exception and missing prior-version DOI are disclosed above.

## Evidence fix

Corrected the run-evidence check to use only rerun/v1.1.0, the 2026-10-20
release run against allmeta 1cb3f84. Earlier candidate attempts are excluded
from the archive. Removed their obsolete path references throughout the
archive and changed future preservation to use the sibling attempts directory.

The provenance release log retains its existing private-profile redactions.
Its obsolete preservation destination on line 22 is additionally replaced by
[earlier attempt path omitted]; all other log bytes are unchanged.
rerun/v1.1.0/RUN_LOG.txt is a byte-for-byte copy of that redacted release log.

No run-evidence generator exists in the archive. Recomputed RERUN_SHA256.json
with Python hashlib from the seven required and three large files present in
rerun/v1.1.0, preserving the manifest schema and exact file inventory.
Regenerated SOURCE_SHA256.json with analysis/recut_manifest.py --write.
No validation input, oracle pin, expected value, tolerance or numerical
verification code was changed. Byte scanning found no obsolete backup paths.

Executed python analysis/verify_archive.py from archive/ in this session.
It exited 1 before checks because Pillow's imaging DLL could not initialize.
The last ten output lines (private local prefix redacted) were:

~~~text
Traceback (most recent call last):
  File "<LOCAL>\lanes\recut-mhpeto\archive\analysis\verify_archive.py", line 4, in <module>
    from PIL import Image
  File "<LOCAL>\AppData\Roaming\Python\Python313\site-packages\PIL\Image.py", line 95, in <module>
    from . import _imaging as core
ImportError: DLL load failed while importing _imaging: A dynamic link library (DLL) initialization routine failed.
~~~

Python 3.13.13 and the alternate installed Python 3.14 both failed to import
Pillow and Matplotlib native modules; NumPy and PyYAML imports succeeded.
No validation assertion was bypassed. A fresh ARCHIVE PASS is still required
in a working native-library environment; the release log's historical pass
does not establish a pass for this edited tree.

The separate archive manifest verifier completed successfully for this fix:

~~~text
RUN EVIDENCE PASS: 7 required files; 3 large-file hashes recorded and checked when present
ORIGINAL INPUTS AND PLUS PINS PASS; app dependencies and webR package pins verified
MANIFEST PASS: app and archive inventories match
~~~

All three large evidence files were present and hashed. The two release logs
were checked for byte equality, and both edited Python modules compile.
 
Runner verification after the evidence fix (2026-10-20, outside the Codex sandbox): python analysis/verify_archive.py printed RUN EVIDENCE PASS (7 required files), TAIL ARCHIVE PASS 106/106 and ARCHIVE PASS: 56 app hashes; 251 source hashes; 68461/68461 final checks.
