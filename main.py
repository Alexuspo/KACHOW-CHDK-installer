import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from sd_operations import get_drives, format_drive_to_fat32, make_bootable
from chdk_installer import install_chdk, list_available_models, install_firmware_file

class CHDKInstallerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KACHOW CHDK Installer")
        self.root.geometry("650x580")
        self.root.resizable(True, True)
        
        # Nastavení stylu aplikace
        self.style = ttk.Style()
        self.setup_style()
        
        # Nastavení ikony aplikace
        if getattr(sys, 'frozen', False):
            icon_path = os.path.join(sys._MEIPASS, "assets", "icon.ico")
            self.asset_path = os.path.join(sys._MEIPASS, "assets")
        else:
            icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
            self.asset_path = os.path.join(os.path.dirname(__file__), "assets")
            
        try:
            self.root.iconbitmap(icon_path)
        except:
            pass  # Ikona nenalezena, ignorovat
            
        self.create_widgets()
        self.refresh_drives()
        
    def setup_style(self):
        """Nastavení vzhledu aplikace"""
        # Použití moderního tématu
        available_themes = self.style.theme_names()
        if 'clam' in available_themes:
            self.style.theme_use('clam')
        
        # Hlavní barvy aplikace
        bg_color = "#f0f0f0"
        accent_color = "#3498db"  # Modrá
        darker_accent = "#2980b9"
        success_color = "#2ecc71"  # Zelená
        warning_color = "#e74c3c"  # Červená
        
        # Nastavení základního stylu
        self.style.configure("TFrame", background=bg_color)
        self.style.configure("TLabel", background=bg_color, font=("Arial", 10))
        self.style.configure("TLabelframe", background=bg_color)
        self.style.configure("TLabelframe.Label", font=("Arial", 11, "bold"))
        
        # Tlačítka
        self.style.configure("TButton", font=("Arial", 10))
        
        # Speciální tlačítka
        self.style.configure("Install.TButton", font=("Arial", 11, "bold"))
        self.style.configure("Refresh.TButton", font=("Arial", 9))
        
        # Progressbar
        self.style.configure("TProgressbar", thickness=8)
        
        # Záhlaví
        self.style.configure("Header.TLabel", font=("Arial", 18, "bold"), foreground=accent_color)
        
        # Varování
        self.style.configure("Warning.TLabel", foreground=warning_color, font=("Arial", 10, "bold"))
    
    def create_widgets(self):
        # Hlavní rámec
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Nadpis
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=10)
        
        # Logo a nadpis vedle sebe
        try:
            logo_path = os.path.join(self.asset_path, "logo.png")
            if os.path.exists(logo_path):
                logo_img = tk.PhotoImage(file=logo_path)
                logo_img = logo_img.subsample(3, 3)  # Zmenšení obrázku
                self.logo_img = logo_img  # Uchování reference
                logo_label = ttk.Label(header_frame, image=logo_img, background="#f0f0f0")
                logo_label.pack(side=tk.LEFT, padx=(0, 10))
        except:
            pass  # Ignorovat pokud logo není k dispozici
        
        title_label = ttk.Label(header_frame, text="KACHOW CHDK Installer", style="Header.TLabel")
        title_label.pack(side=tk.LEFT)
        
        # Uvítací zpráva / krátký popis
        welcome_text = ("Vítejte v instalátoru KACHOW CHDK! Tento nástroj vám pomůže připravit SD kartu "
                      "s firmwarem CHDK pro váš fotoaparát Canon.")
        welcome_label = ttk.Label(main_frame, text=welcome_text, wraplength=600, 
                                 justify="center", padding=(0, 5))
        welcome_label.pack(fill=tk.X, pady=5)
        
        # Notebook pro organizaci obsahu
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Záložka 1: Instalace
        install_frame = ttk.Frame(notebook, padding=15)
        notebook.add(install_frame, text=" Instalace CHDK ")
        
        # Záložka 2: Nápověda
        help_frame = ttk.Frame(notebook, padding=15)
        notebook.add(help_frame, text=" Nápověda ")
        
        # Záložka 3: O aplikaci
        about_frame = ttk.Frame(notebook, padding=15)
        notebook.add(about_frame, text=" O aplikaci ")
        
        # Obsah záložky Instalace
        self.setup_install_tab(install_frame)
        
        # Obsah záložky Nápověda
        self.setup_help_tab(help_frame)
        
        # Obsah záložky O aplikaci
        self.setup_about_tab(about_frame)
        
        # Stavový řádek a progress bar
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        
        self.progress_var = tk.DoubleVar(value=0.0)
        progress_bar = ttk.Progressbar(status_frame, mode="determinate", 
                                      variable=self.progress_var, length=100)
        progress_bar.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))
        
        self.status_var = tk.StringVar(value="Připraven")
        status_bar = ttk.Label(status_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W, padding=(5, 2))
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def setup_install_tab(self, parent_frame):
        # SD Card selection frame
        sd_frame = ttk.LabelFrame(parent_frame, text="Krok 1: Výběr SD karty", padding=10)
        sd_frame.pack(fill=tk.X, pady=5)
        
        # Drives selection and refresh
        drive_frame = ttk.Frame(sd_frame)
        drive_frame.pack(fill=tk.X, pady=5)
        
        sd_label = ttk.Label(drive_frame, text="Dostupné SD karty:")
        sd_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.drive_combobox = ttk.Combobox(drive_frame, state="readonly", width=10)
        self.drive_combobox.pack(side=tk.LEFT, padx=(0, 5))
        
        refresh_button = ttk.Button(drive_frame, text="Obnovit", 
                                   command=self.refresh_drives, style="Refresh.TButton")
        refresh_button.pack(side=tk.LEFT)
        
        # Format checkbox
        format_frame = ttk.Frame(sd_frame)
        format_frame.pack(fill=tk.X, pady=5)
        
        self.format_var = tk.BooleanVar(value=True)
        format_check = ttk.Checkbutton(format_frame, text="Formátovat SD kartu (FAT32)", variable=self.format_var)
        format_check.pack(side=tk.LEFT)
        
        # Warning label
        warning_text = "VAROVÁNÍ: Formátování smaže všechna data z vybrané SD karty!"
        warning_label = ttk.Label(sd_frame, text=warning_text, style="Warning.TLabel", wraplength=550)
        warning_label.pack(fill=tk.X, pady=5)
        
        # CHDK Selection frame
        chdk_frame = ttk.LabelFrame(parent_frame, text="Krok 2: Výběr firmware CHDK", padding=10)
        chdk_frame.pack(fill=tk.X, pady=10)
        
        # Informace o stažení firmwaru
        download_text = ("Navštivte stránku https://www.mighty-hoernsche.de/ a stáhněte "
                         "firmware CHDK pro váš model fotoaparátu Canon.")
        download_label = ttk.Label(chdk_frame, text=download_text, wraplength=550, justify=tk.LEFT)
        download_label.pack(fill=tk.X, pady=5)
        
        # Odkaz na web
        website_frame = ttk.Frame(chdk_frame)
        website_frame.pack(fill=tk.X, pady=5)
        
        visit_label = ttk.Label(website_frame, text="Otevřít stránku s firmwarem:")
        visit_label.pack(side=tk.LEFT, padx=(0, 5))
        
        website_button = ttk.Button(website_frame, text="Otevřít mighty-hoernsche.de",
                                  command=lambda: self.open_website("https://www.mighty-hoernsche.de/"))
        website_button.pack(side=tk.LEFT)
        
        # Výběr staženého souboru
        file_frame = ttk.Frame(chdk_frame)
        file_frame.pack(fill=tk.X, pady=10)
        
        file_label = ttk.Label(file_frame, text="Stažený soubor:")
        file_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.firmware_file_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.firmware_file_var, width=40)
        file_entry.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)
        
        browse_file_button = ttk.Button(file_frame, text="Procházet",
                                      command=self.browse_firmware_file)
        browse_file_button.pack(side=tk.LEFT)
        
        # Instalační tlačítko
        install_frame = ttk.Frame(parent_frame)
        install_frame.pack(pady=15, anchor=tk.CENTER)
        
        install_button = ttk.Button(install_frame, text="📥 Instalovat CHDK", 
                                  command=self.run_installation, style="Install.TButton", 
                                  padding=(20, 10))
        install_button.pack()
    
    def setup_help_tab(self, parent_frame):
        """Nastavení obsahu záložky Nápověda"""
        help_text = (
            "Jak používat CHDK Installer:\n\n"
            "1. Připojte SD kartu k počítači.\n"
            "2. Navštivte stránku https://www.mighty-hoernsche.de/\n"
            "3. Najděte a stáhněte CHDK firmware pro váš model fotoaparátu Canon.\n"
            "4. V záložce 'Instalace CHDK' vyberte správnou SD kartu.\n"
            "5. Pokud chcete SD kartu formátovat (doporučeno), ponechte zaškrtnutou možnost formátování.\n"
            "6. Klikněte na tlačítko 'Procházet' a vyberte stažený soubor s firmwarem.\n"
            "7. Klikněte na 'Instalovat CHDK'.\n\n"
            "Po instalaci:\n"
            "1. Vložte SD kartu do fotoaparátu.\n"
            "2. Zapněte fotoaparát v režimu přehrávání.\n"
            "3. Aktivujte CHDK podle návodu k vašemu modelu (obvykle stisknutím tlačítka 'menu' nebo 'disp').\n\n"
            "Další informace najdete na oficiálních stránkách CHDK: http://chdk.wikia.com/"
        )
        
        # Použití scrollovatelného textového pole pro nápovědu
        help_scroll = ttk.Scrollbar(parent_frame)
        help_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        help_text_box = tk.Text(parent_frame, wrap=tk.WORD, height=15, 
                              yscrollcommand=help_scroll.set, bg="#ffffff", padx=10, pady=10)
        help_text_box.insert(tk.END, help_text)
        help_text_box.config(state=tk.DISABLED)  # Jen pro čtení
        help_text_box.pack(fill=tk.BOTH, expand=True)
        
        help_scroll.config(command=help_text_box.yview)
    
    def setup_about_tab(self, parent_frame):
        """Nastavení obsahu záložky O aplikaci"""
        about_frame = ttk.Frame(parent_frame)
        about_frame.pack(fill=tk.BOTH, expand=True)
        
        # Logo aplikace (větší)
        try:
            about_logo_path = os.path.join(self.asset_path, "logo.png")
            if os.path.exists(about_logo_path):
                about_logo = tk.PhotoImage(file=about_logo_path)
                about_logo = about_logo.subsample(2, 2)  # Zmenšení obrázku
                self.about_logo = about_logo  # Uchování reference
                about_logo_label = ttk.Label(about_frame, image=about_logo, background="#f0f0f0")
                about_logo_label.pack(pady=10)
        except:
            pass  # Ignorovat pokud logo není k dispozici
        
        # Informace o aplikaci
        about_text = (
            "KACHOW CHDK Installer v1.0\n\n"
            "Aplikace pro snadnou instalaci CHDK firmwaru na SD karty.\n\n"
            "CHDK (Canon Hack Development Kit) je neoficiální firmware\n"
            "pro fotoaparáty Canon, který rozšiřuje jejich možnosti.\n\n"
            "© 2025 Alexuspo"
        )
        
        about_label = ttk.Label(about_frame, text=about_text, justify=tk.CENTER, wraplength=400)
        about_label.pack(pady=10)
        
        # Odkaz na webové stránky CHDK
        chdk_website_label = ttk.Label(about_frame, text=self.strings["visit_chdk"], 
                                 foreground="blue", cursor="hand2")
        chdk_website_label.pack(pady=5)
        chdk_website_label.bind("<Button-1>", lambda e: self.open_website("http://chdk.wikia.com/"))
        
        # Odkaz na GitHub repozitář
        github_label = ttk.Label(about_frame, text=self.strings["github_link"], 
                              foreground="blue", cursor="hand2")
        github_label.pack(pady=5)
        github_label.bind("<Button-1>", lambda e: self.open_website("https://github.com/Alexuspo/KACHOW-CHDK-installer"))
    
    def refresh_drives(self):
        self.status_var.set("Načítání disků...")
        self.progress_var.set(10)
        self.root.update_idletasks()
        
        try:
            # Získání seznamu disků
            drives = get_drives()
            
            # Aktualizace comboboxu
            self.drive_combobox['values'] = drives
            
            # Pokud jsou disky k dispozici, vybereme první
            if drives:
                self.drive_combobox.current(0)
                self.status_var.set(f"Nalezeno {len(drives)} vyměnitelných disků")
            else:
                self.status_var.set("Nenalezeny žádné SD karty")
            
            self.progress_var.set(100)
            self.root.after(1000, lambda: self.progress_var.set(0))
            
        except Exception as e:
            # Zachycení a zobrazení chyby
            self.status_var.set("Chyba: " + str(e))
            self.progress_var.set(0)
            messagebox.showerror("Chyba", f"Nepodařilo se načíst dostupné disky: {str(e)}")
    
    def browse_firmware_file(self):
        """Výběr staženého souboru s firmwarem CHDK"""
        filetypes = [
            ("CHDK firmware", "*.zip"),
            ("Všechny soubory", "*.*")
        ]
        firmware_file = filedialog.askopenfilename(
            title="Vyberte stažený CHDK firmware",
            filetypes=filetypes
        )
        if firmware_file:
            self.firmware_file_var.set(firmware_file)
    
    def toggle_custom_folder(self):
        if self.custom_folder_var.get():
            self.custom_folder_entry.config(state="normal")
            self.browse_button.config(state="normal")
        else:
            self.custom_folder_entry.config(state="disabled")
            self.browse_button.config(state="disabled")
    
    def browse_folder(self):
        folder_path = filedialog.askdirectory(title="Vyberte složku s CHDK")
        if folder_path:
            self.custom_folder_entry.delete(0, tk.END)
            self.custom_folder_entry.insert(0, folder_path)
    
    def run_installation(self):
        # Validate selections
        selected_drive = self.drive_combobox.get()
        if not selected_drive:
            messagebox.showerror("Chyba", "Vyberte prosím SD kartu")
            return
        
        # Kontrola souboru s firmwarem
        firmware_file = self.firmware_file_var.get()
        if not firmware_file or not os.path.exists(firmware_file):
            messagebox.showerror("Chyba", "Vyberte platný soubor s CHDK firmwarem")
            return
        
        # Confirm formatting
        if self.format_var.get():
            result = messagebox.askyesno(
                "Potvrdit formátování", 
                f"Opravdu chcete formátovat disk {selected_drive}?\n\n"
                "VŠECHNA DATA NA DISKU BUDOU SMAZÁNA!"
            )
            if not result:
                return
        
        # Run the installation process
        self.status_var.set("Zahajuji instalaci...")
        self.progress_var.set(5)
        self.root.update_idletasks()
        
        try:
            # Format if required
            if self.format_var.get():
                self.status_var.set("Formátování SD karty...")
                self.progress_var.set(20)
                self.root.update_idletasks()
                format_drive_to_fat32(selected_drive)
                self.progress_var.set(50)
                self.root.update_idletasks()
            
            # Make the card bootable
            self.status_var.set("Nastavování bootovatelnosti...")
            self.progress_var.set(70)
            self.root.update_idletasks()
            make_bootable(selected_drive)
            
            # Install CHDK
            self.status_var.set("Instalace CHDK...")
            self.progress_var.set(80)
            self.root.update_idletasks()
            install_firmware_file(selected_drive, firmware_file)
            
            self.progress_var.set(100)
            self.status_var.set("Instalace dokončena")
            messagebox.showinfo("Úspěch", "CHDK bylo úspěšně nainstalováno!")
            self.root.after(2000, lambda: self.progress_var.set(0))
            
        except Exception as e:
            self.progress_var.set(0)
            self.status_var.set(f"Chyba: {str(e)}")
            messagebox.showerror("Chyba při instalaci", str(e))
    
    def open_website(self, url):
        """Otevře webovou stránku v prohlížeči"""
        import webbrowser
        webbrowser.open(url)

if __name__ == "__main__":
    try:
        # Kontrola existence potřebných složek
        assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
        if not os.path.exists(assets_dir):
            os.makedirs(assets_dir)
            print(f"Vytvořena chybějící složka: {assets_dir}")
        
        # Spuštění aplikace
        root = tk.Tk()
        app = CHDKInstallerApp(root)
        root.mainloop()
    except Exception as e:
        import traceback
        error_msg = f"Chyba při spuštění aplikace:\n{str(e)}\n\n{traceback.format_exc()}"
        print(error_msg)
        try:
            import tkinter.messagebox
            tkinter.messagebox.showerror("Chyba", error_msg)
        except:
            print("Nelze zobrazit chybový dialog.")
            input("Stiskněte Enter pro ukončení...")
