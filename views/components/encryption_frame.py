from tkinter import ttk, BooleanVar

class EncryptionFrame(ttk.LabelFrame):
    def __init__(self, parent, font):
        super().__init__(parent, text="Data Encryption", padding=10)
        self.font = font
        self.encrypt_var = BooleanVar(value=False)
        self._create_widgets()
        
    def _create_widgets(self):
        ttk.Checkbutton(
            self, 
            text="Enable AES Encryption", 
            variable=self.encrypt_var,
            command=self._toggle_encryption
        ).grid(row=0, column=0, columnspan=2, sticky="w")
        
        ttk.Label(self, text="AES Key (16 bytes):").grid(row=1, column=0, sticky="e")
        self.aes_key_entry = ttk.Entry(self, show="*")
        self.aes_key_entry.grid(row=1, column=1, pady=2, sticky="ew")
        self.aes_key_entry.grid_remove()
    
    def _toggle_encryption(self):
        if self.encrypt_var.get():
            self.aes_key_entry.grid()
        else:
            self.aes_key_entry.grid_remove()
    
    def get_encrypt_state(self):
        return self.encrypt_var.get()
    
    def get_aes_key(self):
        return self.aes_key_entry.get()