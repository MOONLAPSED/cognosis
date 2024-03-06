:: This batch file sets up the environment for the sandbox init process
:: It adds Scoop to the PATH and launches the rollout script.

@echo off

:: Add Scoop to PATH for this session 
set PATH=%PATH%;C:\Users\WDAGUtilityAccount\AppData\Local\Programs\Scoop\bin

:: Introduce a delay of 3 seconds
ping 127.0.0.1 -n 4 > nul

:: Check if Scoop is in the PATH
echo %PATH% | findstr /i /c:"C:\Users\WDAGUtilityAccount\AppData\Local\Programs\Scoop\bin" > nul

IF %ERRORLEVEL% EQU 0 (
    :: Scoop is in the PATH, proceed with the rollout script
    powershell.exe -ExecutionPolicy Bypass -Command "scoop install git; & 'C:\Users\WDAGUtilityAccount\Desktop\scoop.ps1'"
) ELSE (
    :: Scoop is not in the PATH, handle the error or take appropriate action
    echo Scoop is not in the PATH. Please check the installation.
    goto :retry
)

:: Check if the previous command failed
IF %ERRORLEVEL% NEQ 0 (
    :: Previous command failed, try executing scoop.cmd instead
    powershell.exe -ExecutionPolicy Bypass -Command "try { & 'C:\Users\WDAGUtilityAccount\Desktop\scoop.cmd' } catch { Write-Host 'Failed to execute scoop.cmd' }"
)

:retry
:: Retry logic
echo Retrying...
ping 127.0.0.1 -n 4 > nul
goto :EOF

