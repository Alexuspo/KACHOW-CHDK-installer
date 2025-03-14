"""
Tento skript připraví prostředí pro KACHOW CHDK Installer.
Spusťte tento skript před prvním použitím aplikace.

Copyright © 2025 Alexuspo
GitHub: https://github.com/Alexuspo/KACHOW-CHDK-installer
"""

import os
import sys
import subprocess

def main():
    print("Příprava prostředí pro KACHOW CHDK Installer...")  # Změněn název
    
    # Vytvoření potřebných složek
    required_dirs = [
        "assets",
        "chdk_models"
    ]
    
    for directory in required_dirs:
        if not os.path.exists(directory):
            print(f"Vytvářím složku: {directory}")
            os.makedirs(directory)
    
    # Kontrola požadovaných balíčků
    print("Instalace požadovaných balíčků...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Balíčky úspěšně nainstalovány.")
    except Exception as e:
        print(f"Varování: Nepodařilo se nainstalovat balíčky: {str(e)}")
    
    # Příprava adresáře s ukázkovými modely
    try:
        from setup_models_directory import setup_models_directory
        setup_models_directory()
    except Exception as e:
        print(f"Varování: Nepodařilo se připravit ukázkové modely: {str(e)}")
        print("Pro vytvoření ukázkových modelů spusťte skript setup_models_directory.py")
    
    print("\nProstředí připraveno. Nyní můžete spustit aplikaci pomocí 'python main.py'.")
    
    # Vytvoření prázdného souboru ikony, pokud neexistuje
    icon_path = os.path.join("assets", "icon.ico")
    if not os.path.exists(icon_path):
        print(f"Vytvářím prázdnou ikonu v {icon_path}")
        with open(icon_path, 'wb') as f:
            # Minimální validní .ico soubor
            f.write(b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x04\x00\x28\x01\x00\x00\x16\x00\x00\x00\x28\x00\x00\x00\x10\x00\x00\x00\x20\x00\x00\x00\x01\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')

    print("\nVytvořte logo.png ve složce assets pro lepší vzhled aplikace.")
    input("Stiskněte Enter pro ukončení...")

if __name__ == "__main__":
    main()
