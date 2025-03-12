"""
Spustí aplikaci KACHOW CHDK Installer s právy administrátora
"""

import os
import sys
import ctypes
import subprocess

def run_as_admin():
    """
    Pokusí se spustit aplikaci main.py s právy administrátora
    """
    print("Spouštím KACHOW CHDK Installer s právy správce...")
    
    # Zjistíme aktuální adresář
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Cesta k Python interpreteru
    python_exe = sys.executable
    
    # Cesta k hlavnímu skriptu aplikace
    main_script = os.path.join(current_dir, "main.py")
    
    # Pokusíme se spustit aplikaci s právy admina
    try:
        if sys.platform == 'win32':
            # Ve Windows použijeme ShellExecute s parametrem "runas"
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", python_exe, f'"{main_script}"', current_dir, 1
            )
            return True
        else:
            # Na jiných platformách zkusíme 'sudo'
            subprocess.Popen(['sudo', python_exe, main_script])
            return True
    except Exception as e:
        print(f"Chyba při pokusu o spuštění s právy správce: {str(e)}")
        input("Stiskněte Enter pro ukončení...")
        return False

if __name__ == "__main__":
    run_as_admin()
