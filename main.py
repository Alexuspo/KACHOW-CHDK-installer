import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from sd_operations import get_drives, format_drive_to_fat32, make_bootable
from chdk_installer import install_chdk, list_available_models

class CHDKInstallerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CHDK Installer")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Set application icon
        if getattr(sys, 'frozen', False):
            icon_path = os.path.join(sys._MEIPASS, "assets", "icon.ico")
        else:
            icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
            
        try:
            self.root.iconbitmap(icon_path)
        except:
            pass  # Icon not found, ignore
            
        self.create_widgets()
        self.refresh_drives()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="CHDK Installer", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)
        
        # SD Card selection frame
        sd_frame = ttk.LabelFrame(main_frame, text="SD Karta", padding=10)
        sd_frame.pack(fill=tk.X, pady=5)
        
        sd_label = ttk.Label(sd_frame, text="Vyberte SD kartu:")
        sd_label.pack(anchor=tk.W)
        
        # Drives selection and refresh
        drive_frame = ttk.Frame(sd_frame)
        drive_frame.pack(fill=tk.X, pady=5)
        
        self.drive_combobox = ttk.Combobox(drive_frame, state="readonly", width=10)
        self.drive_combobox.pack(side=tk.LEFT, padx=(0, 5))
        
        refresh_button = ttk.Button(drive_frame, text="Obnovit", command=self.refresh_drives)
        refresh_button.pack(side=tk.LEFT)
        
        # Format checkbox
        self.format_var = tk.BooleanVar(value=True)
        format_check = ttk.Checkbutton(sd_frame, text="Formátovat SD kartu (FAT32)", variable=self.format_var)
        format_check.pack(anchor=tk.W)
        
        # Warning label
        warning_text = "VAROVÁNÍ: Formátování smaže všechna data z vybrané SD karty!"
        warning_label = ttk.Label(sd_frame, text=warning_text, foreground="red", wraplength=550)
        warning_label.pack(fill=tk.X, pady=5)
        
        # CHDK Selection frame
        chdk_frame = ttk.LabelFrame(main_frame, text="CHDK", padding=10)
        chdk_frame.pack(fill=tk.X, pady=10)
        
        # Camera model
        model_label = ttk.Label(chdk_frame, text="Vyberte model fotoaparátu:")
        model_label.pack(anchor=tk.W)
        
        self.model_combobox = ttk.Combobox(chdk_frame, state="readonly", width=30)
        self.model_combobox.pack(fill=tk.X, pady=5)
        
        # Load camera models
        try:
            models = list_available_models()
            if models:
                self.model_combobox['values'] = models
                self.model_combobox.current(0)
            else:
                self.model_combobox['values'] = ["Nenalezeny žádné modely CHDK"]
                self.model_combobox.current(0)
        except Exception as e:
            messagebox.showerror("Chyba", f"Nepodařilo se načíst modely fotoaparátů: {str(e)}")
            self.model_combobox['values'] = ["Chyba při načítání modelů"]
            self.model_combobox.current(0)
        
        # Custom CHDK folder option
        custom_chdk_frame = ttk.Frame(chdk_frame)
        custom_chdk_frame.pack(fill=tk.X, pady=5)
        
        self.custom_folder_var = tk.BooleanVar(value=False)
        custom_folder_check = ttk.Checkbutton(custom_chdk_frame, text="Vlastní CHDK složka", 
                                             variable=self.custom_folder_var,
                                             command=self.toggle_custom_folder)
        custom_folder_check.pack(side=tk.LEFT)
        
        self.custom_folder_entry = ttk.Entry(custom_chdk_frame, state="disabled", width=30)
        self.custom_folder_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        browse_button = ttk.Button(custom_chdk_frame, text="Procházet", 
                                  command=self.browse_folder, state="disabled")
        self.browse_button = browse_button
        browse_button.pack(side=tk.LEFT)
        
        # Action buttons
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=20)
        
        install_button = ttk.Button(buttons_frame, text="Instalovat CHDK", 
                                   command=self.run_installation, width=20)
        install_button.pack(side=tk.LEFT, padx=5)
        
        quit_button = ttk.Button(buttons_frame, text="Ukončit", 
                               command=self.root.destroy, width=15)
        quit_button.pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Připraven")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def refresh_drives(self):
        self.status_var.set("Načítání disků...")
        self.root.update_idletasks()
        
        try:
            drives = get_drives()
            self.drive_combobox['values'] = drives
            if drives:
                self.drive_combobox.current(0)
            self.status_var.set("Připraven")
        except Exception as e:
            self.status_var.set("Chyba: " + str(e))
            messagebox.showerror("Chyba", f"Nepodařilo se načíst dostupné disky: {str(e)}")
    
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
        
        selected_model = self.model_combobox.get()
        if "Nenalezeny" in selected_model or "Chyba" in selected_model:
            messagebox.showerror("Chyba", "Není k dispozici žádný model fotoaparátu")
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
        
        # Get CHDK path
        if self.custom_folder_var.get():
            chdk_path = self.custom_folder_entry.get()
            if not os.path.exists(chdk_path):
                messagebox.showerror("Chyba", "Vybraná CHDK složka neexistuje")
                return
        else:
            chdk_path = None  # Use default
        
        # Run the installation process
        self.status_var.set("Probíhá instalace...")
        self.root.update_idletasks()
        
        try:
            # Format if required
            if self.format_var.get():
                self.status_var.set("Formátování SD karty...")
                self.root.update_idletasks()
                format_drive_to_fat32(selected_drive)
            
            # Make the card bootable
            self.status_var.set("Nastavování bootovatelnosti...")
            self.root.update_idletasks()
            make_bootable(selected_drive)
            
            # Install CHDK
            self.status_var.set("Instalace CHDK...")
            self.root.update_idletasks()
            install_chdk(selected_drive, selected_model, custom_path=chdk_path)
            
            self.status_var.set("Instalace dokončena")
            messagebox.showinfo("Úspěch", "CHDK bylo úspěšně nainstalováno!")
            
        except Exception as e:
            self.status_var.set(f"Chyba: {str(e)}")
            messagebox.showerror("Chyba při instalaci", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = CHDKInstallerApp(root)
    root.mainloop()
