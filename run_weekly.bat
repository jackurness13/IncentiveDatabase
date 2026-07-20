@echo off
REM Weekly Energy Efficiency Incentives Database Updater
REM Schedule via Windows Task Scheduler: every Monday at 7:00 AM
REM Action: Start a program → path to this .bat file

cd /d "%~dp0"
python fetch_incentives.py >> run_log.txt 2>&1
