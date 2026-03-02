@echo off
REM EVA Asset Copy Script - Project 10 MkDocs PoC
REM Copies 98 visual assets from EVA-JP-reference-0113 into Project 10 normalized structure
REM
REM CRITICAL: Windows Enterprise Encoding Safety
REM - ASCII-only output characters: [INFO], [PASS], [ERROR], [FOUND]
REM - No Unicode: NO checkmarks, crosses, emojis, ellipsis
REM
REM Usage: copy-eva-assets.bat
REM Result: Creates docs/assets/ with 11 category folders and 98 copied assets

setlocal enabledelayedexpansion

REM Set encoding for Windows enterprise safety
set PYTHONIOENCODING=utf-8

REM Define paths
set "SOURCE_ROOT=C:\Users\marco.presta\OneDrive - ESDC EDSC\Documents\AICOE\EVA-JP-reference-0113"
set "TARGET_ROOT=%~dp0docs\assets"

echo [INFO] EVA Asset Copy Script - Project 10 MkDocs PoC
echo [INFO] Starting asset copy operation
echo.
echo [INFO] Source: %SOURCE_ROOT%
echo [INFO] Target: %TARGET_ROOT%
echo.

REM Pre-flight validation
if not exist "%SOURCE_ROOT%" (
    echo [ERROR] Source repository not found: %SOURCE_ROOT%
    echo [ERROR] Please verify EVA-JP-reference-0113 is cloned to expected location
    exit /b 1
)

echo [PASS] Source repository found
echo.

REM Create target directory structure
echo [INFO] Creating target directory structure...
mkdir "%TARGET_ROOT%\branding" 2>nul
mkdir "%TARGET_ROOT%\architecture" 2>nul
mkdir "%TARGET_ROOT%\ui" 2>nul
mkdir "%TARGET_ROOT%\deployment" 2>nul
mkdir "%TARGET_ROOT%\development" 2>nul
mkdir "%TARGET_ROOT%\debugging" 2>nul
mkdir "%TARGET_ROOT%\features" 2>nul
mkdir "%TARGET_ROOT%\governance" 2>nul
mkdir "%TARGET_ROOT%\source-diagrams" 2>nul
mkdir "%TARGET_ROOT%\reference-docs" 2>nul
mkdir "%TARGET_ROOT%\diagrams\svg" 2>nul
mkdir "%TARGET_ROOT%\diagrams\png" 2>nul

echo [PASS] Directory structure created
echo.

REM Initialize counters
set /a TOTAL_FILES=0
set /a COPIED_FILES=0
set /a FAILED_FILES=0

REM ============================================================================
REM Category 1: Branding Assets (5 files)
REM ============================================================================
echo [INFO] Copying branding assets (5 files)...

copy "%SOURCE_ROOT%\app\frontend\src\assets\github.svg" "%TARGET_ROOT%\branding\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\app\frontend\src\assets\openai.svg" "%TARGET_ROOT%\branding\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\app\frontend\src\assets\search.svg" "%TARGET_ROOT%\branding\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\esdc logo.png" "%TARGET_ROOT%\branding\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\app\frontend\favicon.ico" "%TARGET_ROOT%\branding\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

set /a TOTAL_FILES+=5
echo [PASS] Branding assets: %COPIED_FILES% of 5 copied
echo.

REM ============================================================================
REM Category 2: Architecture Diagrams (10 files)
REM ============================================================================
echo [INFO] Copying architecture diagrams (10 files)...
set /a BEFORE_ARCH=%COPIED_FILES%

copy "%SOURCE_ROOT%\docs\images\Secure Deployment High-Level Architecture.png" "%TARGET_ROOT%\architecture\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Secure Deployment Architecture Detailed.png" "%TARGET_ROOT%\architecture\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Frontend Architecture Diagram.png" "%TARGET_ROOT%\architecture\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Functions Architecture Diagram.png" "%TARGET_ROOT%\architecture\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Network Architecture Diagram.png" "%TARGET_ROOT%\architecture\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Ingest Process Flow.png" "%TARGET_ROOT%\architecture\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Enrichment Process Flow.png" "%TARGET_ROOT%\architecture\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Vector Search Architecture.png" "%TARGET_ROOT%\architecture\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\SharePoint Logic App overview.png" "%TARGET_ROOT%\architecture\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\App Components.png" "%TARGET_ROOT%\architecture\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

set /a TOTAL_FILES+=10
set /a ARCH_COPIED=%COPIED_FILES%-%BEFORE_ARCH%
echo [PASS] Architecture diagrams: %ARCH_COPIED% of 10 copied
echo.

REM ============================================================================
REM Category 3: UI Screenshots (17 files)
REM ============================================================================
echo [INFO] Copying UI screenshots (17 files)...
set /a BEFORE_UI=%COPIED_FILES%

copy "%SOURCE_ROOT%\docs\images\Chat UI.png" "%TARGET_ROOT%\ui\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Work and Web.png" "%TARGET_ROOT%\ui\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Main UI.png" "%TARGET_ROOT%\ui\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Content Library.png" "%TARGET_ROOT%\ui\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Upload Files (Pre-Upload).png" "%TARGET_ROOT%\ui\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Upload Files (Uploading).png" "%TARGET_ROOT%\ui\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Upload Files (Uploaded).png" "%TARGET_ROOT%\ui\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Example of the upload workflow.png" "%TARGET_ROOT%\ui\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Citation Modal.png" "%TARGET_ROOT%\ui\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Detailed Upload Process.png" "%TARGET_ROOT%\ui\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Content View UI.png" "%TARGET_ROOT%\ui\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Response Streaming.png" "%TARGET_ROOT%\ui\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Side-by-Side Comparison.png" "%TARGET_ROOT%\ui\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Chat Interface.png" "%TARGET_ROOT%\ui\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Hybrid Search Interface.png" "%TARGET_ROOT%\ui\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Session Management.png" "%TARGET_ROOT%\ui\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Content Management Panel.png" "%TARGET_ROOT%\ui\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

set /a TOTAL_FILES+=17
set /a UI_COPIED=%COPIED_FILES%-%BEFORE_UI%
echo [PASS] UI screenshots: %UI_COPIED% of 17 copied
echo.

REM ============================================================================
REM Category 4: Deployment Screenshots (10 files)
REM ============================================================================
echo [INFO] Copying deployment screenshots (10 files)...
set /a BEFORE_DEPLOY=%COPIED_FILES%

copy "%SOURCE_ROOT%\docs\images\App Registration Overview.png" "%TARGET_ROOT%\deployment\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\App Registration API Permissions.png" "%TARGET_ROOT%\deployment\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\App Registration Authentication.png" "%TARGET_ROOT%\deployment\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\App Registration Expose API.png" "%TARGET_ROOT%\deployment\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\CosmosDB Networking.png" "%TARGET_ROOT%\deployment\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Auth Issues.png" "%TARGET_ROOT%\deployment\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Authentication Configuration.jpg" "%TARGET_ROOT%\deployment\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Deployment Pipeline Config.jpg" "%TARGET_ROOT%\deployment\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\upload_interface.jpg" "%TARGET_ROOT%\deployment\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\web_ui_overview.jpg" "%TARGET_ROOT%\deployment\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

set /a TOTAL_FILES+=10
set /a DEPLOY_COPIED=%COPIED_FILES%-%BEFORE_DEPLOY%
echo [PASS] Deployment screenshots: %DEPLOY_COPIED% of 10 copied
echo.

REM ============================================================================
REM Category 5: Development Screenshots (15 files)
REM ============================================================================
echo [INFO] Copying development screenshots (15 files)...
set /a BEFORE_DEV=%COPIED_FILES%

copy "%SOURCE_ROOT%\docs\images\Codespaces Dashboard.png" "%TARGET_ROOT%\development\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Codespaces Creation.png" "%TARGET_ROOT%\development\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Codespaces Editor.png" "%TARGET_ROOT%\development\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Codespaces Ports.png" "%TARGET_ROOT%\development\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\VS Code Setup.png" "%TARGET_ROOT%\development\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\VS Code Extensions.png" "%TARGET_ROOT%\development\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Python Environment Setup.png" "%TARGET_ROOT%\development\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Terminal Configuration.png" "%TARGET_ROOT%\development\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Backend Test Environment.png" "%TARGET_ROOT%\development\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Fork Repository.png" "%TARGET_ROOT%\development\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Clone Repository.png" "%TARGET_ROOT%\development\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Environment Setup Complete.png" "%TARGET_ROOT%\development\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\GitHub Repository Structure.png" "%TARGET_ROOT%\development\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\local_dev_environment.jpg" "%TARGET_ROOT%\development\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\repository_setup.jpg" "%TARGET_ROOT%\development\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

set /a TOTAL_FILES+=15
set /a DEV_COPIED=%COPIED_FILES%-%BEFORE_DEV%
echo [PASS] Development screenshots: %DEV_COPIED% of 15 copied
echo.

REM ============================================================================
REM Category 6: Debugging Screenshots (11 files)
REM ============================================================================
echo [INFO] Copying debugging screenshots (11 files)...
set /a BEFORE_DEBUG=%COPIED_FILES%

copy "%SOURCE_ROOT%\docs\images\FastAPI Backend Logs.png" "%TARGET_ROOT%\debugging\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Function App Logs.png" "%TARGET_ROOT%\debugging\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Network Debug Tools.png" "%TARGET_ROOT%\debugging\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Console Errors.png" "%TARGET_ROOT%\debugging\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\CORS Configuration.png" "%TARGET_ROOT%\debugging\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Environment Variable Check.png" "%TARGET_ROOT%\debugging\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Frontend Dev Server.png" "%TARGET_ROOT%\debugging\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Known Issues Dashboard.png" "%TARGET_ROOT%\debugging\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Browser Dev Tools Network Tab.png" "%TARGET_ROOT%\debugging\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Azure Portal Logs.png" "%TARGET_ROOT%\debugging\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Vite Frontend Watch Mode.png" "%TARGET_ROOT%\debugging\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

set /a TOTAL_FILES+=11
set /a DEBUG_COPIED=%COPIED_FILES%-%BEFORE_DEBUG%
echo [PASS] Debugging screenshots: %DEBUG_COPIED% of 11 copied
echo.

REM ============================================================================
REM Category 7: Feature Screenshots (18 files)
REM ============================================================================
echo [INFO] Copying feature screenshots (18 files)...
set /a BEFORE_FEAT=%COPIED_FILES%

copy "%SOURCE_ROOT%\docs\images\Work + Web Mode.png" "%TARGET_ROOT%\features\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Math Assistant Feature.png" "%TARGET_ROOT%\features\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Data Assist Feature.png" "%TARGET_ROOT%\features\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Multilingual Chat.png" "%TARGET_ROOT%\features\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Citation Highlighting.png" "%TARGET_ROOT%\features\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Thought Process Viewer.png" "%TARGET_ROOT%\features\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Supporting Content Panel.png" "%TARGET_ROOT%\features\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Work Only Mode.png" "%TARGET_ROOT%\features\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Hybrid Search Results.png" "%TARGET_ROOT%\features\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Vector Search Demo.png" "%TARGET_ROOT%\features\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Document Preview.png" "%TARGET_ROOT%\features\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Export Chat History.png" "%TARGET_ROOT%\features\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\User Preferences Panel.png" "%TARGET_ROOT%\features\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Document Upload Success.png" "%TARGET_ROOT%\features\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Ungrounded Mode.png" "%TARGET_ROOT%\features\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Developer Settings Panel.png" "%TARGET_ROOT%\features\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Search Results with Citations.png" "%TARGET_ROOT%\features\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Feedback Collection Interface.png" "%TARGET_ROOT%\features\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

set /a TOTAL_FILES+=18
set /a FEAT_COPIED=%COPIED_FILES%-%BEFORE_FEAT%
echo [PASS] Feature screenshots: %FEAT_COPIED% of 18 copied
echo.

REM ============================================================================
REM Category 8: Governance Screenshots (4 files)
REM ============================================================================
echo [INFO] Copying governance screenshots (4 files)...
set /a BEFORE_GOV=%COPIED_FILES%

copy "%SOURCE_ROOT%\docs\images\Analysis Panel.png" "%TARGET_ROOT%\governance\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Citation Transparency.png" "%TARGET_ROOT%\governance\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\Audit Trail View.png" "%TARGET_ROOT%\governance\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\AI Transparency Panel.png" "%TARGET_ROOT%\governance\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

set /a TOTAL_FILES+=4
set /a GOV_COPIED=%COPIED_FILES%-%BEFORE_GOV%
echo [PASS] Governance screenshots: %GOV_COPIED% of 4 copied
echo.

REM ============================================================================
REM Category 9: Source Diagrams (6 files - .drawio)
REM ============================================================================
echo [INFO] Copying source diagrams (6 files)...
set /a BEFORE_SRC=%COPIED_FILES%

copy "%SOURCE_ROOT%\docs\images\architecture-overview.drawio" "%TARGET_ROOT%\source-diagrams\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\frontend-architecture.drawio" "%TARGET_ROOT%\source-diagrams\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\functions-architecture.drawio" "%TARGET_ROOT%\source-diagrams\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\network-architecture.drawio" "%TARGET_ROOT%\source-diagrams\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\ingest-flow.drawio" "%TARGET_ROOT%\source-diagrams\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\images\enrichment-flow.drawio" "%TARGET_ROOT%\source-diagrams\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

set /a TOTAL_FILES+=6
set /a SRC_COPIED=%COPIED_FILES%-%BEFORE_SRC%
echo [PASS] Source diagrams: %SRC_COPIED% of 6 copied
echo.

REM ============================================================================
REM Category 10: Reference Documents (2 files)
REM ============================================================================
echo [INFO] Copying reference documents (2 files)...
set /a BEFORE_REF=%COPIED_FILES%

copy "%SOURCE_ROOT%\docs\Info Assistant Architecture v1.0.pdf" "%TARGET_ROOT%\reference-docs\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

copy "%SOURCE_ROOT%\docs\example.pdf" "%TARGET_ROOT%\reference-docs\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (set /a COPIED_FILES+=1) else (set /a FAILED_FILES+=1)

set /a TOTAL_FILES+=2
set /a REF_COPIED=%COPIED_FILES%-%BEFORE_REF%
echo [PASS] Reference documents: %REF_COPIED% of 2 copied
echo.

REM ============================================================================
REM Summary Report
REM ============================================================================
echo.
echo ============================================================================
echo [INFO] EVA Asset Copy Complete
echo ============================================================================
echo.
echo Total files processed: %TOTAL_FILES%
echo Successfully copied:   %COPIED_FILES%
echo Failed to copy:        %FAILED_FILES%
echo.

if %FAILED_FILES% GTR 0 (
    echo [WARNING] Some files failed to copy. Check source paths.
    echo [INFO] Common causes: File not found, path too long, permission denied
) else (
    echo [PASS] All assets copied successfully
)

echo.
echo Target location: %TARGET_ROOT%
echo.
echo [INFO] Next steps:
echo 1. Run: run_mkdocs_poc.bat (generates site with all assets)
echo 2. Test: Open generated site in browser
echo 3. Verify: Check architecture pages show real diagrams
echo.

endlocal
exit /b 0
