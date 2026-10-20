@echo off
cd /d "%~dp0"
echo === Verify full archive after repairing the Python Pillow DLL environment
python analysis/verify_archive.py || exit /b 1
