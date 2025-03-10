"""
Dialog pro výběr jazyka aplikace KACHOW CHDK Installer
"""

import tkinter as tk
from tkinter import ttk

class LanguageSelector:
    def __init__(self, master=None):
        """
        Vytvoří dialog pro výběr jazyka.
        
        Vrací: 'cs' pro češtinu, 'en' pro angličtinu
        """
        self.master = master or tk.Tk()
        self.master.title("Výběr jazyka | Language Selection")
        self.master.geometry("400x200")
        self.master.resizable(False, False)
        self.master.withdraw()  # Skryjeme okno dokud nebude připraveno
        
        self.language_code = None
        
        self.create_widgets()
        
        # Vycentrování okna na obrazovce
        self.center_window()
        
        self.master.deiconify()  # Zobrazíme okno
        self.master.protocol("WM_DELETE_WINDOW", lambda: self.set_language('cs'))  # Výchozí při zavření
        
    def create_widgets(self):
        frame = ttk.Frame(self.master, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Nadpis
        title_label = ttk.Label(frame, text="Výběr jazyka | Language Selection", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Text s výzvou
        prompt_label = ttk.Label(frame, text="Vyberte jazyk | Select language:")
        prompt_label.pack(pady=(0, 20))
        
        # Tlačítka
        buttons_frame = ttk.Frame(frame)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        cs_button = ttk.Button(buttons_frame, text="Česky 🇨🇿", 
                             command=lambda: self.set_language('cs'),
                             width=15, padding=10)
        cs_button.pack(side=tk.LEFT, padx=10)
        
        en_button = ttk.Button(buttons_frame, text="English 🇺🇸", 
                             command=lambda: self.set_language('en'),
                             width=15, padding=10)
        en_button.pack(side=tk.RIGHT, padx=10)
        
    def center_window(self):
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
    def set_language(self, lang_code):
        self.language_code = lang_code
        self.master.quit()

def select_language():
    """
    Zobrazí dialog pro výběr jazyka a vrátí kód vybraného jazyka.
    
    Vrací: 'cs' pro češtinu, 'en' pro angličtinu
    """
    root = tk.Tk()
    root.withdraw()  # Skryje hlavní okno
    
    app = LanguageSelector(tk.Toplevel(root))
    root.mainloop()
    
    selected_language = app.language_code
    
    try:
        root.destroy()  # Zavřít root okno
    except:
        pass
        
    return selected_language or 'cs'  # Výchozí čeština, pokud není zvolen jazyk

if __name__ == "__main__":
    # Test dialogu
    lang = select_language()
    print(f"Selected language: {lang}")
