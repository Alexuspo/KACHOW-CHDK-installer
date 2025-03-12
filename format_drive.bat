@echo off
echo Formátování %1 jako FAT32...
echo Y | format %1 /FS:FAT32 /Q /X /V:"CHDK"
if %ERRORLEVEL% neq 0 (
    echo Chyba při formátování %1
    exit /b 1
)
echo Formátování bylo dokončeno úspěšně.
exit /b 0
