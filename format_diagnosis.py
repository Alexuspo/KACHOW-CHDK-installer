"""
Diagnostický nástroj pro formátování SD karet
"""

import os
import sys
import subprocess
import tempfile
import ctypes
import platform

def is_admin():
    """Kontroluje, zda je aplikace spuštěna s administrátorskými právy"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def test_format_tools():
    """Testuje dostupnost formátovacích nástrojů"""
    print("Diagnostika formátování SD karty")
    print("=" * 50)
    
    # Kontrola oprávnění
    print(f"Spuštěno jako administrátor: {'ANO' if is_admin() else 'NE'}")
    print(f"Operační systém: {platform.system()} {platform.release()} {platform.version()}")
    print(f"Python verze: {platform.python_version()}")
    print(f"Aktuální adresář: {os.getcwd()}")
    
    # Test PowerShell
    try:
        result = subprocess.run(
            ["powershell.exe", "-Command", "Get-Command Format-Volume"],
            capture_output=True,
            text=True,
            timeout=10
        )
        print(f"PowerShell Format-Volume příkaz: {'DOSTUPNÝ' if result.returncode == 0 else 'NEDOSTUPNÝ'}")
    except Exception as e:
        print(f"PowerShell test selhal: {str(e)}")
    
    # Test DiskPart
    try:
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            script_path = temp_file.name
            temp_file.write("list disk\nexit\n")
        
        result = subprocess.run(
            ["diskpart", "/s", script_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        os.unlink(script_path)
        print(f"DiskPart příkaz: {'DOSTUPNÝ' if result.returncode == 0 else 'NEDOSTUPNÝ'}")
    except Exception as e:
        print(f"DiskPart test selhal: {str(e)}")
    
    # Test Format
    try:
        result = subprocess.run(
            ["cmd", "/c", "where", "format"],
            capture_output=True,
            text=True,
            timeout=5
        )
        format_available = result.returncode == 0
        format_path = result.stdout.strip() if format_available else "NENALEZENO"
        print(f"Format příkaz: {'DOSTUPNÝ' if format_available else 'NEDOSTUPNÝ'}")
        print(f"Format umístění: {format_path}")
    except Exception as e:
        print(f"Format test selhal: {str(e)}")
    
    # Test oprávnění zápisu do temp adresáře
    try:
        with tempfile.NamedTemporaryFile(mode='w', delete=True) as temp_file:
            temp_file.write("test")
            temp_file.flush()
        print("Oprávnění zápisu do temp adresáře: ANO")
    except Exception as e:
        print(f"Oprávnění zápisu do temp adresáře: NE - {str(e)}")
    
    print("\nDoporučení:")
    if not is_admin():
        print("- Spusťte aplikaci jako správce (run as administrator)")
    print("- Zkuste formátovat SD kartu přímo z Průzkumníka Windows (pravý klik na disk > Formátovat)")
    print("- Po manuálním formátování použijte funkci 'Nastavit bootovatelnost' v aplikaci")

if __name__ == "__main__":
    test_format_tools()
    input("\nStiskněte Enter pro ukončení...")
