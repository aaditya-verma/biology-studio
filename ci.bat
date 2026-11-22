@echo off
rem Purpose: one-click CI status (CIG): last 5 runs of the automatic checks + the failed-step log of the newest red one.
rem Use:  ci.bat                 writes out\ci-status.txt and shows it
rem       ci.bat --preview       runs only, no log (fast)       ci.bat --only <run id>   one run
rem       ci.bat --dry-run       show the gh commands; run nothing   ci.bat --debug   print each gh call
rem Needs: GitHub CLI signed in (winget install GitHub.cli, then gh auth login). Owner doc: studio-docs/build/setup-guide.md §6a.
rem EDIT: nothing here; settings are at the top of tools\ci\status.py.
setlocal
cd /d "%~dp0"
where python >nul 2>nul || (echo [ci] Python not found - install it ^(setup guide section 5^). & pause & exit /b 2)
python -X utf8 tools\ci\status.py %*
set CIRC=%errorlevel%
if "%CIRC%"=="1" echo [ci] The newest finished run is RED - open out\ci-status.txt, or paste it into a chat.
if "%CIRC%"=="2" echo [ci] Could not ask GitHub - see the message above.
pause
exit /b %CIRC%
