@echo off
title KACHOW CHDK Formatter
echo ************************************************
echo * KACHOW CHDK Formatter - SD Card Formátování *
echo ************************************************
echo.
echo Tento nástroj zformátuje SD kartu pro CHDK firmware.
echo.

REM Kontrola zda byl zadán argument
if "%1"=="" goto :PROMPT

REM Použití příkazového řádku
set DRIVE=%1
goto :FORMAT

:PROMPT
echo Dostupné vyměnitelné disky:
echo ---------------------------
set "DriveCount=0"
setlocal enabledelayedexpansion
for %%D in (A B C D E F G H I J K L M N O P Q R S T U V W X Y Z) do (
    if exist %%D:\ (
        fsutil fsinfo drivetype %%D: | find "Removable" > nul
        if !errorlevel! equ 0 (
            echo %%D:
            set /a "DriveCount+=1"
        )
    )
)

if %DriveCount% EQU 0 (
    echo Nenalezeny žádné vyměnitelné disky.
    goto :END
)
endlocal

set /p DRIVE=Zadejte písmeno disku SD karty (např. E): 

:FORMAT
REM Přidání dvojtečky, pokud chybí
if not "%DRIVE:~1,1%"==":" set DRIVE=%DRIVE%:

if not exist %DRIVE%\ (
    echo CHYBA: Disk %DRIVE% není dostupný.
    goto :END
)

echo.
echo VAROVÁNÍ: Všechna data na disku %DRIVE% budou smazána!
echo.
set /p CONFIRM=Chcete pokračovat? (A/N): 
if /i not "%CONFIRM%"=="A" goto :END

echo.
echo Formátuji disk %DRIVE%...
echo.

REM Spustíme super_simple_format.cmd s pravomocemi admin
echo Spouštím formátování...
powershell -Command "Start-Process cmd -ArgumentList '/c %~dp0super_simple_format.cmd %DRIVE%' -Verb RunAs"

echo.
echo Po dokončení formátování bude SD karta připravena pro instalaci CHDK.
echo.

:END
echo.
echo Stiskněte libovolnou klávesu pro ukončení...
pause > nul
