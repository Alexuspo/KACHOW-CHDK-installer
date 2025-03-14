"""
Modul pro logování operací CHDK instalátoru
"""
import os
import logging
from datetime import datetime

# Nastavení globálního loggeru
def setup_logger():
    """
    Nastaví a vrátí logger pro CHDK instalátor
    """
    # Vytvoření adresáře pro logy, pokud neexistuje
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    # Název souboru logu podle data a času
    log_filename = os.path.join(log_dir, f"chdk_installer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    # Konfigurace loggeru
    logger = logging.getLogger("CHDKInstaller")
    logger.setLevel(logging.DEBUG)
    
    # Handler pro soubor
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # Handler pro konzoli
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formát zpráv
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Přidání handlerů k loggeru
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info(f"Logger nastaven, logy ukládány do: {log_filename}")
    return logger

# Globální instance loggeru
logger = setup_logger()

def get_logger():
    """
    Vrátí globální instanci loggeru
    """
    return logger
