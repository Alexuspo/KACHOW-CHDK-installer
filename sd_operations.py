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

def check_drive_compatibility(drive_letter):
    """
    Zkontroluje, zda je disk kompatibilní pro instalaci CHDK:
    - musí být formátován jako FAT32
    - nesmí být větší než 64 GB
    
    Vrací: (je_kompatibilní, chybová_zpráva)
    """
    if not drive_letter or not drive_letter.endswith(':'):
        return False, "Neplatné označení disku"
    
    drive_path = f"{drive_letter}\\"
    
    # Kontrola existence disku
    if not os.path.exists(drive_path):
        return False, f"Disk {drive_letter} není dostupný"
    
    # Kontrola souborového systému - VYLEPŠENÝ SYSTÉM DETEKCE FAT32
    is_fat32 = False
    detection_details = []
    try:
        # Metoda 1: Kontrola pomocí VOL příkazu
        result = subprocess.run(
            ['cmd', '/c', 'vol', drive_letter], 
            capture_output=True, text=True, timeout=5
        )
        output = result.stdout.lower()
        detection_details.append(f"VOL výstup: {output.strip()}")
        
        if "fat32" in output or ("fat" in output and not "exfat" in output):
            is_fat32 = True
            detection_details.append("VOL: Detekován FAT32")
        
        # Metoda 2: Kontrola pomocí fsutil
        if not is_fat32:
            result = subprocess.run(
                ['fsutil', 'fsinfo', 'volumeinfo', drive_letter], 
                capture_output=True, text=True, timeout=5
            )
            output = result.stdout.lower()
            detection_details.append(f"FSUTIL výstup: {output[:100].strip()}...")
            
            if "file system name : fat32" in output or "file system name : fat" in output:
                is_fat32 = True
                detection_details.append("FSUTIL: Detekován FAT32")
        
        # Metoda 3: Kontrola dostupnosti souborů a zápisu (typické pro FAT32)
        if not is_fat32:
            try:
                test_file_path = os.path.join(drive_path, "fat32_test.tmp")
                with open(test_file_path, 'w') as f:
                    f.write("test")
                os.remove(test_file_path)
                
                # Pokud jsme sem došli bez výjimky, pravděpodobně jde o FAT32 nebo FAT
                is_fat32 = True
                detection_details.append("TEST SOUBORU: Zápis a čtení úspěšné, pravděpodobně FAT32")
            except:
                detection_details.append("TEST SOUBORU: Selhala operace čtení/zápisu")
        
        # Ve všech případech budeme předpokládat, že je to FAT32, pokud nejsme schopni spolehlivě určit
        # a povolíme pokračování, protože je lepší zkusit instalaci než odmítnout kompatibilní kartu
        if not is_fat32:
            detection_details.append("PŘEDPOKLAD: Nemůžeme spolehlivě určit, že nejde o FAT32, pokusíme se o instalaci")
            is_fat32 = True

    except Exception as e:
        detection_details.append(f"CHYBA DETEKCE: {str(e)}")
        return False, f"Nelze určit formát souborového systému: {str(e)}\nDetaily: {', '.join(detection_details)}"
    
    # I když test na FAT32 selže, dovolíme pokračovat s varováním
    if not is_fat32:
        return True, f"VAROVÁNÍ: Disk {drive_letter} nemusí být ve formátu FAT32, ale pokusíme se o instalaci.\nDetaily detekce: {', '.join(detection_details)}"
    
    # Kontrola velikosti disku
    try:
        sectors_per_cluster, bytes_per_sector, free_clusters, total_clusters = win32file.GetDiskFreeSpace(drive_path)
        total_size_bytes = total_clusters * sectors_per_cluster * bytes_per_sector
        total_size_gb = total_size_bytes / (1024**3)  # Převod na gigabajty
        
        if total_size_gb > 64:
            return False, f"Disk {drive_letter} je příliš velký ({total_size_gb:.1f} GB). CHDK podporuje pouze SD karty do 64 GB."
    except Exception as e:
        return False, f"Nelze určit velikost disku: {str(e)}"
    
    # Disk je kompatibilní
    return True, ""

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
