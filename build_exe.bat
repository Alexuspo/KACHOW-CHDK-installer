@echo off
echo Vytváření spustitelného souboru KACHOW CHDK Installer...
echo.

REM Kontrola existence PyInstalleru
pip show pyinstaller >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo PyInstaller není nainstalován. Instaluji...
    pip install pyinstaller
    if %ERRORLEVEL% NEQ 0 (
        echo Nepodařilo se nainstalovat PyInstaller!
        pause
        exit /b 1
    )
)

REM Vytvoření EXE souboru
pyinstaller --onefile ^
            --windowed ^
            --icon=assets/icon.ico ^
            --add-data "assets;assets" ^
            --add-data "chdk_models;chdk_models" ^
            --add-data "reliable_format.cmd;." ^
            --add-data "super_simple_format.cmd;." ^
            --name "KACHOW_CHDK_Installer" ^
            main.py

if %ERRORLEVEL% NEQ 0 (
    echo Nepodařilo se vytvořit EXE soubor!
    pause
    exit /b 1
)

echo.
echo Spustitelný soubor byl vytvořen ve složce dist/KACHOW_CHDK_Installer.exe
echo.

REM Kopírování dodatečných potřebných souborů do složky dist
echo Kopíruji dodatečné soubory...
xcopy /y "reliable_format.cmd" "dist\"
xcopy /y "super_simple_format.cmd" "dist\"

echo.
echo Sestavení dokončeno!
pause
