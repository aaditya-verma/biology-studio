@echo off
rem Purpose: one-click git sync for docs and code (RULES I8). Owner doc: studio-docs/build/setup-guide.md §6.
rem Use:  sync.bat              pull only (run before a chat)
rem       sync.bat "message"    pull, then commit everything changed and push (after a chat)
rem       sync.bat --dry-run    show what would be committed; change nothing
rem EDIT: nothing to edit; uses the repo this file sits in.
cd /d "%~dp0"
if /i "%~1"=="--dry-run" ( git fetch & git status -sb & goto :eof )
git pull --rebase || ( echo [sync] Pull failed - stop and ask a chat to help. & pause & goto :eof )
if "%~1"=="" ( echo [sync] Up to date. & pause & goto :eof )
git add -A
git commit -m "%~1" || echo [sync] Nothing to commit.
git push && echo [sync] Pushed. Now press Sync now in your Claude Project.
pause
