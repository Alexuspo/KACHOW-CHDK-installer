@echo off
echo Spouštím KACHOW CHDK Installer s právy správce...

REM Zjistí, zda byla zadána písmeno disku pro přímé formátování
IF "%~1"=="" (
    REM Spuštění hlavní aplikace
    powershell -Command "Start-Process cmd -ArgumentList '/c python main.py' -Verb RunAs -WorkingDirectory '%~dp0'"
) ELSE (
    REM Spuštění konzolové verze s parametrem (písmeno disku)
    echo Formátování disku %~1 ...
    powershell -Command "Start-Process cmd -ArgumentList '/c python console_formatter.py %~1' -Verb RunAs -WorkingDirectory '%~dp0'"
)

echo Aplikace by měla být nyní spuštěna s právy správce.
