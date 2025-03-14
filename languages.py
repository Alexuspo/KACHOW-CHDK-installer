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
    
    # Operace s SD kartou
    "format_button": "Formátovat SD kartu",
    "bootable_button": "Nastavit bootovatelnost",
    "format_complete": "Formátování dokončeno",
    "bootable_complete": "Bootovatelnost nastavena",
    "format_success": "SD karta byla úspěšně formátována!",
    "bootable_success": "SD karta byla úspěšně nastavena jako bootovatelná!",
    "format_error": "Chyba při formátování: {}",
    "bootable_error": "Chyba při nastavování bootovatelnosti: {}",

    # Administrátorská práva
    "admin_warning": "Aplikace není spuštěna jako správce. Formátování SD karet nemusí fungovat.",
    "restart_as_admin": "Spustit jako správce",
    "admin_required": "Vyžadována práva správce",
    "format_admin_warning": "Pro formátování SD karty jsou vyžadována práva správce. Chcete aplikaci restartovat s právy správce?",
    "admin_restart_failed": "Nepodařilo se spustit aplikaci jako správce.",

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
    "language_prompt": "Vyberte jazyk | Select language:",

    # Dialogy
    "select_firmware_file": "Vyberte stažený CHDK firmware",
    "select_folder": "Vyberte složku s CHDK",
    
    # Nové klíče
    "card_compatibility": "Zkontrolovat kompatibilitu",
    "card_compatible": "SD karta je kompatibilní",
    "card_incompatible": "SD karta není kompatibilní",
    "format_manually": "Formátujte SD kartu ručně ve Windows před použitím této aplikace.",
    "check_compatibility": "Kontrola kompatibility",
    "sd_requirements": "SD karta musí být ve formátu FAT32 a menší než 64 GB.",
    "card_too_big": "SD karta je příliš velká (max 64 GB).",
    "wrong_filesystem": "SD karta není ve formátu FAT32.",
    "manual_format_instructions": "Formátování SD karty v počítači:",
    "manual_format_steps": "1. Otevřete Průzkumník Windows\n2. Pravým tlačítkem klikněte na SD kartu\n3. Vyberte možnost 'Formátovat'\n4. V rozbalovacím seznamu vyberte 'FAT32'\n5. Klikněte na 'Spustit'",
    "firmware_custom": "Vlastní firmware (stažený z internetu)",
    "firmware_preinstalled": "Předinstalované CHDK firmware",
    "model_select": "Vyberte model fotoaparátu ze seznamu:",
    "no_preinstalled": "Žádné předinstalované firmware nejsou k dispozici",
    "add_firmware": "Přidat nový firmware do databáze",
    "model_name": "Název modelu",
    "model_name_prompt": "Zadejte název modelu fotoaparátu (např. 'PowerShot A720 IS'):",
    "model_name_empty": "Název modelu nemůže být prázdný",
    "firmware_added": "Firmware přidán",
    "firmware_added_success": "Firmware pro model {0} byl úspěšně přidán do databáze.",
    "firmware_add_error": "Nepodařilo se přidat firmware: {0}",
    "select_model": "Vyberte model fotoaparátu ze seznamu",
    "select_firmware_add": "Vyberte firmware pro přidání do databáze"
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
    
    # SD card operations
    "format_button": "Format SD card",
    "bootable_button": "Make bootable",
    "format_complete": "Formatting complete",
    "bootable_complete": "Bootable setup complete",
    "format_success": "SD card was successfully formatted!",
    "bootable_success": "SD card was successfully set as bootable!",
    "format_error": "Error while formatting: {}",
    "bootable_error": "Error while setting bootability: {}",

    # Administrator rights
    "admin_warning": "The application is not running as administrator. SD card formatting may not work.",
    "restart_as_admin": "Run as administrator",
    "admin_required": "Administrator rights required",
    "format_admin_warning": "Administrator rights are required to format the SD card. Do you want to restart the application with administrator rights?",
    "admin_restart_failed": "Failed to restart the application as administrator.",

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
    "language_prompt": "Select language | Vyberte jazyk:",

    # Dialogs
    "select_firmware_file": "Select downloaded CHDK firmware",
    "select_folder": "Select CHDK folder",
    
    # Nové klíče
    "card_compatibility": "Check compatibility",
    "card_compatible": "SD card is compatible",
    "card_incompatible": "SD card is not compatible",
    "format_manually": "Format the SD card manually in Windows before using this application.",
    "check_compatibility": "Compatibility check",
    "sd_requirements": "SD card must be in FAT32 format and less than 64 GB.",
    "card_too_big": "SD card is too large (max 64 GB).",
    "wrong_filesystem": "SD card is not in FAT32 format.",
    "manual_format_instructions": "Formatting SD card on your computer:",
    "manual_format_steps": "1. Open Windows Explorer\n2. Right-click on the SD card\n3. Select 'Format'\n4. From the dropdown menu, select 'FAT32'\n5. Click 'Start'",
    "firmware_custom": "Custom firmware (downloaded from internet)",
    "firmware_preinstalled": "Pre-installed CHDK firmware",
    "model_select": "Select camera model from the list:",
    "no_preinstalled": "No pre-installed firmware available",
    "add_firmware": "Add new firmware to database",
    "model_name": "Model name",
    "model_name_prompt": "Enter camera model name (e.g. 'PowerShot A720 IS'):",
    "model_name_empty": "Model name cannot be empty",
    "firmware_added": "Firmware added",
    "firmware_added_success": "Firmware for model {0} has been successfully added to the database.",
    "firmware_add_error": "Failed to add firmware: {0}",
    "select_model": "Select camera model from the list",
    "select_firmware_add": "Select firmware to add to the database"
}
