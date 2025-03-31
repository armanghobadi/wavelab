from tkinter import ttk

class ModulationFrame(ttk.LabelFrame):
    def __init__(self, parent, font):
        super().__init__(parent, text="Modulation Parameters", padding=10)
        self.font = font
        self._create_widgets()
        
    def _create_widgets(self):
        # Digital modulation
        ttk.Label(self, text="Digital Modulation:").grid(row=0, column=0, sticky="e")
        self.digital_mod = ttk.Combobox(self, values=["FSK", "PSK", "ASK"], state="readonly")
        self.digital_mod.grid(row=0, column=1, pady=2)
        self.digital_mod.set("FSK")
        
        ttk.Label(self, text="Bit 1 Freq (Hz):").grid(row=1, column=0, sticky="e")
        self.f1_entry = ttk.Entry(self)
        self.f1_entry.grid(row=1, column=1, pady=2)
        self.f1_entry.insert(0, "1200")
        
        # Analog modulation
        ttk.Label(self, text="Analog Modulation:").grid(row=0, column=2, sticky="e")
        self.analog_mod = ttk.Combobox(self, values=["AM", "FM"], state="readonly")
        self.analog_mod.grid(row=0, column=3, pady=2)
        self.analog_mod.set("AM")
    
    def get_digital_mod(self):
        return self.digital_mod.get()
    
    def get_f1(self):
        return float(self.f1_entry.get())
    
    def get_analog_mod(self):
        return self.analog_mod.get()