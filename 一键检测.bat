@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

echo.
echo   ╔══════════════════════════════════╗
echo   ║   DevFit 一键环境检测            ║
echo   ║   国内自动镜像 · 小白友好        ║
echo   ╚══════════════════════════════════╝
echo.
echo   [检测] 查看环境是否合格
echo   [修复] 自动装缺失依赖(镜像加速)
echo   [全部] 查看支持的27个框架
echo.
echo   ── 常用框架 ──
echo   [1] Hermes Agent
echo   [2] Python
echo   [3] Node.js
echo   [4] Git
echo   [5] Docker
echo   [6] Chrome
echo   [7] OpenClaw
echo   [8] Ollama
echo.
echo   [L] 列出全部框架
echo   [Q] 退出
echo.
set /p choice="  输入编号或框架名: "

if /i "%choice%"=="1" goto :run_hermes
if /i "%choice%"=="2" goto :run_python
if /i "%choice%"=="3" goto :run_node
if /i "%choice%"=="4" goto :run_git
if /i "%choice%"=="5" goto :run_docker
if /i "%choice%"=="6" goto :run_chrome
if /i "%choice%"=="7" goto :run_openclaw
if /i "%choice%"=="8" goto :run_ollama
if /i "%choice%"=="L" goto :list
if /i "%choice%"=="Q" goto :end
if /i "%choice%"=="检测" goto :ask_check
if /i "%choice%"=="修复" goto :ask_fix
if /i "%choice%"=="全部" goto :list

:: Direct check by name
python devfit.py check %choice%
goto :end

:run_hermes
python devfit.py check hermes
goto :end
:run_python
python devfit.py check python
goto :end
:run_node
python devfit.py check node
goto :end
:run_git
python devfit.py check git
goto :end
:run_docker
python devfit.py check docker
goto :end
:run_chrome
python devfit.py check chrome
goto :end
:run_openclaw
python devfit.py check openclaw
goto :end
:run_ollama
python devfit.py check ollama
goto :end

:list
python devfit.py list
goto :end

:ask_check
set /p fw="  输入框架名: "
python devfit.py check %fw%
goto :end

:ask_fix
set /p fw="  输入框架名: "
python devfit.py fix %fw%
goto :end

:end
echo.
pause
endlocal
