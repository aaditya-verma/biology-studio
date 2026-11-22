@echo off
rem Purpose: one-click git sync for docs and code (RULES I8), with the pre-push guard (CIG). Owner doc: studio-docs/build/setup-guide.md §6a.
rem Use:  sync.bat              pull only (run before a chat)
rem       sync.bat "message"    guard, commit everything changed, pull (rebase), guard again, push (after a chat)
rem       sync.bat --check      run the guard only (rebuilds sources.json); commit nothing, push nothing
rem       sync.bat --dry-run    show what would be committed; change nothing
rem Guard: card-check --write-sources (rebuilds content\E\sources.json), then card-check, scene-check, tracker, lesson-check
rem        (each + --selftest) - the fast CI checks; CI alone runs parity, map, stills, layout-check.
rem        Any error = stop: nothing is pushed. Fix it (or ask a chat), then run the same line again.
rem EDIT: the checks the guard runs are in :guard below (keep them in step with .github/workflows/checks.yml).
setlocal
cd /d "%~dp0"
if /i "%~1"=="--dry-run" goto dry
if /i "%~1"=="--check" goto checkonly
if "%~1"=="" goto pullonly
call :guard write || goto guardfail
git add -A
git commit -m "%~1" || echo [sync] Nothing new to commit.
git pull --rebase || goto pullfail
rem Re-check what will actually be pushed: the pull may have brought the other person's changes.
rem The other side's DECISIONS/registry lines make sources.json stale, so rebuild it and commit it if it changed.
call :guard write || goto guardfail2
git diff --quiet -- content\E\sources.json || git commit -m "%~1 (sources.json rebuilt after pull)" -- content\E\sources.json
git push || goto pushfail
echo [sync] Checks passed and pushed. Now press Sync now in your Claude Project.
pause
goto :eof

:checkonly
call :guard write || goto guardfail
echo [sync] Guard passed. Nothing committed or pushed.
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

rem ---- the guard: exit code 1 on the first failing check ----
:guard
where python >nul 2>nul || (echo [sync] Python not found - install it ^(setup guide section 5^) or ask a chat. & exit /b 1)
if not exist out mkdir out
if "%~1"=="write" (
  echo [sync] Guard: rebuilding content\E\sources.json ...
  python -X utf8 tools\card-check\check.py --write-sources || (echo [sync] FAILED: card-check --write-sources & exit /b 1)
)
call :run "card-check" tools\card-check\check.py || exit /b 1
call :run "card-check selftest" tools\card-check\check.py --selftest || exit /b 1
call :run "scene-check" tools\scene-check\check.py || exit /b 1
call :run "scene-check selftest" tools\scene-check\check.py --selftest || exit /b 1
call :run "tracker check - steps.json" tools\tracker\check.py || exit /b 1
call :run "tracker selftest" tools\tracker\check.py --selftest || exit /b 1
call :run "lesson-check" tools\lesson-check\check.py || exit /b 1
call :run "lesson-check selftest" tools\lesson-check\check.py --selftest || exit /b 1
echo [sync] Guard: all checks passed.
exit /b 0

rem :run "<name>" <script> [args] - one check; its output goes to out\sync-check.txt and is shown only if it fails.
:run
echo [sync] Guard: %~1 ...
python -X utf8 %2 %3 %4 > out\sync-check.txt 2>&1
if errorlevel 1 (type out\sync-check.txt & echo [sync] FAILED: %~1 ^(output above, also in out\sync-check.txt^) & exit /b 1)
exit /b 0

:guardfail
echo [sync] Stopped: a check failed. Nothing was committed or pushed. Fix it (or ask a chat), then run the same line again.
pause
exit /b 1
:guardfail2
echo [sync] Stopped after the pull: a check fails on the merged files. Your commit is saved here but NOT pushed.
echo [sync] Run the same sync.bat "message" line once more first. Still failing - ask a chat (route B) to fix it.
pause
exit /b 1
:pullfail
echo [sync] Pull failed - don't delete anything; ask a chat (route B) to help merge.
pause
exit /b 1
:pushfail
echo [sync] Push failed - check your internet / GitHub sign-in, or ask a chat.
pause
exit /b 1
