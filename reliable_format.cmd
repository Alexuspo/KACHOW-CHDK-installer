@echo off
title KACHOW CHDK Formatter - Reliable Format
color 0A
echo ==========================================================
echo              KACHOW CHDK SD CARD FORMATTER
echo ==========================================================
echo.

REM Kontrola argumentu
if "%~1"=="" (
    echo Chyba: Nebyl zadán disk k formátování
    echo Použití: %~nx0 [písmeno_disku]
    echo Příklad: %~nx0 E:
    pause
    exit /b 1
)

set DRIVE=%~1
if not "%DRIVE:~1,1%"==":" set DRIVE=%DRIVE%:

echo VAROVÁNÍ: Všechna data na disku %DRIVE% budou smazána!
echo.
set /p CONFIRM=Chcete pokračovat s formátováním (A/N)? 
if /i not "%CONFIRM%"=="A" (
    echo Formátování zrušeno.
    pause
    exit /b 0
)

echo.
echo Formátování disku %DRIVE% na FAT32...
echo Tento proces může trvat několik minut, prosím čekejte.
echo.

REM První pokus - používáme FORMAT příkaz
echo [1/3] Pokus o formátování pomocí příkazu FORMAT...
echo Y | format %DRIVE% /FS:FAT32 /Q /X /V:"CHDK" > nul
if %ERRORLEVEL% equ 0 (
    goto :check_success
)

REM Druhý pokus - PowerShell Format-Volume
echo [2/3] První metoda selhala, zkouším PowerShell...
powershell -Command "Format-Volume -DriveLetter '%DRIVE:~0,1%' -FileSystem FAT32 -NewFileSystemLabel 'CHDK' -Confirm:$false" > nul 2>&1
if %ERRORLEVEL% equ 0 (
    goto :check_success
)

REM Třetí pokus - diskpart
echo [3/3] PowerShell selhal, zkouším diskpart...
echo select volume %DRIVE:~0,1%> "%TEMP%\diskpart_format.txt"
echo format fs=fat32 quick label="CHDK">> "%TEMP%\diskpart_format.txt"
echo exit>> "%TEMP%\diskpart_format.txt"

diskpart /s "%TEMP%\diskpart_format.txt" > nul
if exist "%TEMP%\diskpart_format.txt" del "%TEMP%\diskpart_format.txt"

:check_success
REM Ověření, zda formátování proběhlo úspěšně
echo.
echo Ověřuji, zda bylo formátování úspěšné...

REM Kontrola existence disku a souborového systému
vol %DRIVE% | find "FAT" > nul
if %ERRORLEVEL% equ 0 (
    echo.
    echo [ÚSPĚCH] Disk %DRIVE% byl úspěšně naformátován!
    
    echo.
    echo Nastavuji bootovatelnost pro CHDK...
    if not exist %DRIVE%\BOOTDISK.BIN (
        echo. > %DRIVE%\BOOTDISK.BIN
        attrib +h %DRIVE%\BOOTDISK.BIN
        echo - Vytvořen boot soubor
    ) else (
        echo - Boot soubor již existuje
    )
    
    if not exist %DRIVE%\DCIM (
        mkdir %DRIVE%\DCIM
        echo - Vytvořena DCIM složka
    ) else (
        echo - DCIM složka již existuje
    )
    
    echo.
    echo SD karta je nyní připravena pro instalaci CHDK!
    echo.
    exit /b 0
) else (
    echo.
    echo [CHYBA] Formátování se nezdařilo.
    echo Zkuste prosím naformátovat SD kartu ručně pomocí Průzkumníka Windows
    echo (pravý klik na disk %DRIVE% -> Formátovat -> vyberte FAT32).
    echo.
    echo Po ručním formátování spusťte funkci "Nastavit bootovatelnost" v aplikaci.
    echo.
    pause
    exit /b 1
)
