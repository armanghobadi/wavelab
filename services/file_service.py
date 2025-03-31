from tkinter import filedialog, messagebox
from scipy.io import wavfile
import numpy as np

class FileService:
    @staticmethod
    def save_signal(signal, sampling_rate):
        filename = filedialog.asksaveasfilename(
            defaultextension=".wav",
            filetypes=[("WAV Audio File", "*.wav")])
        if filename:
            try:
                wavfile.write(filename, sampling_rate, np.int16(signal * 32767))
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save signal: {str(e)}")
                return False
        return False
    
    @staticmethod
    def save_analysis(results):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text File", "*.txt")])
        if filename:
            try:
                with open(filename, 'w') as f:
                    for key, value in results.items():
                        f.write(f"{key}: {value}\n")
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save results: {str(e)}")
                return False
        return False