@echo off
title KACHOW CHDK Formatter - Formátování
echo ================================
echo  KACHOW CHDK Formatter
echo ================================
echo.

if "%1"=="" (
    echo Chyba: Nezadáno písmeno disku
    echo Použití: %0 [písmeno_disku]
    echo Příklad: %0 E:
    pause
    exit /b 1
)

echo Formátuji disk %1 na FAT32...
echo Tento proces může trvat několik minut podle velikosti SD karty.
echo.
echo UPOZORNĚNÍ: VŠECHNA data na disku %1 budou SMAZÁNA!
echo.

REM Formát bez interaktivní výzvy
echo Y | format %1 /FS:FAT32 /Q /X /V:"CHDK"

echo.
if %ERRORLEVEL% NEQ 0 (
    echo Chyba při formátování disku %1
    echo Zkuste disk formátovat ručně přes Průzkumníka Windows.
    pause
    exit /b 1
)

echo Formátování dokončeno úspěšně!
echo.
echo Nastavuji disk jako bootovatelný pro CHDK...

REM Nastavení bootovatelnosti
echo. > %1\BOOTDISK.BIN
attrib +h %1\BOOTDISK.BIN

if not exist %1\DCIM mkdir %1\DCIM

echo.
echo SD karta je nyní připravena pro instalaci CHDK!
echo.
echo Můžete zavřít toto okno a pokračovat v aplikaci.
pause
exit /b 0
