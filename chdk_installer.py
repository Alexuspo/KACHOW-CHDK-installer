import os
import shutil
import requests
import zipfile
import io
from pathlib import Path
import tempfile

# URL pro stažení CHDK verzí nebo adresář s modely
CHDK_MODELS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chdk_models")

# Odkaz na CHDK downloads
CHDK_DOWNLOAD_URL = "https://www.mighty-hoernsche.de/"

def list_available_models():
    """Vrací seznam dostupných modelů fotoaparátů Canon s CHDK"""
    # Tato funkce je zde zachována pro zpětnou kompatibilitu
    # V nové verzi aplikace už není potřeba
    # Pokud máme lokální adresář s modely
    if os.path.exists(CHDK_MODELS_DIR) and os.path.isdir(CHDK_MODELS_DIR):
        models = []
        for item in os.listdir(CHDK_MODELS_DIR):
            if os.path.isdir(os.path.join(CHDK_MODELS_DIR, item)):
                models.append(item)
        
        if models:
            return models
    
    # Pokud nemáme lokální adresář, vracíme základní seznam modelů
    return [
        "PowerShot A480", 
        "PowerShot A490",
        "PowerShot A495",
        "PowerShot A590 IS",
        "PowerShot A610",
        "PowerShot A620",
        "PowerShot A630",
        "PowerShot A640",
        "PowerShot A650 IS",
        "PowerShot A700",
        "PowerShot A710 IS",
        "PowerShot A720 IS",
        "PowerShot G7",
        "PowerShot G9",
        "PowerShot S5 IS",
        "PowerShot SX10 IS",
        "PowerShot SX100 IS",
        "PowerShot SX110 IS",
        "PowerShot SX120 IS",
        "PowerShot SX20 IS",
        "PowerShot SX200 IS",
        "PowerShot SX220 HS",
        "PowerShot SX230 HS"
    ]

def install_chdk(drive_letter, model_name, custom_path=None):
    """
    Instaluje CHDK na vybranou SD kartu pro daný model fotoaparátu
    (Ponecháno pro zpětnou kompatibilitu)
    """
    if custom_path and os.path.exists(custom_path):
        return install_firmware_file(drive_letter, custom_path)
    
    raise ValueError("Tato metoda je zastaralá. Použijte install_firmware_file.")

def install_firmware_file(drive_letter, firmware_path):
    """
    Instaluje CHDK firmware ze staženého souboru na SD kartu
    
    Args:
        drive_letter (str): Písmeno disku (např. "E:")
        firmware_path (str): Cesta k souboru s CHDK firmwarem
    """
    if not drive_letter or not drive_letter.endswith(':'):
        raise ValueError("Neplatné označení disku")
    
    drive_path = f"{drive_letter}\\"
    
    # Zkontrolujeme, zda je SD karta připojena
    if not os.path.exists(drive_path):
        raise FileNotFoundError(f"Disk {drive_letter} není dostupný")
    
    # Zkontrolujeme, zda existuje soubor s firmwarem
    if not os.path.exists(firmware_path):
        raise FileNotFoundError(f"Soubor s firmwarem nebyl nalezen: {firmware_path}")
    
    # Vytvoříme CHDK adresář na SD kartě
    chdk_dir = os.path.join(drive_path, "CHDK")
    os.makedirs(chdk_dir, exist_ok=True)
    
    # Pokud je to ZIP soubor, extrahujeme ho
    if firmware_path.lower().endswith('.zip'):
        extract_firmware_zip(firmware_path, chdk_dir)
    # Jinak zkopírujeme celou složku (pokud je to adresář)
    elif os.path.isdir(firmware_path):
        copy_directory_contents(firmware_path, chdk_dir)
    # Nebo zkopírujeme samostatný soubor
    else:
        shutil.copy2(firmware_path, os.path.join(chdk_dir, os.path.basename(firmware_path)))

def extract_firmware_zip(zip_path, destination):
    """
    Extrahuje obsah ZIP souboru s firmwarem CHDK do cílové složky
    Zpracovává různé formáty ZIP archivů, které mohou být k dispozici
    """
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            file_list = z.namelist()
            
            # Zjistíme strukturu ZIP archivu
            has_diskboot = any(f.upper() == "DISKBOOT.BIN" for f in file_list)
            has_chdk_dir = any(f.upper().startswith("CHDK/") for f in file_list)
            has_root_dir = any("/" in f and not f.startswith(("CHDK/", "DISKBOOT")) for f in file_list)
            
            # Případy různých struktur ZIP archivů
            if has_diskboot and has_chdk_dir:
                # Ideální případ - ZIP obsahuje DISKBOOT.BIN a složku CHDK/
                print(f"Standardní CHDK formát detekován v {os.path.basename(zip_path)}")
                z.extractall(destination)
            elif has_root_dir:
                # ZIP obsahuje kořenový adresář - možná je to archiv celé SD karty
                # Musíme najít DISKBOOT.BIN a CHDK adresář
                print(f"Detekována složitější struktura v {os.path.basename(zip_path)}")
                
                # Najdeme kořenové adresáře obsahující CHDK soubory
                root_dirs = set()
                for fname in file_list:
                    parts = fname.split('/')
                    if len(parts) > 1:
                        root_dirs.add(parts[0])
                
                for root_dir in root_dirs:
                    # Zkontrolujeme, zda tento adresář obsahuje CHDK soubory
                    diskboot_path = f"{root_dir}/DISKBOOT.BIN"
                    chdk_dir_exists = any(f.startswith(f"{root_dir}/CHDK/") for f in file_list)
                    
                    if diskboot_path in file_list or chdk_dir_exists:
                        print(f"Nalezena CHDK data v adresáři: {root_dir}")
                        # Extrahujeme soubory z tohoto adresáře, ale odstraníme kořenový prefix
                        for item in file_list:
                            if item.startswith(f"{root_dir}/"):
                                # Přeskakujeme adresářové záznamy
                                if item.endswith('/'):
                                    continue
                                    
                                # Extrahujeme soubor bez kořenového prefixu
                                target_path = os.path.join(destination, item[len(root_dir)+1:])
                                
                                # Vytvoříme adresářovou strukturu, pokud neexistuje
                                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                                
                                # Extrahujeme soubor
                                with z.open(item) as source, open(target_path, 'wb') as target:
                                    shutil.copyfileobj(source, target)
            else:
                # Jiný formát, extrahujem vše a doufáme v nejlepší
                print(f"Neznámá struktura ZIP souboru {os.path.basename(zip_path)}, extrahujeme vše")
                z.extractall(destination)
                
            # Kontrola, zda byl firmware správně extrahován
            if not os.path.exists(os.path.join(destination, "DISKBOOT.BIN")) and not os.path.exists(os.path.join(destination, "CHDK")):
                print(f"Varování: V extrahovaných souborech nebyl nalezen DISKBOOT.BIN ani složka CHDK")
                
                # Hledání souborů v jakékoliv podadresářové struktuře
                found_files = []
                for root, dirs, files in os.walk(destination):
                    if "DISKBOOT.BIN" in files:
                        found_files.append(os.path.join(root, "DISKBOOT.BIN"))
                    if "CHDK" in dirs:
                        found_files.append(os.path.join(root, "CHDK"))
                
                if found_files:
                    print(f"Nalezeny CHDK soubory v podadresářích: {found_files}")
                    
                    # Přesuneme soubory do kořenového adresáře
                    for found_file in found_files:
                        basename = os.path.basename(found_file)
                        if os.path.exists(os.path.join(destination, basename)):
                            shutil.rmtree(os.path.join(destination, basename))
                        shutil.copytree(found_file, os.path.join(destination, basename))
                    
                    # Vyčistíme případné prázdné adresáře
                    for root, dirs, files in os.walk(destination, topdown=False):
                        if root != destination and not os.listdir(root):
                            os.rmdir(root)
            
    except zipfile.BadZipFile:
        raise ValueError(f"Soubor {zip_path} není platný ZIP archiv")
    except Exception as e:
        raise RuntimeError(f"Chyba při extrakci souboru: {str(e)}")

def copy_directory_contents(src_dir, dst_dir):
    """Zkopíruje obsah adresáře src_dir do dst_dir"""
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    
    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dst_path = os.path.join(dst_dir, item)
        
        if os.path.isdir(src_path):
            # Rekurzivní kopírování adresářů
            copy_directory_contents(src_path, dst_path)
        else:
            # Kopírování souborů
            shutil.copy2(src_path, dst_path)

def download_chdk_for_model(model_name, destination):
    """
    Stáhne CHDK soubory pro daný model
    (Ponecháno pro zpětnou kompatibilitu)
    """
    # Vytvoříme dočasný adresář
    temp_dir = tempfile.mkdtemp()
    
    # Vytvoříme základní CHDK soubory pro ukázku
    with open(os.path.join(temp_dir, "DISKBOOT.BIN"), "w") as f:
        f.write(f"CHDK boot file for {model_name}")
    
    # Vytvoříme adresář pro skripty
    scripts_dir = os.path.join(temp_dir, "SCRIPTS")
    os.makedirs(scripts_dir, exist_ok=True)
    
    # Vytvoříme ukázkový skript
    with open(os.path.join(scripts_dir, "example.lua"), "w") as f:
        f.write('-- Example CHDK script\nprint("Hello from CHDK!")')
    
    return temp_dir
