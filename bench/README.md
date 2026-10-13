# Historical benchmark scripts

These scripts are preserved from the final run. Local machine paths are replaced by <ALLMETA_ROOT> and <R_LIBS_USER>; replace these in a private working copy. Use a scratch directory inside this archive for any rerun, copying the data and scripts there. build.R creates the metadat corpus; reference.R creates all MH/Peto and ancillary references; run-app.cjs runs the actual browser page; fragility-reference.R executes the independent greedy oracle; compare.py compares records. finalize.py is historical provenance and expects the original baseline checkout, not the validation-enhanced app snapshot.

R packages: metafor 5.2-1, metadat 1.6-0; runner: installed Node playwright and Chrome. run-app.cjs accepts the app root and output path and resumes existing outputs, so use a new output filename for fresh coverage. For the supported portable offline command, use Rscript validate.R at the archive root.
