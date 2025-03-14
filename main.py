import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from sd_operations import get_drives, make_bootable, is_admin, check_drive_compatibility
from chdk_installer import install_chdk, list_available_models, install_firmware_file
from language_selector import select_language
from languages import CZECH, ENGLISH
import ctypes
import subprocess
from chdk_logger import get_logger

# Získáme instanci loggeru
logger = get_logger()

def run_as_admin(command=None, params=None):
    """
    Restartuje aplikaci s administrátorskými právy
    """
    if command is None:
        command = sys.executable
    if params is None:
        params = sys.argv

    shell32 = ctypes.windll.shell32
    if not isinstance(command, str):
        command = str(command)

    # Pokud je cesta k exe v uvozovkách, odstraníme je
    if command.startswith('"') and command.endswith('"'):
        command = command[1:-1]

    # ShellExecute otevře program s požadavkem na práva správce 
    ret = shell32.ShellExecuteW(None, "runas", command, " ".join(params), None, 1)
    return ret > 32  # Pokud je návratová hodnota > 32, pak bylo spuštění úspěšné

class CHDKInstallerApp:
    def __init__(self, root, language='cs'):
        self.root = root
        
        # Nastavení jazyka
        self.language = language
        self.strings = CZECH if language == 'cs' else ENGLISH
        
        self.root.title(self.strings["app_title"])
        
        # Změna výchozí velikosti okna na větší rozměr
        self.root.geometry("900x700")  # Zvětšil jsem z 650x580 na 900x700
        self.root.resizable(True, True)
        
        # Nastavení minimální velikosti okna
        self.root.minsize(650, 580)
        
        # Přidání reakce na změnu velikosti okna
        self.root.bind("<Configure>", self.on_window_resize)
        
        # Kontrola administrátorských práv při startu aplikace
        self.has_admin = is_admin()
        
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
        
        # Zobrazit varování, pokud nejsou administrátorská práva
        if not self.has_admin:
            self.show_admin_warning()
            
        self.create_widgets()
        self.refresh_drives()
    
    def show_admin_warning(self):
        """Zobrazí varování o chybějících administrátorských právech"""
        warning_frame = ttk.Frame(self.root, padding=10)
        warning_frame.pack(fill=tk.X, pady=5)
        
        warning_text = self.strings.get("admin_warning", 
                      "Aplikace není spuštěna jako správce. Formátování SD karet nemusí fungovat.")
        
        warning_label = ttk.Label(warning_frame, text=warning_text,
                               foreground="red", font=("Arial", 10, "bold"),
                               wraplength=600)
        warning_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        restart_button = ttk.Button(warning_frame, text=self.strings.get("restart_as_admin", "Spustit jako správce"),
                                 command=self.restart_as_admin)
        restart_button.pack(side=tk.RIGHT, padx=5)

    def restart_as_admin(self):
        """Restartuje aplikaci s administrátorskými právy"""
        if run_as_admin():
            self.root.destroy()  # Ukončí aktuální instanci aplikace
        else:
            messagebox.showerror(
                self.strings["error"], 
                self.strings.get("admin_restart_failed", "Nepodařilo se spustit aplikaci jako správce.")
            )
     
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
        # Hlavní rámec bez scrollování - jednodušší řešení
        main_frame = ttk.Frame(self.root, padding=20)
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
        
        title_label = ttk.Label(header_frame, text=self.strings["app_title"], style="Header.TLabel")
        title_label.pack(side=tk.LEFT)
        
        # Uvítací zpráva / krátký popis
        welcome_label = ttk.Label(main_frame, text=self.strings["welcome_text"], wraplength=600, 
                                 justify="center", padding=(0, 5))
        welcome_label.pack(fill=tk.X, pady=5)
        
        # Notebook pro organizaci obsahu - upravena výška
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=15)  # Zvětšeno pady z 10 na 15
        
        # Záložka 1: Instalace
        install_frame = ttk.Frame(notebook, padding=15)
        notebook.add(install_frame, text=self.strings["tab_install"])
        
        # Záložka 2: Nápověda
        help_frame = ttk.Frame(notebook, padding=15)
        notebook.add(help_frame, text=self.strings["tab_help"])
        
        # Záložka 3: O aplikaci
        about_frame = ttk.Frame(notebook, padding=15)
        notebook.add(about_frame, text=self.strings["tab_about"])
        
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
        
        self.status_var = tk.StringVar(value=self.strings["ready"])
        status_bar = ttk.Label(status_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W, padding=(5, 2))
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def setup_install_tab(self, parent_frame):
        # Vytvoření scrollovatelného rámce pro záložku instalace
        canvas = tk.Canvas(parent_frame)
        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=canvas.yview)
        
        # Konfigurace scrollování
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack komponenty
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Vytvoření vnitřního rámce pro obsah
        inner_frame = ttk.Frame(canvas)
        
        # Konfigurace canvas window
        canvas_window = canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        
        # Funkce pro aktualizaci scrollování
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            
        # Funkce pro přizpůsobení šířky vnitřního rámce při změně velikosti
        def configure_window_size(event):
            canvas.itemconfig(canvas_window, width=event.width)
            
        # Přidání bindování událostí
        inner_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_window_size)
        
        # Přidání scrollování pomocí myši
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # SD Card selection frame
        sd_frame = ttk.LabelFrame(inner_frame, text=self.strings["step1_title"], padding=10)
        sd_frame.pack(fill=tk.X, pady=5)
        
        # Drives selection and refresh
        drive_frame = ttk.Frame(sd_frame)
        drive_frame.pack(fill=tk.X, pady=5)
        
        sd_label = ttk.Label(drive_frame, text=self.strings["available_cards"])
        sd_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.drive_combobox = ttk.Combobox(drive_frame, state="readonly", width=10)
        self.drive_combobox.pack(side=tk.LEFT, padx=(0, 5))
        
        refresh_button = ttk.Button(drive_frame, text=self.strings["refresh"], 
                                  command=self.refresh_drives, style="Refresh.TButton")
        refresh_button.pack(side=tk.LEFT)
        
        # Informace o SD kartě - nový element
        card_info_frame = ttk.Frame(sd_frame)
        card_info_frame.pack(fill=tk.X, pady=5)
        
        # Přidání tlačítka pro kontrolu kompatibility
        check_button = ttk.Button(card_info_frame, text="Zkontrolovat kompatibilitu",
                               command=self.check_card_compatibility)
        check_button.pack(side=tk.LEFT, padx=5)
        
        # Přidání tlačítka pro nastavení bootovatelnosti
        bootable_button = ttk.Button(card_info_frame, text="Nastavit bootovatelnost",
                                  command=self.make_card_bootable)
        bootable_button.pack(side=tk.LEFT, padx=5)
        
        # Varování
        warning_label = ttk.Label(sd_frame, 
                              text="SD karta musí být ve formátu FAT32 a menší než 64 GB. Formátujte kartu ručně před použitím aplikace.",
                              style="Warning.TLabel", wraplength=550)
        warning_label.pack(fill=tk.X, pady=5)
        
        # CHDK Selection frame
        chdk_frame = ttk.LabelFrame(inner_frame, text=self.strings["step2_title"], padding=10)
        chdk_frame.pack(fill=tk.X, pady=10)
        
        # Přidáme přepínač pro výběr mezi předinstalovanými a vlastními firmware
        firmware_selection_frame = ttk.Frame(chdk_frame)
        firmware_selection_frame.pack(fill=tk.X, pady=5)
        
        self.firmware_source_var = tk.StringVar(value="custom")
        
        # Radiobutton pro vlastní firmware
        custom_radio = ttk.Radiobutton(
            firmware_selection_frame, 
            text="Vlastní firmware (stažený z internetu)", 
            variable=self.firmware_source_var, 
            value="custom",
            command=self.toggle_firmware_source
        )
        custom_radio.pack(anchor=tk.W)
        
        # Radiobutton pro předinstalované firmware
        preinstalled_radio = ttk.Radiobutton(
            firmware_selection_frame, 
            text="Předinstalované CHDK firmware", 
            variable=self.firmware_source_var, 
            value="preinstalled",
            command=self.toggle_firmware_source
        )
        preinstalled_radio.pack(anchor=tk.W)
        
        # Frame pro výběr vlastního firmware
        self.custom_firmware_frame = ttk.Frame(chdk_frame)
        self.custom_firmware_frame.pack(fill=tk.X, pady=5)
        
        # Informace o stažení firmwaru (pro vlastní firmware)
        download_label = ttk.Label(self.custom_firmware_frame, text=self.strings["download_info"],
                                wraplength=550, justify=tk.LEFT)
        download_label.pack(fill=tk.X, pady=5)
        
        # Odkaz na web
        website_frame = ttk.Frame(self.custom_firmware_frame)
        website_frame.pack(fill=tk.X, pady=5)
        
        visit_label = ttk.Label(website_frame, text=self.strings["open_firmware_page"])
        visit_label.pack(side=tk.LEFT, padx=(0, 5))
        
        website_button = ttk.Button(website_frame, text=self.strings["open_website"],
                                 command=lambda: self.open_website("https://www.mighty-hoernsche.de/"))
        website_button.pack(side=tk.LEFT)
        
        # Výběr staženého souboru
        file_frame = ttk.Frame(self.custom_firmware_frame)
        file_frame.pack(fill=tk.X, pady=10)
        
        file_label = ttk.Label(file_frame, text=self.strings["downloaded_file"])
        file_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.firmware_file_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.firmware_file_var, width=40)
        file_entry.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)
        
        browse_file_button = ttk.Button(file_frame, text=self.strings["browse"],
                                     command=self.browse_firmware_file)
        browse_file_button.pack(side=tk.LEFT)
        
        # Frame pro výběr předinstalovaného firmware
        self.preinstalled_firmware_frame = ttk.Frame(chdk_frame)
        
        # Načtení seznamu dostupných modelů
        from chdk_models_manager import CHDKModelsManager
        self.models_manager = CHDKModelsManager()
        available_models = self.models_manager.get_available_models()
        
        # Informace o předinstalovaných firmwarech
        model_info_label = ttk.Label(
            self.preinstalled_firmware_frame, 
            text="Vyberte model fotoaparátu ze seznamu:",
            wraplength=550
        )
        model_info_label.pack(fill=tk.X, pady=5)
        
        # Seznam modelů + scrollbar - zvětšená výška listboxu
        models_frame = ttk.Frame(self.preinstalled_firmware_frame)
        models_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        models_scrollbar = ttk.Scrollbar(models_frame)
        models_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.models_listbox = tk.Listbox(
            models_frame, 
            height=12,  # Zvětšeno z 8 na 12
            selectmode=tk.SINGLE,
            yscrollcommand=models_scrollbar.set
        )
        self.models_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        models_scrollbar.config(command=self.models_listbox.yview)
        
        # Naplnění seznamu modelů
        for model in available_models:
            self.models_listbox.insert(tk.END, model)
            
        # Pokud nejsou k dispozici žádné předinstalované modely, přidáme informaci
        if not available_models:
            self.models_listbox.insert(tk.END, "Žádné předinstalované firmware nejsou k dispozici")
            self.models_listbox.config(state=tk.DISABLED)
        
        # Tlačítko pro přidání nového firmwaru
        add_firmware_button = ttk.Button(
            self.preinstalled_firmware_frame, 
            text="Přidat nový firmware do databáze",
            command=self.add_new_firmware
        )
        add_firmware_button.pack(pady=5)
        
        # Výchozí zobrazení - vlastní firmware
        self.toggle_firmware_source()
        
        # Instalační tlačítko
        install_frame = ttk.Frame(inner_frame)
        install_frame.pack(pady=15, anchor=tk.CENTER)
        
        install_button = ttk.Button(install_frame, text=self.strings["install_button"], 
                                 command=self.run_installation, style="Install.TButton", 
                                 padding=(20, 10))
        install_button.pack()
        
        # Pro správné scrollování
        inner_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
    
    def toggle_firmware_source(self):
        """Přepíná mezi vlastním a předinstalovaným firmwarem"""
        if self.firmware_source_var.get() == "custom":
            # Zobrazíme custom frame, skryjeme preinstalled
            self.custom_firmware_frame.pack(fill=tk.X, pady=5)
            self.preinstalled_firmware_frame.pack_forget()
        else:
            # Zobrazíme preinstalled frame, skryjeme custom
            self.custom_firmware_frame.pack_forget()
            self.preinstalled_firmware_frame.pack(fill=tk.X, pady=5)

    def add_new_firmware(self):
        """Přidá nový firmware do databáze"""
        # Vybereme soubor nebo složku
        firmware_path = filedialog.askopenfilename(
            title="Vyberte firmware pro přidání do databáze",
            filetypes=[
                ("CHDK firmware (zip)", "*.zip"),
                ("Všechny soubory", "*.*")
            ]
        )
        
        if not firmware_path:
            return
        
        # Vyžádáme si název modelu
        model_name = None
        while not model_name:
            model_name = simpledialog.askstring(
                "Název modelu", 
                "Zadejte název modelu fotoaparátu (např. 'PowerShot A720 IS'):",
                parent=self.root
            )
            if model_name is None:  # uživatel klikl na Cancel
                return
            
            if not model_name.strip():
                messagebox.showerror("Chyba", "Název modelu nemůže být prázdný")
                model_name = None
        
        try:
            # Přidání firmware do databáze
            self.models_manager.add_firmware(firmware_path, model_name)
            
            # Aktualizace seznamu modelů
            self.models_listbox.delete(0, tk.END)
            for model in self.models_manager.get_available_models():
                self.models_listbox.insert(tk.END, model)
            
            messagebox.showinfo(
                "Firmware přidán", 
                f"Firmware pro model {model_name} byl úspěšně přidán do databáze."
            )
        except Exception as e:
            messagebox.showerror("Chyba", f"Nepodařilo se přidat firmware: {str(e)}")

    def setup_help_tab(self, parent_frame):
        """Nastavení obsahu záložky Nápověda"""
        # Použití scrollovatelného textového pole pro nápovědu
        help_scroll = ttk.Scrollbar(parent_frame)
        help_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        help_text_box = tk.Text(parent_frame, wrap=tk.WORD, height=25,  # Zvětšeno z 15 na 25
                             yscrollcommand=help_scroll.set, bg="#ffffff", padx=15, pady=15)  # Zvětšené padx a pady z 10 na 15
        help_text_box.insert(tk.END, self.strings["help_text"])
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
        about_label = ttk.Label(about_frame, text=self.strings["about_text"], 
                            justify=tk.CENTER, wraplength=400)
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
        self.status_var.set(self.strings["loading_drives"])
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
                self.status_var.set(self.strings["drives_found"].format(len(drives)))
            else:
                self.status_var.set(self.strings["no_drives"])
            
            self.progress_var.set(100)
            self.root.after(1000, lambda: self.progress_var.set(0))
            
        except Exception as e:
            # Zachycení a zobrazení chyby
            self.status_var.set(f"{self.strings['error']}: {str(e)}")
            self.progress_var.set(0)
            messagebox.showerror(self.strings["error"], 
                              self.strings["load_drives_error"].format(str(e)))
    
    def browse_firmware_file(self):
        """Výběr staženého souboru s firmwarem CHDK"""
        filetypes = [
            ("CHDK firmware", "*.zip"),
            ("Všechny soubory", "*.*")
        ]
        firmware_file = filedialog.askopenfilename(
            title="Vyberte stažený CHDK firmware",  # Použití pevného textu místo klíče
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
        folder_path = filedialog.askdirectory(title="Vyberte složku s CHDK")  # Použití pevného textu místo klíče
        if folder_path:
            self.custom_folder_entry.delete(0, tk.END)
            self.custom_folder_entry.insert(0, folder_path)
    
    def run_installation(self):
        # Validate selections
        selected_drive = self.drive_combobox.get()
        if not selected_drive:
            messagebox.showerror(self.strings["error"], self.strings["select_card"])
            return
        
        # Kontrola typu firmware zdroje
        if self.firmware_source_var.get() == "custom":
            # Kontrola souboru s firmwarem
            firmware_file = self.firmware_file_var.get()
            if not firmware_file or not os.path.exists(firmware_file):
                messagebox.showerror(self.strings["error"], self.strings["select_firmware"])
                return
        else:
            # Kontrola vybraného předinstalovaného modelu
            if not self.models_listbox.curselection():
                messagebox.showerror(self.strings["error"], self.strings["select_model"])
                return
            firmware_file = None
            firmware_model = self.models_listbox.get(self.models_listbox.curselection()[0])
        
        # Kontrola kompatibility SD karty
        is_compatible, error_message = check_drive_compatibility(selected_drive)
        
        if not is_compatible:
            # Nabídneme uživateli možnost přeskočit kontrolu a pokračovat
            force_result = messagebox.askyesno(
                "Nekompabilní SD karta", 
                f"{error_message}\n\nChcete přesto pokračovat s instalací CHDK?\n"
                "(Použijte tuto volbu pouze pokud víte, že karta je naformátována správně)"
            )
            if not force_result:
                return
        
        # Confirm installation
        result = messagebox.askyesno(
            "Instalace CHDK", 
            f"Opravdu chcete nainstalovat CHDK na SD kartu {selected_drive}?\n\n"
            "SD karta bude nastavena jako bootovatelná a budou na ni nahrány soubory CHDK."
        )
        if not result:
            return
        
        # Logování operace
        logger.info(f"Zahájení instalace CHDK na disk {selected_drive}")
        if firmware_file:
            logger.info(f"Používám vlastní firmware soubor: {firmware_file}")
        else:
            logger.info(f"Používám předinstalovaný firmware modelu: {firmware_model}")
        
        # Run the installation process
        self.status_var.set(self.strings["starting_install"])
        self.progress_var.set(5)
        self.root.update_idletasks()
        
        try:
            # Make the card bootable
            self.status_var.set(self.strings["making_bootable"])
            self.progress_var.set(30)
            self.root.update_idletasks()
            make_bootable(selected_drive)
            logger.info(f"Disk {selected_drive} nastaven jako bootovatelný")
            
            # Install CHDK
            self.status_var.set(self.strings["installing"])
            self.progress_var.set(60)
            self.root.update_idletasks()
            
            if self.firmware_source_var.get() == "custom":
                # Instalace z vybraného souboru
                logger.info(f"Instaluji CHDK z vlastního souboru: {firmware_file}")
                install_firmware_file(selected_drive, firmware_file)
            else:
                # Instalace předinstalovaného firmware
                logger.info(f"Instaluji předinstalovaný CHDK firmware pro model: {firmware_model}")
                self.models_manager.install_model_firmware(firmware_model, selected_drive)
            
            self.progress_var.set(100)
            self.status_var.set(self.strings["install_complete"])
            logger.info(f"Instalace CHDK na disk {selected_drive} dokončena úspěšně")
            messagebox.showinfo(self.strings["success"], self.strings["install_success"])
            self.root.after(2000, lambda: self.progress_var.set(0))
            
        except Exception as e:
            self.progress_var.set(0)
            self.status_var.set(f"{self.strings['error']}: {str(e)}")
            logger.error(f"Chyba při instalaci CHDK: {str(e)}")
            messagebox.showerror(self.strings["install_error"], str(e))
    
    def check_card_compatibility(self):
        """Zkontroluje kompatibilitu vybrané SD karty"""
        selected_drive = self.drive_combobox.get()
        if not selected_drive:
            messagebox.showerror(self.strings["error"], self.strings["select_card"])
            return
        
        self.status_var.set("Kontroluji kompatibilitu...")
        self.progress_var.set(30)
        self.root.update_idletasks()
        
        try:
            is_compatible, error_message = check_drive_compatibility(selected_drive)
            
            if is_compatible:
                # Pokud je vráceno varování (kompatibilní, ale s výhradou)
                if error_message and error_message.startswith("VAROVÁNÍ"):
                    self.progress_var.set(80)
                    self.status_var.set("Karta může být kompatibilní")
                    messagebox.showwarning(
                        "Možná kompatibilní", 
                        f"{error_message}\n\nMůžete zkusit pokračovat s instalací."
                    )
                    self.root.after(1000, lambda: self.progress_var.set(0))
                else:
                    self.progress_var.set(100)
                    self.status_var.set("Karta je kompatibilní")
                    messagebox.showinfo(
                        "Kontrola kompatibility", 
                        f"SD karta {selected_drive} je kompatibilní s CHDK.\n\n"
                        "Můžete pokračovat nastavením bootovatelnosti a instalací CHDK."
                    )
                    self.root.after(1000, lambda: self.progress_var.set(0))
            else:
                # Nabídneme uživateli možnost přeskočit kontrolu a pokračovat
                force_result = messagebox.askyesno(
                    "Nekompabilní SD karta", 
                    f"{error_message}\n\nChcete přesto označit kartu jako kompatibilní?\n"
                    "(Použijte tuto volbu pouze pokud víte, že karta je naformátována správně)"
                )
                
                if force_result:
                    self.progress_var.set(100)
                    self.status_var.set("Karta označena jako kompatibilní")
                    messagebox.showinfo(
                        "Kontrola přeskočena", 
                        f"SD karta {selected_drive} byla ručně označena jako kompatibilní.\n\n"
                        "Můžete pokračovat nastavením bootovatelnosti a instalací CHDK."
                    )
                    self.root.after(1000, lambda: self.progress_var.set(0))
                else:
                    self.progress_var.set(0)
                    self.status_var.set(f"Karta není kompatibilní: {error_message}")
                    messagebox.showerror("Kontrola kompatibility", error_message)
            
        except Exception as e:
            self.progress_var.set(0)
            self.status_var.set(f"Chyba: {str(e)}")
            messagebox.showerror("Chyba", f"Při kontrole kompatibility nastala chyba: {str(e)}")

    def make_card_bootable(self):
        """Samostatné nastavení bootovatelnosti SD karty"""
        selected_drive = self.drive_combobox.get()
        if not selected_drive:
            messagebox.showerror(self.strings["error"], self.strings["select_card"])
            return
        
        # Run bootable setup
        self.status_var.set(self.strings["making_bootable"])
        self.progress_var.set(40)
        self.root.update_idletasks()
        
        try:
            make_bootable(selected_drive)
            self.progress_var.set(100)
            self.status_var.set("Bootovatelnost nastavena")
            messagebox.showinfo(self.strings["success"], "SD karta byla úspěšně nastavena jako bootovatelná!")
            self.root.after(2000, lambda: self.progress_var.set(0))
        except Exception as e:
            self.progress_var.set(0)
            self.status_var.set(f"{self.strings['error']}: {str(e)}")
            messagebox.showerror(self.strings["error"], f"Chyba při nastavování bootovatelnosti: {str(e)}")

    def format_card(self):
        """Zobrazí instrukce pro ruční formátování SD karty"""
        messagebox.showinfo(
            "Ruční formátování SD karty",
            "Aplikace již nepodporuje automatické formátování SD karet.\n\n"
            "Pro formátování SD karty prosím postupujte takto:\n"
            "1. Otevřete Průzkumník Windows\n"
            "2. Pravým tlačítkem klikněte na SD kartu\n"
            "3. Zvolte možnost 'Formátovat...'\n"
            "4. Vyberte formát 'FAT32'\n"
            "5. Klikněte na 'Spustit'\n\n"
            "Po formátování můžete pokračovat nastavením bootovatelnosti a instalací CHDK."
        )

    def open_website(self, url):
        """Otevře webovou stránku v prohlížeči"""
        import webbrowser
        webbrowser.open(url)

    def on_window_resize(self, event):
        """Reaguje na změnu velikosti okna a upravuje šířku obsahu"""
        # Pouze když se událost týká hlavního okna
        if event.widget == self.root and hasattr(self, 'main_canvas'):
            # Upravuje šířku scrollovatelného obsahu podle velikosti okna
            canvas_width = event.width - 20  # Odečteme šířku scrollbaru
            self.main_canvas.itemconfig(1, width=canvas_width)  # První item v canvas je náš rámec

if __name__ == "__main__":
    try:
        # Kontrola existence potřebných složek
        assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
        if not os.path.exists(assets_dir):
            os.makedirs(assets_dir)
            print(f"Vytvořena chybějící složka: {assets_dir}")
        
        # Výběr jazyka před spuštěním aplikace
        selected_language = select_language()
        
        # Spuštění aplikace s vybraným jazykem
        root = tk.Tk()
        app = CHDKInstallerApp(root, language=selected_language)
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
