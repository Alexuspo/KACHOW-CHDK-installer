import os
import subprocess
import win32api
import win32file
import win32con
import ctypes
import sys

def get_drives():
    """Vrátí seznam dostupných vyměnitelných disků (SD karet)"""
    drives = []
    bitmask = win32api.GetLogicalDrives()
    
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        if bitmask & 1:
            drive_path = f"{letter}:\\"
            try:
                drive_type = win32file.GetDriveType(drive_path)
                if (drive_type == win32file.DRIVE_REMOVABLE):
                    drives.append(f"{letter}:")
            except:
                pass
        bitmask >>= 1
    
    return drives

def format_drive_to_fat32(drive_letter):
    """Formátuje vybraný disk na souborový systém FAT32"""
    if not drive_letter or not drive_letter.endswith(':'):
        raise ValueError("Neplatné označení disku")
    
    # Kontrola, zda má uživatel administrátorská práva
    if not is_admin():
        raise PermissionError("Pro formátování je nutné spustit aplikaci jako správce")
    
    # Velmi jednoduchý přístup k formátování - spustit přímý dávkový soubor
    try:
        # Cesta k nejjednoduššímu formátovacímu dávkovému souboru
        batch_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "direct_format.bat")
        
        # Pokud soubor neexistuje, vytvoříme ho
        if not os.path.exists(batch_path):
            with open(batch_path, 'w') as f:
                f.write('@echo off\necho Formátování %1...\necho Y | format %1 /FS:FAT32 /Q /V:"CHDK"\n')
                f.write('if not exist %1\\BOOTDISK.BIN echo. > %1\\BOOTDISK.BIN\n')
                f.write('attrib +h %1\\BOOTDISK.BIN\n')
                f.write('if not exist %1\\DCIM mkdir %1\\DCIM\n')
        
        # Spustíme dávkový soubor v samostatném okně, které se nezavře po dokončení
        os.system(f'start "" "{batch_path}" {drive_letter}')
        
        # Dáme uživateli vědět, že formátování probíhá v samostatném okně.
        print(f"Formátování disku {drive_letter} bylo spuštěno v samostatném okně.")
        print("Po dokončení formátování pokračujte v aplikaci kliknutím na tlačítko.")
        
        # Jelikož jsme spustili proces samostatně, nehrozí timeout
        return True
    
    except Exception as e:
        raise RuntimeError(f"Chyba při spouštění formátování: {str(e)}")

def is_drive_formatted_as_fat32(drive_letter):
    """Kontroluje, zda je disk naformátován jako FAT32"""
    try:
        # Zkontrolujeme, zda disk obsahuje souborový systém FAT32
        result = subprocess.run(['cmd', '/c', 'vol', drive_letter], 
                            capture_output=True, text=True, timeout=5)
        
        output = result.stdout.lower()
        
        # Pokud je v názvu svazku "fat32", je to FAT32
        if "fat32" in output:
            return True
            
        # Další kontrola pomocí fsutil
        result = subprocess.run(['fsutil', 'fsinfo', 'volumeinfo', drive_letter], 
                            capture_output=True, text=True, timeout=5)
                            
        output = result.stdout.lower()
        return "fat32" in output or "fat" in output
    except:
        return False

def show_format_dialog(drive_letter):
    """Zobrazí standardní dialogové okno pro formátování"""
    try:
        shell_command = f'start explorer.exe shell:::{{{0xed7ba470, 0x8e54, 0x465e, 0x82, 0x5c, 0x99, 0x72, 0x03, 0x88, 0x9d, 0x57}}} ' + drive_letter
        subprocess.Popen(shell_command, shell=True)
    except:
        # Pokud selže přímé volání Explorer dialogu, použijeme PowerShell
        ps_command = f'powershell -Command "Start-Process \"$env:windir\explorer.exe\" -ArgumentList \"shell:::{{{0xed7ba470, 0x8e54, 0x465e, 0x82, 0x5c, 0x99, 0x72, 0x03, 0x88, 0x9d, 0x57}}} {drive_letter}\""'
        subprocess.Popen(ps_command, shell=True)

def make_bootable(drive_letter):
    """Nastaví SD kartu jako bootovatelnou pro CHDK"""
    if not drive_letter or not drive_letter.endswith(':'):
        raise ValueError("Neplatné označení disku")
    
    drive_path = f"{drive_letter}\\"
    
    try:
        # Vytvoření souboru BOOTDISK.BIN (pro bootování)
        boot_file_path = os.path.join(drive_path, 'BOOTDISK.BIN')
        if not os.path.exists(boot_file_path):
            with open(boot_file_path, 'wb') as f:
                # Vytvoříme prázdný soubor
                f.write(b'')
            
            # Nastavení atributu skrytý (pokud selže, pokračujeme)
            try:
                os.system(f'attrib +h "{boot_file_path}"')
            except:
                pass  # Ignorovat chyby při nastavení atributu
        
        # Vytvoření složky DCIM, pokud neexistuje (požadováno některými fotoaparáty)
        dcim_path = os.path.join(drive_path, 'DCIM')
        if not os.path.exists(dcim_path):
            os.makedirs(dcim_path, exist_ok=True)
            
        return True
    except Exception as e:
        raise RuntimeError(f"Nepodařilo se nastavit bootovatelnost: {str(e)}")

def is_admin():
    """Kontroluje, zda je aplikace spuštěna s administrátorskými právy"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
