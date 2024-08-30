@echo off
set SIGNTOOL="C:\Program Files (x86)\Windows Kits\10\bin\10.0.26100.0\x64\signtool.exe"
set CERT_PATH="C:\Users\marsh\PycharmProjects\RNGwall\RNGwallCert.pfx"
set TIMESTAMP_SERVER="http://timestamp.digicert.com"
set EXE_PATH="C:\Users\marsh\PycharmProjects\RNGwall\installer_output\RNGwall_setup_1.0_x64.exe"

%SIGNTOOL% sign /f %CERT_PATH% /p Obzen311! /fd SHA256 /t %TIMESTAMP_SERVER% %EXE_PATH%

if %ERRORLEVEL% EQU 0 (
    echo Signing successful.
    %SIGNTOOL% verify /pa /v %EXE_PATH%
) else (
    echo Signing failed. Error code: %ERRORLEVEL%
)

pause