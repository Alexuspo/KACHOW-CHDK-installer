"""
Modul pro správu předinstalovaných CHDK firmwarů
"""
import os
import shutil
import zipfile
import glob
from pathlib import Path

# Definujeme cestu k adresáři s modely fotoaparátů
MODELS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chdk_models")

class CHDKModelsManager:
    def __init__(self):
        # Zajistit existenci adresáře pro modely
        if not os.path.exists(MODELS_DIR):
            os.makedirs(MODELS_DIR, exist_ok=True)
    
    def get_available_models(self):
        """Vrátí seznam dostupných modelů fotoaparátů s předinstalovaným CHDK"""
        models = []
        if os.path.exists(MODELS_DIR):
            # Procházíme všechny adresáře/zip soubory v MODELS_DIR
            for item in sorted(os.listdir(MODELS_DIR)):
                item_path = os.path.join(MODELS_DIR, item)
                # Pokud je to adresář nebo ZIP soubor, přidáme ho jako model
                if os.path.isdir(item_path) or item.lower().endswith(".zip"):
                    model_name = os.path.splitext(item)[0]  # Odstraníme příponu pro jednotnost
                    models.append(model_name)
        return models
    
    def install_model_firmware(self, model_name, drive_letter):
        """Nainstaluje CHDK firmware pro vybraný model na SD kartu"""
        if not drive_letter or not drive_letter.endswith(':'):
            raise ValueError("Neplatné označení disku")
        
        drive_path = f"{drive_letter}\\"
        
        # Kontrola, zda existuje CHDK adresář na SD kartě, pokud ne, vytvoříme ho
        chdk_dir = os.path.join(drive_path, "CHDK")
        os.makedirs(chdk_dir, exist_ok=True)
        
        # Nejprve zkontrolujeme existenci adresáře pro daný model
        model_dir = os.path.join(MODELS_DIR, model_name)
        if os.path.isdir(model_dir):
            # Kopírujeme soubory z adresáře modelu na SD kartu
            self._copy_directory_contents(model_dir, chdk_dir)
            return True
        
        # Pokud adresář neexistuje, zkusíme hledat ZIP soubor
        zip_path = os.path.join(MODELS_DIR, f"{model_name}.zip")
        if os.path.exists(zip_path):
            # Extrahujeme ZIP soubor na SD kartu
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(chdk_dir)
            return True
            
        raise FileNotFoundError(f"CHDK firmware pro model {model_name} nebyl nalezen")
    
    def _copy_directory_contents(self, src_dir, dst_dir):
        """Zkopíruje obsah adresáře src_dir do dst_dir"""
        for item in os.listdir(src_dir):
            src_path = os.path.join(src_dir, item)
            dst_path = os.path.join(dst_dir, item)
            
            if os.path.isdir(src_path):
                # Rekurzivní kopírování adresářů
                os.makedirs(dst_path, exist_ok=True)
                self._copy_directory_contents(src_path, dst_path)
            else:
                # Kopírování souborů
                shutil.copy2(src_path, dst_path)
    
    def add_firmware(self, firmware_path, model_name=None):
        """
        Přidá nový firmware do adresáře modelů
        
        Args:
            firmware_path: Cesta k firmware souboru nebo adresáři
            model_name: Volitelný název modelu, pokud není uveden, použije se název souboru
        """
        if not os.path.exists(firmware_path):
            raise FileNotFoundError(f"Soubor {firmware_path} nebyl nalezen")
        
        # Pokud není zadán název modelu, použijeme název souboru
        if model_name is None:
            model_name = os.path.splitext(os.path.basename(firmware_path))[0]
        
        # Cílová cesta v adresáři modelů
        target_path = os.path.join(MODELS_DIR, model_name)
        
        # Pokud je firmware_path adresář, zkopírujeme ho celý
        if os.path.isdir(firmware_path):
            if os.path.exists(target_path):
                shutil.rmtree(target_path)  # Smažeme existující složku
            shutil.copytree(firmware_path, target_path)
            return target_path
        
        # Pokud je to ZIP soubor, zkopírujeme ho
        elif firmware_path.lower().endswith('.zip'):
            target_file = os.path.join(MODELS_DIR, f"{model_name}.zip")
            shutil.copy2(firmware_path, target_file)
            return target_file
        
        # Jinak vytvoříme novou složku a zkopírujeme soubor do ní
        else:
            os.makedirs(target_path, exist_ok=True)
            shutil.copy2(firmware_path, target_path)
            return target_path
