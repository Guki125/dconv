@echo off
setlocal EnableDelayedExpansion
chcp 65001 >nul 2>&1

echo.
echo  ╔══════════════════════════════╗
echo  ║     dconv installer          ║
echo  ║  DOCX/DOC ↔ PDF converter   ║
echo  ╚══════════════════════════════╝
echo.

:: ── Check Python ─────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo [dconv] ERROR: Python not found.
    echo         Install it from https://www.python.org/downloads/
    echo         Make sure to check "Add Python to PATH" during install.
    pause
    exit /b 1
)

for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo [dconv] Found Python %PYVER%

:: ── Check / Install LibreOffice ───────────────
set LO_PATH=%PROGRAMFILES%\LibreOffice\program\soffice.exe
if exist "%LO_PATH%" (
    echo [dconv] LibreOffice already installed
    goto INSTALL_DCONV
)

echo [dconv] LibreOffice not found. Attempting install via winget...
winget --version >nul 2>&1
if errorlevel 1 (
    echo [dconv] WARNING: winget not found.
    echo         Please install LibreOffice manually:
    echo         https://www.libreoffice.org/download/download/
    echo         Then re-run this script.
    pause
    exit /b 1
)

winget install --id TheDocumentFoundation.LibreOffice -e --silent
if errorlevel 1 (
    echo [dconv] ERROR: Failed to install LibreOffice via winget.
    echo         Download manually: https://www.libreoffice.org/download/download/
    pause
    exit /b 1
)
echo [dconv] LibreOffice installed successfully

:INSTALL_DCONV
:: ── Install dconv ─────────────────────────────
echo [dconv] Installing dconv...
python -m pip install --upgrade pip -q
python -m pip install -e .
if errorlevel 1 (
    echo [dconv] ERROR: pip install failed.
    pause
    exit /b 1
)

:: ── Verify ────────────────────────────────────
echo.
dconv --help >nul 2>&1
if errorlevel 1 (
    echo [dconv] WARNING: dconv not found in PATH yet.
    echo         Try restarting your terminal and run: dconv --help
) else (
    echo [dconv] All done! Run:  dconv --help
)

echo.
pause
