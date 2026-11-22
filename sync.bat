@echo off
rem Purpose: one-click git sync for docs and code (RULES I8), with the pre-push guard (CIG). Owner doc: studio-docs/build/setup-guide.md §6a.
rem Use:  sync.bat              pull only (run before a chat)
rem       sync.bat "message"    guard, commit everything changed, pull (rebase), guard again, push (after a chat)
rem       sync.bat "message" --lock-ok   the same, from the chat that HOLDS the build lock (its own app files may go in)
rem       sync.bat --check      run the guard only (rebuilds sources.json); commit nothing, push nothing
rem       sync.bat --dry-run    show what would be committed; change nothing
rem Guard: card-check --write-sources (rebuilds content\E\sources.json), then card-check, scene-check, tracker, lesson-check
rem        (each + --selftest) - the fast CI checks; CI alone runs parity, map, stills, layout-check.
rem        Any error = stop: nothing is pushed. Fix it (or ask a chat), then run the same line again.
rem Lock guard (D-087): while STATUS shows the build lock held, app files (src\ index.html sw.js assets\ tools\) that nobody
rem        staged are never swept in by "git add -A" (X1 Ch 20 / 10b13d5 published U2's unfinished v18). Staged files (a chat's
rem        git add line) = commit only those; nothing staged = stop. The lock holder's own line adds --lock-ok. tools\ci\lock_guard.py.
rem EDIT: the checks the guard runs are in :guard below (keep them in step with .github/workflows/checks.yml).
setlocal
chcp 65001 >nul
cd /d "%~dp0"
if /i "%~1"=="--dry-run" goto dry
if /i "%~1"=="--check" goto checkonly
if "%~1"=="" goto pullonly
set "MSG=%~1"
if "%MSG:~0,2%"=="--" (echo [sync] The message comes first: sync.bat "message" [--lock-ok] & pause & exit /b 1)
if not exist out mkdir out
set "LOCKOK="
if /i "%~2"=="--lock-ok" set "LOCKOK=--lock-ok"
rem Lock guard first (D-087): may this commit include every change, only the staged files, or nothing?
python -X utf8 tools\ci\lock_guard.py %LOCKOK% > out\lock-guard.txt 2>&1
if errorlevel 1 (findstr /v /b "MODE=" out\lock-guard.txt & goto lockstop)
findstr /v /b "MODE=" out\lock-guard.txt
set "ONLYSTAGED="
findstr /x "MODE=staged" out\lock-guard.txt >nul && set "ONLYSTAGED=1"
rem Staged only: set every unstaged change aside (git stash keeps the staged files in place), so the guard checks and rebuilds
rem sources.json from exactly what is committed; the left-out files come back at the end (:unstash).
rem sources.json is generated (the guard rebuilds it), so it never goes into the stash - a stashed copy would clash on the way back (G-Eng r2).
rem sync.bat itself never goes in either: cmd reads this file from disk while it runs, so stashing it would swap the script mid-run
rem (22 Nov 16:22 - a staged-only sync ran the old script from that point and never put the files back).
if defined ONLYSTAGED (git stash push --keep-index --include-untracked -m "sync.bat lock guard: left-out files" -- . ":(exclude)content/E/sources.json" ":(exclude)sync.bat" || goto lockstop)
call :guard write || goto guardfail
if defined ONLYSTAGED (git add -- content\E\sources.json) else (git add -A)
git commit -m "%MSG%" || echo [sync] Nothing new to commit.
git pull --rebase || goto pullfail
rem Re-check what will actually be pushed: the pull may have brought the other person's changes.
rem The other side's DECISIONS/registry lines make sources.json stale, so rebuild it and commit it if it changed.
call :guard write || goto guardfail2
git diff --quiet -- content\E\sources.json || git commit -m "%MSG% (sources.json rebuilt after pull)" -- content\E\sources.json
git push || goto pushfail
call :unstash
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

rem ---- put the files the lock guard left out back (staged-only commits) ----
:unstash
if not defined ONLYSTAGED exit /b 0
set "ONLYSTAGED="
if exist .git\rebase-merge goto unstashlater
if exist .git\rebase-apply goto unstashlater
git checkout -- content\E\sources.json
git stash pop || goto unstashclash
git reset -q
python -X utf8 tools\card-check\check.py --write-sources >nul 2>&1
echo [sync] The left-out files are back in your folder, unchanged and uncommitted.
exit /b 0
:unstashclash
git reset -q
python -X utf8 tools\card-check\check.py --write-sources >nul 2>&1
echo [sync] Your left-out files are safe in git stash, but putting them back clashed. Don't delete anything - ask a chat (route B) to restore them.
exit /b 0
:unstashlater
echo [sync] A rebase is still in progress. Your left-out files are safe in git stash - ask a chat (route B) to finish the merge and restore them.
exit /b 0

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
call :run "lock guard selftest" tools\ci\lock_guard.py --selftest || exit /b 1
echo [sync] Guard: all checks passed.
exit /b 0

rem :run "<name>" <script> [args] - one check; its output goes to out\sync-check.txt and is shown only if it fails.
:run
echo [sync] Guard: %~1 ...
python -X utf8 %2 %3 %4 > out\sync-check.txt 2>&1
if errorlevel 1 (type out\sync-check.txt & echo [sync] FAILED: %~1 ^(output above, also in out\sync-check.txt^) & exit /b 1)
exit /b 0

:lockstop
echo [sync] Stopped by the lock guard: nothing was committed or pushed (see the lines above).
pause
exit /b 1
:guardfail
call :unstash
echo [sync] Stopped: a check failed. Nothing was committed or pushed. Fix it (or ask a chat), then run the same line again.
pause
exit /b 1
:guardfail2
call :unstash
echo [sync] Stopped after the pull: a check fails on the merged files. Your commit is saved here but NOT pushed.
echo [sync] Run the same sync.bat "message" line once more first. Still failing - ask a chat (route B) to fix it.
pause
exit /b 1
:pullfail
call :unstash
echo [sync] Pull failed - don't delete anything; ask a chat (route B) to help merge.
pause
exit /b 1
:pushfail
call :unstash
echo [sync] Push failed - check your internet / GitHub sign-in, or ask a chat.
pause
exit /b 1
