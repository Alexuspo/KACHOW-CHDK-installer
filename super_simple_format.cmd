@echo off
REM Super jednoduchý skript pro formátování SD karty
REM Používá pouze základní příkazy Windows

if "%1"=="" (
    echo Pouziti: %~nx0 PISMENO_DISKU
    echo Priklad: %~nx0 E:
    goto :END
)

echo.
echo ========================================
echo  KACHOW CHDK Formatter - Jednoducha verze
echo ========================================
echo.
echo Formátuji disk %1...

REM Pokusime se pouzit ruzne varianty prikazu format
echo Y | format %1 /FS:FAT32 /Q /V:"CHDK"
if %ERRORLEVEL% NEQ 0 (
    echo Zkousim alternativni format...
    echo Y | C:\Windows\System32\format.com %1 /FS:FAT32 /Q /V:"CHDK"
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo CHYBA: Formátování selhalo.
    echo Zkuste SD kartu formátovat ručně přes Průzkumník Windows.
    echo.
    goto :END
)

echo.
echo Formátování dokončeno!
echo.
echo Nastavuji bootovatelnost SD karty...

REM Vytvoření BOOTDISK.BIN souboru a nastavení jako skrytý
if exist %1\BOOTDISK.BIN (
    echo Soubor BOOTDISK.BIN již existuje
) else (
    echo. > %1\BOOTDISK.BIN
    attrib +h %1\BOOTDISK.BIN
    echo Soubor BOOTDISK.BIN vytvořen a nastaven jako skrytý
)

REM Vytvoření složky DCIM
if exist %1\DCIM (
    echo Složka DCIM již existuje
) else (
    mkdir %1\DCIM
    echo Složka DCIM vytvořena
)

echo.
echo SD karta je nyní připravena pro CHDK!

:END
echo.
echo Stiskněte libovolnou klávesu pro ukončení...
pause > nul
