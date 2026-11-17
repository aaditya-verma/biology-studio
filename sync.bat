@echo off
rem Purpose: one-click git sync for docs and code (RULES I8). Owner doc: studio-docs/build/setup-guide.md §6a.
rem Use:  sync.bat              pull only (run before a chat)
rem       sync.bat "message"    commit everything changed, pull (rebase), push (after a chat)
rem       sync.bat --dry-run    show what would be committed; change nothing
rem EDIT: nothing to edit; uses the repo this file sits in.
cd /d "%~dp0"
if /i "%~1"=="--dry-run" goto dry
if "%~1"=="" goto pullonly
git add -A
git commit -m "%~1" || echo [sync] Nothing new to commit.
git pull --rebase || goto pullfail
git push || goto pushfail
echo [sync] Pushed. Now press Sync now in your Claude Project.
pause
goto :eof
:pullonly
git pull --rebase --autostash || goto pullfail
echo [sync] Up to date.
pause
goto :eof
:dry
git fetch
git status -s -uall
pause
goto :eof
:pullfail
echo [sync] Pull failed - don't delete anything; ask a chat (route B) to help merge.
pause
goto :eof
:pushfail
echo [sync] Push failed - check your internet / GitHub sign-in, or ask a chat.
pause
