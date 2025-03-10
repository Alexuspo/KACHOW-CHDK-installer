import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from sd_operations import get_drives, format_drive_to_fat32, make_bootable
from chdk_installer import install_chdk, list_available_models, install_firmware_file
from language_selector import select_language
from languages import CZECH, ENGLISH

class CHDKInstallerApp:
    def __init__(self, root, language='cs'):
        self.root = root
        
        # Nastavení jazyka
        self.language = language
        self.strings = CZECH if language == 'cs' else ENGLISH
        
        self.root.title(self.strings["app_title"])
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
        
        title_label = ttk.Label(header_frame, text=self.strings["app_title"], style="Header.TLabel")
        title_label.pack(side=tk.LEFT)
        
        # Uvítací zpráva / krátký popis
        welcome_label = ttk.Label(main_frame, text=self.strings["welcome_text"], wraplength=600, 
                                 justify="center", padding=(0, 5))
        welcome_label.pack(fill=tk.X, pady=5)
        
        # Notebook pro organizaci obsahu
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
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
        # SD Card selection frame
        sd_frame = ttk.LabelFrame(parent_frame, text=self.strings["step1_title"], padding=10)
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
        
        # Format checkbox
        format_frame = ttk.Frame(sd_frame)
        format_frame.pack(fill=tk.X, pady=5)
        
        self.format_var = tk.BooleanVar(value=True)
        format_check = ttk.Checkbutton(format_frame, text=self.strings["format_card"], variable=self.format_var)
        format_check.pack(side=tk.LEFT)
        
        # Warning label
        warning_label = ttk.Label(sd_frame, text=self.strings["format_warning"],
                               style="Warning.TLabel", wraplength=550)
        warning_label.pack(fill=tk.X, pady=5)
        
        # CHDK Selection frame
        chdk_frame = ttk.LabelFrame(parent_frame, text=self.strings["step2_title"], padding=10)
        chdk_frame.pack(fill=tk.X, pady=10)
        
        # Informace o stažení firmwaru
        download_label = ttk.Label(chdk_frame, text=self.strings["download_info"],
                                wraplength=550, justify=tk.LEFT)
        download_label.pack(fill=tk.X, pady=5)
        
        # Odkaz na web
        website_frame = ttk.Frame(chdk_frame)
        website_frame.pack(fill=tk.X, pady=5)
        
        visit_label = ttk.Label(website_frame, text=self.strings["open_firmware_page"])
        visit_label.pack(side=tk.LEFT, padx=(0, 5))
        
        website_button = ttk.Button(website_frame, text=self.strings["open_website"],
                                 command=lambda: self.open_website("https://www.mighty-hoernsche.de/"))
        website_button.pack(side=tk.LEFT)
        
        # Výběr staženého souboru
        file_frame = ttk.Frame(chdk_frame)
        file_frame.pack(fill=tk.X, pady=10)
        
        file_label = ttk.Label(file_frame, text=self.strings["downloaded_file"])
        file_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.firmware_file_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.firmware_file_var, width=40)
        file_entry.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)
        
        browse_file_button = ttk.Button(file_frame, text=self.strings["browse"],
                                     command=self.browse_firmware_file)
        browse_file_button.pack(side=tk.LEFT)
        
        # Instalační tlačítko
        install_frame = ttk.Frame(parent_frame)
        install_frame.pack(pady=15, anchor=tk.CENTER)
        
        install_button = ttk.Button(install_frame, text=self.strings["install_button"], 
                                 command=self.run_installation, style="Install.TButton", 
                                 padding=(20, 10))
        install_button.pack()
    
    def setup_help_tab(self, parent_frame):
        """Nastavení obsahu záložky Nápověda"""
        # Použití scrollovatelného textového pole pro nápovědu
        help_scroll = ttk.Scrollbar(parent_frame)
        help_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        help_text_box = tk.Text(parent_frame, wrap=tk.WORD, height=15, 
                             yscrollcommand=help_scroll.set, bg="#ffffff", padx=10, pady=10)
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
            title=self.strings["select_firmware_file"],
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
        folder_path = filedialog.askdirectory(title=self.strings["select_folder"])
        if folder_path:
            self.custom_folder_entry.delete(0, tk.END)
            self.custom_folder_entry.insert(0, folder_path)
    
    def run_installation(self):
        # Validate selections
        selected_drive = self.drive_combobox.get()
        if not selected_drive:
            messagebox.showerror(self.strings["error"], self.strings["select_card"])
            return
        
        # Kontrola souboru s firmwarem
        firmware_file = self.firmware_file_var.get()
        if not firmware_file or not os.path.exists(firmware_file):
            messagebox.showerror(self.strings["error"], self.strings["select_firmware"])
            return
        
        # Confirm formatting
        if self.format_var.get():
            result = messagebox.askyesno(
                self.strings["format_card"], 
                self.strings["confirm_format"].format(selected_drive)
            )
            if not result:
                return
        
        # Run the installation process
        self.status_var.set(self.strings["starting_install"])
        self.progress_var.set(5)
        self.root.update_idletasks()
        
        try:
            # Format if required
            if self.format_var.get():
                self.status_var.set(self.strings["formatting"])
                self.progress_var.set(20)
                self.root.update_idletasks()
                format_drive_to_fat32(selected_drive)
                self.progress_var.set(50)
                self.root.update_idletasks()
            
            # Make the card bootable
            self.status_var.set(self.strings["making_bootable"])
            self.progress_var.set(70)
            self.root.update_idletasks()
            make_bootable(selected_drive)
            
            # Install CHDK
            self.status_var.set(self.strings["installing"])
            self.progress_var.set(80)
            self.root.update_idletasks()
            install_firmware_file(selected_drive, firmware_file)
            
            self.progress_var.set(100)
            self.status_var.set(self.strings["install_complete"])
            messagebox.showinfo(self.strings["success"], self.strings["install_success"])
            self.root.after(2000, lambda: self.progress_var.set(0))
            
        except Exception as e:
            self.progress_var.set(0)
            self.status_var.set(f"{self.strings['error']}: {str(e)}")
            messagebox.showerror(self.strings["install_error"], str(e))
    
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
