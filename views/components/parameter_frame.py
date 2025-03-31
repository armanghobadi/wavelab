import tkinter as tk
from tkinter import ttk

class ParameterFrame(ttk.LabelFrame):
    def __init__(self, parent, font):
        super().__init__(parent, text="Signal Parameters", padding=10)
        self.font = font
        self._create_widgets()
        
    def _create_widgets(self):
        ttk.Label(self, text="Input Text:").grid(row=0, column=0, sticky="e")
        self.text_input = tk.Text(self, height=3, width=40, font=self.font)
        self.text_input.grid(row=0, column=1, columnspan=3, pady=5)
        self.text_input.insert("1.0", "ABC")
        
        self._create_parameter_entry("Bit Rate (bps):", "bit_rate", 100, 1)
        self._create_parameter_entry("Carrier Freq (Hz):", "carrier_freq", 600, 2)
        self._create_parameter_entry("Sampling Rate (Hz):", "sampling_rate", 44100, 3)
        self._create_parameter_entry("Duration (sec):", "duration", 0.24, 4)
        self._create_parameter_entry("Amplitude:", "amplitude", 1.0, 5)
        self._create_parameter_entry("Tx Power (dBm):", "tx_power", 20, 6)
        self._create_parameter_entry("SNR Threshold (dB):", "snr_threshold", 10, 7)
    
    def _create_parameter_entry(self, label, name, default, row):
        ttk.Label(self, text=label).grid(row=row, column=0, sticky="e")
        entry = ttk.Entry(self)
        entry.grid(row=row, column=1, pady=2)
        entry.insert(0, str(default))
        setattr(self, f"{name}_entry", entry)
    
    def get_text(self):
        return self.text_input.get("1.0", "end-1c")
    
    def get_bit_rate(self):
        return int(self.bit_rate_entry.get())
    
    def get_carrier_freq(self):
        return float(self.carrier_freq_entry.get())
    
    def get_sampling_rate(self):
        return int(self.sampling_rate_entry.get())
    
    def get_duration(self):
        return float(self.duration_entry.get())
    
    def get_amplitude(self):
        return float(self.amplitude_entry.get())
    
    def get_tx_power(self):
        return float(self.tx_power_entry.get())
    
    def get_snr_threshold(self):
        return float(self.snr_threshold_entry.get())