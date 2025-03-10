"""
Jazykové překlady pro KACHOW CHDK Installer
"""

# Český jazyk (výchozí)
CZECH = {
    # Obecné
    "app_title": "KACHOW CHDK Installer",
    "ready": "Připraven",
    "error": "Chyba",
    "success": "Úspěch",
    
    # Uvítání
    "welcome_text": "Vítejte v instalátoru KACHOW CHDK! Tento nástroj vám pomůže připravit SD kartu "
                  "s firmwarem CHDK pro váš fotoaparát Canon.",
    
    # Záložky
    "tab_install": " Instalace CHDK ",
    "tab_help": " Nápověda ",
    "tab_about": " O aplikaci ",
    
    # Instalační záložka
    "step1_title": "Krok 1: Výběr SD karty",
    "available_cards": "Dostupné SD karty:",
    "refresh": "Obnovit",
    "format_card": "Formátovat SD kartu (FAT32)",
    "format_warning": "VAROVÁNÍ: Formátování smaže všechna data z vybrané SD karty!",
    
    "step2_title": "Krok 2: Výběr firmware CHDK",
    "download_info": "Navštivte stránku https://www.mighty-hoernsche.de/ a stáhněte "
                    "firmware CHDK pro váš model fotoaparátu Canon.",
    "open_firmware_page": "Otevřít stránku s firmwarem:",
    "open_website": "Otevřít mighty-hoernsche.de",
    "downloaded_file": "Stažený soubor:",
    "browse": "Procházet",
    "install_button": "📥 Instalovat CHDK",
    
    # Stavy instalace
    "loading_drives": "Načítání disků...",
    "drives_found": "Nalezeno {} vyměnitelných disků",
    "no_drives": "Nenalezeny žádné SD karty",
    "load_drives_error": "Nepodařilo se načíst dostupné disky: {}",
    "select_card": "Vyberte prosím SD kartu",
    "select_firmware": "Vyberte platný soubor s CHDK firmwarem",
    "confirm_format": "Opravdu chcete formátovat disk {}?\n\nVŠECHNA DATA NA DISKU BUDOU SMAZÁNA!",
    "starting_install": "Zahajuji instalaci...",
    "formatting": "Formátování SD karty...",
    "making_bootable": "Nastavování bootovatelnosti...",
    "installing": "Instalace CHDK...",
    "install_complete": "Instalace dokončena",
    "install_success": "CHDK bylo úspěšně nainstalováno!",
    "install_error": "Chyba při instalaci",
    
    # Nápověda
    "help_text": """Jak používat CHDK Installer:

1. Připojte SD kartu k počítači.
2. Navštivte stránku https://www.mighty-hoernsche.de/
3. Najděte a stáhněte CHDK firmware pro váš model fotoaparátu Canon.
4. V záložce 'Instalace CHDK' vyberte správnou SD kartu.
5. Pokud chcete SD kartu formátovat (doporučeno), ponechte zaškrtnutou možnost formátování.
6. Klikněte na tlačítko 'Procházet' a vyberte stažený soubor s firmwarem.
7. Klikněte na 'Instalovat CHDK'.

Po instalaci:
1. Vložte SD kartu do fotoaparátu.
2. Zapněte fotoaparát v režimu přehrávání.
3. Aktivujte CHDK podle návodu k vašemu modelu (obvykle stisknutím tlačítka 'menu' nebo 'disp').

Další informace najdete na oficiálních stránkách CHDK: http://chdk.wikia.com/""",
    
    # O aplikaci
    "about_text": """KACHOW CHDK Installer v1.0

Aplikace pro snadnou instalaci CHDK firmwaru na SD karty.

CHDK (Canon Hack Development Kit) je neoficiální firmware
pro fotoaparáty Canon, který rozšiřuje jejich možnosti.

© 2025 Alexuspo""",
    "visit_chdk": "Navštivte oficiální web CHDK",
    "github_link": "GitHub: KACHOW-CHDK-installer",
    
    # Dialog výběru jazyka
    "language_title": "Výběr jazyka | Language Selection",
    "language_prompt": "Vyberte jazyk | Select language:"
}

# Anglický jazyk
ENGLISH = {
    # General
    "app_title": "KACHOW CHDK Installer",
    "ready": "Ready",
    "error": "Error",
    "success": "Success",
    
    # Welcome
    "welcome_text": "Welcome to the KACHOW CHDK Installer! This tool will help you prepare an SD card "
                  "with CHDK firmware for your Canon camera.",
    
    # Tabs
    "tab_install": " Install CHDK ",
    "tab_help": " Help ",
    "tab_about": " About ",
    
    # Installation tab
    "step1_title": "Step 1: Select SD Card",
    "available_cards": "Available SD cards:",
    "refresh": "Refresh",
    "format_card": "Format SD card (FAT32)",
    "format_warning": "WARNING: Formatting will erase all data on the selected SD card!",
    
    "step2_title": "Step 2: Select CHDK Firmware",
    "download_info": "Visit https://www.mighty-hoernsche.de/ and download "
                    "the CHDK firmware for your Canon camera model.",
    "open_firmware_page": "Open firmware page:",
    "open_website": "Open mighty-hoernsche.de",
    "downloaded_file": "Downloaded file:",
    "browse": "Browse",
    "install_button": "📥 Install CHDK",
    
    # Installation states
    "loading_drives": "Loading drives...",
    "drives_found": "Found {} removable drives",
    "no_drives": "No SD cards found",
    "load_drives_error": "Failed to load available drives: {}",
    "select_card": "Please select an SD card",
    "select_firmware": "Please select a valid CHDK firmware file",
    "confirm_format": "Do you really want to format drive {}?\n\nALL DATA ON THE DRIVE WILL BE ERASED!",
    "starting_install": "Starting installation...",
    "formatting": "Formatting SD card...",
    "making_bootable": "Making card bootable...",
    "installing": "Installing CHDK...",
    "install_complete": "Installation complete",
    "install_success": "CHDK has been successfully installed!",
    "install_error": "Installation error",
    
    # Help
    "help_text": """How to use CHDK Installer:

1. Connect the SD card to your computer.
2. Visit https://www.mighty-hoernsche.de/
3. Find and download the CHDK firmware for your Canon camera model.
4. In the 'Install CHDK' tab, select the correct SD card.
5. If you want to format the SD card (recommended), leave the formatting option checked.
6. Click the 'Browse' button and select the downloaded firmware file.
7. Click 'Install CHDK'.

After installation:
1. Insert the SD card into your camera.
2. Turn on the camera in playback mode.
3. Activate CHDK according to your model's instructions (usually by pressing the 'menu' or 'disp' button).

For more information, visit the official CHDK website: http://chdk.wikia.com/""",
    
    # About
    "about_text": """KACHOW CHDK Installer v1.0

An application for easy installation of CHDK firmware on SD cards.

CHDK (Canon Hack Development Kit) is an unofficial firmware
for Canon cameras that extends their capabilities.

© 2025 Alexuspo""",
    "visit_chdk": "Visit the official CHDK website",
    "github_link": "GitHub: KACHOW-CHDK-installer",
    
    # Language selection dialog
    "language_title": "Language Selection | Výběr jazyka",
    "language_prompt": "Select language | Vyberte jazyk:"
}
