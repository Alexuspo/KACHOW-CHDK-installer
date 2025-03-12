@echo off
REM DIRECT SD CARD FORMATTER - NEJJEDNODUŠŠÍ VERZE
setlocal enabledelayedexpansion

REM Kontrola parametrů
if "%1"=="" (
    echo Chyba: Zadejte písmeno disku!
    echo Příklad: %~nx0 E
    pause
    exit /b 1
)

REM Příprava písmene disku (s dvojtečkou)
set DRIVE=%1
if not "%DRIVE:~1,1%"==":" set DRIVE=%DRIVE%:

REM Kontrola existence disku
if not exist %DRIVE%\ (
    echo Chyba: Disk %DRIVE% není dostupný.
    pause
    exit /b 2
)

echo.
echo *************************************************
echo * POZOR! VŠECHNA DATA NA %DRIVE% BUDOU SMAZÁNA! *
echo *************************************************
echo.
set /p CONFIRM=Opravdu chcete formátovat disk %DRIVE%? (ano/ne): 
if /i not "%CONFIRM%"=="ano" exit /b 0

echo.
echo Formátování %DRIVE% na FAT32...
echo Y | format %DRIVE% /FS:FAT32 /Q /V:"CHDK"
echo.

if %ERRORLEVEL% NEQ 0 (
    echo Formátování selhalo
    echo Otevírám standardní dialog pro formátování...
    explorer.exe %DRIVE%\
    
    echo Pokračujte formátováním kliknutím pravým tlačítkem na disk %DRIVE% a výběrem "Formátovat..."
    pause
) else (
    echo Formátování úspěšně dokončeno!
)

echo.
echo Nastavuji bootovatelnost pro CHDK...
if not exist %DRIVE%\BOOTDISK.BIN echo. > %DRIVE%\BOOTDISK.BIN
attrib +h %DRIVE%\BOOTDISK.BIN
if not exist %DRIVE%\DCIM mkdir %DRIVE%\DCIM

echo.
echo === Hotovo! SD karta je připravena pro CHDK ===
echo.
pause
