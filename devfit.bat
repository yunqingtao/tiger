@echo off
setlocal
cd /d "%~dp0"
python devfit.py %*
endlocal
