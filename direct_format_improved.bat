@echo off
title KACHOW CHDK SD CARD FORMATTER
color 0A
mode con: cols=80 lines=30
setlocal EnableDelayedExpansion

REM ========================
REM  VYLEPŠENÁ VERZE FORMÁTOVAČE
REM ========================

echo.
echo ********************************************************
echo *            KACHOW CHDK SD CARD FORMATTER             *
echo ********************************************************
echo.

REM Kontrola parametrů
if "%1"=="" (
    echo CHYBA: Nebyl zadán disk k formátování!
    echo.
    echo Použití: %0 [písmeno_disku]
    echo Příklad: %0 E:
    echo.
    pause
    exit /b 1
)

REM Příprava písmene disku
set DRIVE=%1
if not "%DRIVE:~1,1%"==":" set DRIVE=%DRIVE%:

REM Kontrola existence disku
if not exist %DRIVE%\ (
    echo CHYBA: Disk %DRIVE% není dostupný!
    echo.
    pause
    exit /b 2
)

echo Informace o disku:
echo ------------------
echo.
vol %DRIVE%
echo.
fsutil fsinfo drives | find "%DRIVE%"
echo.

REM Potvrzení od uživatele
echo ===================== VAROVÁNÍ =====================
echo VŠECHNA DATA NA DISKU %DRIVE% BUDOU SMAZÁNA!
echo ==================================================
echo.
echo 1. Ujistěte se, že jste vybrali správnou SD kartu
echo 2. Ujistěte se, že karta neobsahuje důležitá data
echo.
set /p CONFIRM=Přejete si pokračovat s formátováním? (ano/ne): 
if /i not "%CONFIRM%"=="ano" (
    echo.
    echo Formátování bylo zrušeno.
    pause
    exit /b 0
)

echo.
echo -----------------------------------------
echo       Průběh formátování
echo -----------------------------------------

echo.
echo [1/3] Začínám formátovat disk %DRIVE% na FAT32...
echo.

REM Pokus č.1: FORMAT příkaz
echo Y | format %DRIVE% /FS:FAT32 /Q /X /V:"CHDK"
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Formátování bylo úspěšné!
    goto :make_bootable
)

echo.
echo ❌ Běžné formátování selhalo, zkouším alternativní metody...

REM Pokus č.2: Diskpart
echo.
echo [2/3] Zkouším formátovat pomocí Diskpart...
echo.

echo select volume %DRIVE:~0,1%> "%TEMP%\chdk_diskpart.txt"
echo format fs=fat32 quick label="CHDK">> "%TEMP%\chdk_diskpart.txt"
echo exit>> "%TEMP%\chdk_diskpart.txt"

diskpart /s "%TEMP%\chdk_diskpart.txt"
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Formátování pomocí Diskpart bylo úspěšné!
    del "%TEMP%\chdk_diskpart.txt" 2>nul
    goto :make_bootable
)

del "%TEMP%\chdk_diskpart.txt" 2>nul

REM Pokus č.3: PowerShell
echo.
echo [3/3] Zkouším formátovat pomocí PowerShell...
echo.

powershell -Command "Format-Volume -DriveLetter '%DRIVE:~0,1%' -FileSystem FAT32 -NewFileSystemLabel 'CHDK' -Force -Confirm:$false"
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Formátování pomocí PowerShell bylo úspěšné!
    goto :make_bootable
)

echo.
echo ❌ Všechny pokusy o automatické formátování selhaly!
echo.
echo Otevírám průzkumník pro ruční formátování...
explorer.exe %DRIVE%\

echo.
echo ℹ️ Postupujte následovně:
echo 1. Pravým tlačítkem klikněte na disk %DRIVE%
echo 2. Vyberte možnost "Formátovat..."
echo 3. Vyberte formát "FAT32"
echo 4. Nastavte popisek svazku: "CHDK"
echo 5. Klikněte na "Spustit" a poté na "OK"
echo.
echo Po ručním formátování se vraťte do tohoto okna a stiskněte ENTER...
pause > nul

:make_bootable
echo.
echo -----------------------------------------
echo       Nastavení bootovatelnosti
echo -----------------------------------------
echo.

REM Kontrola, zda je disk skutečně naformátován
echo Kontroluji formátování...
vol %DRIVE% | find "FAT" > nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ CHYBA: Disk %DRIVE% nebyl správně naformátován na FAT32!
    echo.
    echo Zkuste provést formátování ručně v Průzkumníku Windows.
    pause
    exit /b 1
)

echo Nastavuji SD kartu jako bootovatelnou pro CHDK...
echo.

REM Vytvoření BOOTDISK.BIN
if not exist %DRIVE%\BOOTDISK.BIN (
    echo Vytvářím bootovací soubor...
    echo. > %DRIVE%\BOOTDISK.BIN
    attrib +h %DRIVE%\BOOTDISK.BIN
    echo ✅ Soubor BOOTDISK.BIN vytvořen a nastaven jako skrytý
) else (
    echo ✅ Soubor BOOTDISK.BIN již existuje
)

REM Vytvoření složky DCIM
if not exist %DRIVE%\DCIM (
    echo Vytvářím složku pro fotografie...
    mkdir %DRIVE%\DCIM
    echo ✅ Složka DCIM vytvořena
) else (
    echo ✅ Složka DCIM již existuje
)

echo.
echo ==================================================
echo             ✅ INSTALACE DOKONČENA
echo ==================================================
echo.
echo SD karta %DRIVE% je nyní připravena pro CHDK!
echo.
echo Po ukončení tohoto průvodce můžete pokračovat
echo s instalací firmwaru v hlavní aplikaci.
echo.

pause
exit /b 0
