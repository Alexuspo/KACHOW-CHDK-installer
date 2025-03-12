@echo off
setlocal EnableDelayedExpansion

REM Vytvoření diskpart skriptu
set DISK_SCRIPT="%TEMP%\diskpart_script.txt"

REM Získání písmene disku bez dvojtečky
set DRIVE=%1
if "%DRIVE:~-1%"==":" set DRIVE=%DRIVE:~0,-1%

REM Kontrola, zda bylo zadáno písmeno disku
if "%DRIVE%"=="" (
    echo Chyba: Nezadáno písmeno disku.
    exit /b 1
)

echo Formátování disku %DRIVE%: na FAT32...

REM Vytvoření skriptu pro diskpart
echo select volume %DRIVE% > %DISK_SCRIPT%
echo clean >> %DISK_SCRIPT%
echo create partition primary >> %DISK_SCRIPT%
echo format fs=fat32 quick label="CHDK" >> %DISK_SCRIPT%
echo assign letter=%DRIVE% >> %DISK_SCRIPT%
echo exit >> %DISK_SCRIPT%

REM Spuštění diskpart s vytvořeným skriptem
diskpart /s %DISK_SCRIPT%

REM Kontrola úspěšnosti
if %ERRORLEVEL% neq 0 (
    echo Chyba při formátování disku %DRIVE%:
    del %DISK_SCRIPT%
    exit /b 1
)

echo Formátování dokončeno úspěšně.
del %DISK_SCRIPT%
exit /b 0
