@echo off
echo Jednoduchy script pro formatovani SD karty
IF "%~1"=="" (
    echo Pouziti: %0 [pismeno_disku:]
    echo Priklad: %0 E:
    exit /b 1
)

echo Formatovani %~1 na FAT32...
echo Y | format %~1 /FS:FAT32 /Q /X /V:"CHDK"

IF %ERRORLEVEL% NEQ 0 (
    echo Chyba pri formatovani %~1
    exit /b 1
)

echo Formatovani uspesne dokonceno.
exit /b 0
