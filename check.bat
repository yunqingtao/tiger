@echo off
setlocal
cd /d "%~dp0"
if "%1"=="" (
    echo 用法: check.bat ^<框架名^>
    echo 示例: check.bat hermes
    echo 所有框架: python devfit.py list
    goto :end
)
python devfit.py check %*
:end
endlocal
