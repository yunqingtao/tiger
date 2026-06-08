@echo off
setlocal
cd /d "%~dp0"
if "%1"=="" (
    echo 用法: fix.bat ^<框架名^>
    echo 示例: fix.bat hermes
    goto :end
)
python devfit.py fix %*
:end
endlocal
