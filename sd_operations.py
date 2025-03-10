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
                if drive_type == win32file.DRIVE_REMOVABLE:
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
    
    # Formátování přes příkazovou řádku
    cmd = f'format {drive_letter} /FS:FAT32 /Q /X /V:"CHDK"'
    
    try:
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                               text=True, input='Y\n')
        
        if result.returncode != 0:
            raise RuntimeError(f"Chyba při formátování: {result.stderr}")
    except Exception as e:
        raise RuntimeError(f"Chyba při formátování disku: {str(e)}")

def make_bootable(drive_letter):
    """Nastaví SD kartu jako bootovatelnou pro CHDK"""
    if not drive_letter or not drive_letter.endswith(':'):
        raise ValueError("Neplatné označení disku")
    
    drive_path = f"{drive_letter}\\"
    
    # Vytvoření DISKBOOT.BIN souboru (prázdný soubor)
    try:
        # Kontrola, zda již existuje
        boot_file_path = os.path.join(drive_path, 'BOOTDISK.BIN')
        if not os.path.exists(boot_file_path):
            with open(boot_file_path, 'w') as f:
                pass  # Vytvoření prázdného souboru
        
        # Nastavení atributu souboru
        os.system(f'attrib +h {boot_file_path}')
    except Exception as e:
        raise RuntimeError(f"Nepodařilo se nastavit bootovatelnost: {str(e)}")

def is_admin():
    """Kontroluje, zda je aplikace spuštěna s administrátorskými právy"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
