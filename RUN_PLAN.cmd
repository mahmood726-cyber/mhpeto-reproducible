@echo off
echo === R PATH & set "PATH=%R_HOME%\bin;%PATH%"
echo === R user library & rem R_LIBS_USER is supplied by the caller
echo === R additional library & rem R_LIBS is supplied by the caller
echo === R environment & set R_ENVIRON_USER=NUL
echo === runtime note & rem Rscript = %R_HOME%\bin\Rscript.exe ; node and python are on PATH
echo === UTF-8 console & set PYTHONIOENCODING=utf-8
echo === Verify prepared manifests & python analysis/recut_manifest.py --verify || exit /b 1
echo === Check native R versions & Rscript analysis/check-r-versions.R || exit /b 1
echo === Preserve previous replay & python analysis/recut_runner.py preserve || exit /b 1
echo === Prepare original replay & python analysis/recut_runner.py prepare || exit /b 1
echo === Replay original browser & node analysis/replay-app.cjs app rerun/v1.1.0/results/app-patched.json || exit /b 1
echo === Compare original protocol & python analysis/recut_runner.py compare || exit /b 1
echo === Recompute original R validation & python analysis/recut_runner.py r || exit /b 1
echo === Check extras and text claims & node validation-plus/run-plus.mjs --json rerun/v1.1.0/plus-comparison.json || exit /b 1
echo === Verify retained publication outputs & python analysis/verify_archive.py || exit /b 1
echo === Verify final manifests & python analysis/recut_manifest.py --verify || exit /b 1
