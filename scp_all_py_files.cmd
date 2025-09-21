@echo off
setlocal enabledelayedexpansion

:: MONAY Complete Python Files Transfer Script
:: Transfers ALL .py files excluding virtual environments and dependencies
:: Usage: Double-click or run: scp_all_py_files.cmd

echo.
echo ================================================
echo 🔥 MONAY Complete Python Files Transfer
echo ================================================
echo.

:: Configuration
set "SERVER=george@94.72.111.253"
set "REMOTE_DIR=/opt/monay"
set "LOCAL_DIR=%cd%"
set "TEMP_LIST=temp_py_files.txt"
set "SCP_BATCH_SIZE=50"

:: Create staging directory on server
echo 📡 Creating remote staging directory...
ssh %SERVER% "mkdir -p %REMOTE_DIR%/staging"

:: Clean up any existing file list
if exist %TEMP_LIST% del %TEMP_LIST%

echo 🔍 Finding all Python files (excluding venvs, __pycache__, etc.)...

:: Find all .py files excluding virtual environments and cache directories
for /r %LOCAL_DIR% %%f in (*.py) do (
    set "FILE_PATH=%%f"
    set "REL_PATH=%%f"
    set "REL_PATH=!REL_PATH:%LOCAL_DIR%=!"
    
    :: Skip virtual environments and cache directories
    if not "!FILE_PATH!"=="!FILE_PATH:venv=!" (
        if not "!FILE_PATH!"=="!FILE_PATH:__pycache__=!" (
            if not "!FILE_PATH!"=="!FILE_PATH:.git=!" (
                if not "!FILE_PATH!"=="!FILE_PATH:Lib\site-packages=!" (
                    echo !REL_PATH!>>%TEMP_LIST%
                )
            )
        )
    )
)

echo 📊 Found Python files:
type %TEMP_LIST%

:: Count total files
set "TOTAL_FILES=0"
for /f %%i in (%TEMP_LIST%) do set /a TOTAL_FILES+=1
echo.
echo 📁 Total Python files to transfer: %TOTAL_FILES%

:: Create directory structure on remote server
echo 📂 Creating remote directory structure...
for /f %%i in (%TEMP_LIST%) do (
    set "DIR_PATH=%%~pi"
    if not "!DIR_PATH!"=="" (
        ssh %SERVER% "mkdir -p %REMOTE_DIR%/staging!DIR_PATH!"
    )
)

echo 🚀 Starting SCP transfer...
set "CURRENT_BATCH=0"
set "BATCH_COUNT=0"
set "SUCCESS_COUNT=0"
set "ERROR_COUNT=0"

:: Transfer files in batches
for /f %%i in (%TEMP_LIST%) do (
    set /a CURRENT_BATCH+=1
    set /a BATCH_COUNT+=1
    
    :: Extract relative path
    set "REL_PATH=%%i"
    set "LOCAL_FILE=%LOCAL_DIR%!REL_PATH!"
    set "REMOTE_FILE=%REMOTE_DIR%/staging!REL_PATH!"
    
    :: Replace backslashes with forward slashes for SCP
    set "REMOTE_FILE=!REMOTE_FILE:\=/!"
    set "LOCAL_FILE=!LOCAL_FILE:\=/!"
    
    echo 📤 Transferring [!CURRENT_BATCH!/%TOTAL_FILES%]: !REL_PATH!
    
    scp "!LOCAL_FILE!" "%SERVER%:!REMOTE_FILE!"
    if !errorlevel! neq 0 (
        echo ❌ Failed: !REL_PATH!
        set /a ERROR_COUNT+=1
    ) else (
        echo ✅ Success: !REL_PATH!
        set /a SUCCESS_COUNT+=1
    )
    
    :: Small delay to prevent overwhelming
    timeout /t 1 /nobreak >nul
)

echo.
echo ================================================
echo 📊 Transfer Summary
set /a TOTAL_TRANSFERRED=%SUCCESS_COUNT%+%ERROR_COUNT%
echo Total files: %TOTAL_FILES%
echo Transferred: %SUCCESS_COUNT%
echo Failed: %ERROR_COUNT%
echo ================================================

:: Clean up
if exist %TEMP_LIST% del %TEMP_LIST%

echo.
echo 🎯 Transfer complete! Files are in: %REMOTE_DIR%/staging

echo.
echo 🔗 Next steps:
echo 1. SSH to server: ssh %SERVER%
echo 2. Navigate to staging: cd %REMOTE_DIR%/staging
echo 3. Move files to final location as needed

:: Optional: Create a verification script on the server
echo 📋 Creating verification script on server...
ssh %SERVER% "echo '#!/bin/bash' > %REMOTE_DIR%/verify_transfer.sh && echo 'echo \"🔍 Verifying MONAY Python files...\"' >> %REMOTE_DIR%/verify_transfer.sh && echo 'find %REMOTE_DIR%/staging -name \"*.py\" -type f | wc -l' >> %REMOTE_DIR%/verify_transfer.sh && echo 'echo \"✅ Verification complete!\"' >> %REMOTE_DIR%/verify_transfer.sh && chmod +x %REMOTE_DIR%/verify_transfer.sh"

echo.
echo 🎉 All done! Run this on server to verify: %REMOTE_DIR%/verify_transfer.sh
pause