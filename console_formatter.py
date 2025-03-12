"""
Jednoduchý skript pro formátování SD karty z příkazové řádky
Použití: python console_formatter.py <písmeno_disku>
Příklad: python console_formatter.py E:
"""

import sys
import os
import subprocess
from sd_operations import make_bootable, is_admin

def format_disk_direct(drive_letter):
    """Pokus o přímé formátování disku bez použití sd_operations"""
    print(f"Formátování disku {drive_letter} pomocí speciálního skriptu...")
    
    # Cesta k CMD skriptu
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "super_simple_format.cmd")
    
    # Kontrola, zda soubor existuje
    if not os.path.exists(script_path):
        print(f"Skript {script_path} neexistuje. Vytvářím nový...")
        
        # Pokud skript neexistuje, vytvoříme ho
        with open(script_path, 'w') as f:
            f.write('@echo off\n')
            f.write('REM Super jednoduchý skript pro formátování SD karty\n')
            f.write('echo Formátuji disk %1...\n')
            f.write('echo Y | format %1 /FS:FAT32 /Q /V:"CHDK"\n')
            f.write('if %ERRORLEVEL% NEQ 0 (\n')
            f.write('    echo CHYBA: Formátování selhalo\n')
            f.write('    exit /b 1\n')
            f.write(')\n')
            f.write('echo Formátování dokončeno\n')
            f.write('echo Nastavuji bootovatelnost\n')
            f.write('echo. > %1\\BOOTDISK.BIN\n')
            f.write('attrib +h %1\\BOOTDISK.BIN\n')
            f.write('if not exist %1\\DCIM mkdir %1\\DCIM\n')
            f.write('exit /b 0\n')
    
    # Spustíme skript s pravomocemi admin (pokud ještě nejsme admin)
    try:
        cmd_exe = r"C:\Windows\System32\cmd.exe"
        if not os.path.exists(cmd_exe):
            cmd_exe = "cmd.exe"  # Záložní varianta - spoléháme na PATH
            
        command = [cmd_exe, "/c", script_path, drive_letter]
        print(f"Spouštím příkaz: {' '.join(command)}")
        
        process = subprocess.Popen(
            command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()
        
        print(stdout)
        if stderr:
            print(f"Chyby: {stderr}")
        
        return process.returncode == 0
        
    except Exception as e:
        print(f"Při formátování nastala chyba: {str(e)}")
        return False

def main():
    print("KACHOW CHDK SD Card Formatter - Konzolová verze")
    print("=" * 50)
    
    if not is_admin():
        print("CHYBA: Tento skript musí být spuštěn s právy správce!")
        print("Zkuste spustit příkazovou řádku jako správce a zkuste to znovu.")
        return 1
    
    if len(sys.argv) < 2:
        print("Použití: python console_formatter.py <písmeno_disku>")
        print("Příklad: python console_formatter.py E:")
        return 1
    
    drive_letter = sys.argv[1]
    if not drive_letter.endswith(':'):
        drive_letter = f"{drive_letter}:"
    
    print(f"Formátování disku {drive_letter}...")
    
    try:
        # Pokus o formátování přímou metodou
        if format_disk_direct(drive_letter):
            print("Formátování úspěšně dokončeno!")
        else:
            print("Všechny metody formátování selhaly.")
            return 1
        
        print(f"Nastavuji bootovatelnost disku {drive_letter}...")
        make_bootable(drive_letter)
        print("Bootovatelnost úspěšně nastavena!")
        
        print("SD karta je připravena pro instalaci CHDK!")
        return 0
    except Exception as e:
        print(f"CHYBA: {str(e)}")
        print("Zkuste formátovat SD kartu ručně pomocí Windows a pak použijte tento nástroj jen pro nastavení bootovatelnosti.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
