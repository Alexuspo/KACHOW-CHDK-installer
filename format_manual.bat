@echo off
title KACHOW CHDK Formatter - Manual Mode
echo KACHOW CHDK Formatter - Manual Mode
echo ================================
echo.

if "%1"=="" (
    echo Pouziti: %0 [pismeno_disku] (napriklad E)
    goto :prompt
)

set DRIVE=%1
goto :format

:prompt
set /p DRIVE=Zadejte pismeno disku SD karty (napr. E): 

:format
echo.
echo POZOR! Veskery obsah disku %DRIVE%: bude smazan!
echo.

set /p CONFIRM=Opravdu chcete formatovat disk %DRIVE%:? (A/N): 
if /i not "%CONFIRM%"=="A" goto :end

echo.
echo Formatuji disk %DRIVE%:...
echo.

REM Pokus 1: PowerShell
echo Pokus o formatovani pomoci PowerShell...
powershell -Command "Format-Volume -DriveLetter %DRIVE% -FileSystem FAT32 -NewFileSystemLabel 'CHDK' -Confirm:$false" > nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo PowerShell formatovani uspesne!
    goto :bootable
)

echo PowerShell formatovani selhalo, zkousim diskpart...

REM Pokus 2: Diskpart
echo select volume %DRIVE% > diskpart_script.txt
echo format fs=fat32 quick label="CHDK" >> diskpart_script.txt
echo exit >> diskpart_script.txt

diskpart /s diskpart_script.txt
if %ERRORLEVEL% equ 0 (
    echo Diskpart formatovani uspesne!
    del diskpart_script.txt
    goto :bootable
)

del diskpart_script.txt

REM Pokus 3: CMD Format
echo Zkousim prikaz format...
echo Y | format %DRIVE%: /FS:FAT32 /Q /X /V:"CHDK"
if %ERRORLEVEL% equ 0 (
    echo Format prikaz uspesne proveden!
    goto :bootable
)

echo.
echo Vsechny pokusy o formatovani selhaly.
echo Zkuste formatovat disk rucne v Pruzkumniku Windows.
echo (pravy klik na disk %DRIVE%: - Formatovat)
goto :end

:bootable
echo.
echo Nastavuji disk %DRIVE%: jako bootovatelny pro CHDK...
if not exist %DRIVE%:\BOOTDISK.BIN (
    echo. > %DRIVE%:\BOOTDISK.BIN
    attrib +h %DRIVE%:\BOOTDISK.BIN
)

if not exist %DRIVE%:\DCIM (
    mkdir %DRIVE%:\DCIM
)

echo.
echo Disk %DRIVE%: je nyni pripraven pro CHDK!
echo Stisknete Enter pro ukonceni...

:end
pause
