"""
Skript pro vytvoření a naplnění adresáře s modely CHDK firmwarů
"""
import os
import shutil
import zipfile
import urllib.request
from io import BytesIO
import tempfile

def setup_models_directory():
    """Vytvoří a naplní adresář s ukázkovými CHDK firmwary"""
    print("Příprava adresáře s CHDK modely...")
    
    # Cesta k adresáři s modely
    models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chdk_models")
    os.makedirs(models_dir, exist_ok=True)
    
    print(f"Adresář vytvořen: {models_dir}")
    
    # Demonstrační model - vytvoření složkové struktury pro PowerShot A720 IS
    demo_model_dir = os.path.join(models_dir, "PowerShot A720 IS")
    os.makedirs(demo_model_dir, exist_ok=True)
    
    # Vytvoření základní struktury CHDK
    os.makedirs(os.path.join(demo_model_dir, "CHDK"), exist_ok=True)
    os.makedirs(os.path.join(demo_model_dir, "CHDK", "SCRIPTS"), exist_ok=True)
    os.makedirs(os.path.join(demo_model_dir, "CHDK", "LOGS"), exist_ok=True)
    
    # Vytvoření ukázkových souborů
    with open(os.path.join(demo_model_dir, "DISKBOOT.BIN"), "w") as f:
        f.write("# CHDK boot file for PowerShot A720 IS\n")
    
    with open(os.path.join(demo_model_dir, "CHDK", "CHDK.CFG"), "w") as f:
        f.write("# CHDK configuration file\n")
    
    with open(os.path.join(demo_model_dir, "CHDK", "SCRIPTS", "demo.bas"), "w") as f:
        f.write("rem CHDK demo script\n")
        f.write("print \"Hello from CHDK!\"\n")
        f.write("sleep 3000\n")
    
    print(f"Vytvořen ukázkový model: PowerShot A720 IS")
    
    # Vytvoření ZIP souboru pro další demonstrační model
    zip_model_path = os.path.join(models_dir, "PowerShot A480.zip")
    
    with zipfile.ZipFile(zip_model_path, 'w') as zipf:
        # Vytvoření a přidání souborů do ZIPu
        with tempfile.TemporaryDirectory() as temp_dir:
            # Vytvoření DISKBOOT.BIN
            diskboot_path = os.path.join(temp_dir, "DISKBOOT.BIN")
            with open(diskboot_path, "w") as f:
                f.write("# CHDK boot file for PowerShot A480\n")
            zipf.write(diskboot_path, "DISKBOOT.BIN")
            
            # Vytvoření struktury CHDK
            chdk_dir = os.path.join(temp_dir, "CHDK")
            os.makedirs(chdk_dir)
            
            # Vytvoření konfiguračního souboru
            cfg_path = os.path.join(chdk_dir, "CHDK.CFG")
            with open(cfg_path, "w") as f:
                f.write("# CHDK configuration file for A480\n")
            zipf.write(cfg_path, "CHDK/CHDK.CFG")
            
            # Vytvoření adresáře SCRIPTS
            scripts_dir = os.path.join(chdk_dir, "SCRIPTS")
            os.makedirs(scripts_dir)
            
            # Vytvoření ukázkového skriptu
            script_path = os.path.join(scripts_dir, "script.bas")
            with open(script_path, "w") as f:
                f.write("rem CHDK demo script for A480\n")
                f.write("print \"Hello from PowerShot A480!\"\n")
            zipf.write(script_path, "CHDK/SCRIPTS/script.bas")
    
    print(f"Vytvořen ZIP model: PowerShot A480.zip")
    
    # Pokud máme internet, zkusíme stáhnout reálný firmware
    try:
        # Adresa ke stažení ukázkového CHDK firmware
        # Poznámka: Tento URL je jen ilustrační a nemusí fungovat
        # demo_url = "https://downloads.sourceforge.net/project/chdk/CHDK/1.5.1/CHDK_1.5.1_for_A720IS.zip"
        # 
        # with urllib.request.urlopen(demo_url, timeout=10) as response:
        #    with open(os.path.join(models_dir, "PowerShot A720 IS - Official.zip"), 'wb') as out_file:
        #        shutil.copyfileobj(response, out_file)
        #    print("Stažen oficiální firmware pro PowerShot A720 IS")
        pass
    except:
        print("Stahování oficiálního firmware se nezdařilo - offline mód")
    
    print("\nPříprava adresáře s CHDK modely dokončena.")
    print(f"K dispozici jsou 2 ukázkové modely v adresáři: {models_dir}")
    print("Pro přidání dalších modelů použijte funkci \"Přidat nový firmware\" v aplikaci.")

if __name__ == "__main__":
    setup_models_directory()
    input("Stiskněte Enter pro ukončení...")
