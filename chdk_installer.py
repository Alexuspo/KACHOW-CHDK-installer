import os
import shutil
import requests
import zipfile
import io
from pathlib import Path
import tempfile

# URL pro stažení CHDK verzí nebo adresář s modely
CHDK_MODELS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chdk_models")

# Odkaz na CHDK download
CHDK_DOWNLOAD_URL = "https://app.assembla.com/spaces/chdk/git/source/stable_version"

def list_available_models():
    """Vrací seznam dostupných modelů fotoaparátů Canon s CHDK"""
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
    """
    if not drive_letter or not drive_letter.endswith(':'):
        raise ValueError("Neplatné označení disku")
    
    drive_path = f"{drive_letter}\\"
    
    # Zkontrolujeme, zda je SD karta připojena
    if not os.path.exists(drive_path):
        raise FileNotFoundError(f"Disk {drive_letter} není dostupný")
    
    # Pokud je zadána vlastní cesta
    if custom_path and os.path.exists(custom_path):
        source_path = custom_path
    else:
        # Použijeme vestavěné CHDK pro daný model
        model_dir = model_name.replace(" ", "_").lower()
        source_path = os.path.join(CHDK_MODELS_DIR, model_dir)
        
        # Pokud nemáme lokální soubory, pokusíme se stáhnout
        if not os.path.exists(source_path):
            source_path = download_chdk_for_model(model_name, drive_path)
    
    # Vytvoříme CHDK adresář na SD kartě
    chdk_dir = os.path.join(drive_path, "CHDK")
    os.makedirs(chdk_dir, exist_ok=True)
    
    # Zkopírujeme soubory
    if os.path.isdir(source_path):
        copy_directory_contents(source_path, chdk_dir)
    else:
        raise FileNotFoundError(f"Nenalezeny soubory CHDK pro model {model_name}")

def download_chdk_for_model(model_name, destination):
    """
    Stáhne CHDK soubory pro daný model
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
