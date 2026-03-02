@echo off
REM ============================================================================
REM MkDocs Proof of Concept - Professional Runner
REM ============================================================================
REM CRITICAL: Windows Enterprise Encoding Safety
REM This script uses ASCII-only output to prevent UnicodeEncodeError crashes
REM in enterprise Windows cp1252 environments.
REM ============================================================================

REM Set encoding for Python
set PYTHONIOENCODING=utf-8

echo.
echo ============================================================================
echo [INFO] MkDocs Proof of Concept - Professional Runner
echo ============================================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not found in PATH
    echo [INFO] Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo [INFO] Python found
echo.

REM Check if we're in the right directory
if not exist "scripts\build_mkdocs.py" (
    echo [WARN] Not in project root, attempting to locate...
    
    REM Try to find project root
    if exist "10-MkDocs-PoC\scripts\build_mkdocs.py" (
        cd 10-MkDocs-PoC
        echo [INFO] Changed directory to 10-MkDocs-PoC
    ) else (
        echo [ERROR] Cannot find project root
        echo [INFO] Please run this script from the 10-MkDocs-PoC directory
        pause
        exit /b 1
    )
)

echo [INFO] Project root detected
echo.

REM Check if dependencies are installed
python -c "import mkdocs" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [WARN] MkDocs not found, installing dependencies...
    echo [INFO] Installing from requirements-core.txt
    python -m pip install -r requirements-core.txt
    
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
    
    echo [PASS] Dependencies installed successfully
    echo.
)

REM Execute the professional runner
echo [INFO] Executing MkDocs PoC builder...
echo.

python scripts\build_mkdocs.py %*

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] MkDocs PoC build failed with exit code %ERRORLEVEL%
    echo [INFO] Check logs\ directory for detailed error information
    echo [INFO] Debug artifacts available in debug\ directory
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ============================================================================
echo [PASS] MkDocs PoC completed successfully
echo ============================================================================
echo.
echo [INFO] Generated artifacts:
echo   - MkDocs site source: mkdocs-sample\docs\
echo   - Static HTML output: mkdocs-sample\site\
echo   - Debug artifacts: debug\
echo   - Evidence reports: evidence\
echo   - Execution logs: logs\
echo.
echo [INFO] Next steps:
echo   1. Test SharePoint Online hosting (upload mkdocs-sample\site\ to SPO)
echo   2. Test Azure Static Website hosting (deploy mkdocs-sample\site\)
echo   3. Review VALIDATION-CHECKLIST.md for detailed test steps
echo.
pause
