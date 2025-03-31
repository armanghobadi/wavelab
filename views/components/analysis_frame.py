import tkinter as tk
from tkinter import ttk

class AnalysisFrame(ttk.LabelFrame):
    def __init__(self, parent, font):
        super().__init__(parent, text="Analysis Results", padding=10)
        self.font = font
        self._create_widgets()
    
    def _create_widgets(self):
        self.analysis_text = tk.Text(self, height=8, width=40, font=self.font)
        self.analysis_text.pack(fill=tk.BOTH, expand=True)
        self.analysis_text.config(state=tk.DISABLED)
    
    def display_results(self, results):
        report = (
            f"=== Signal Analysis Results ===\n"
            f"Duration: {results['duration']:.3f} sec\n"
            f"Sampling Rate: {results['sampling_rate']} Hz\n"
            f"Samples: {results['samples_count']}\n"
            f"Bandwidth: {results['bandwidth']:.2f} Hz\n"
            f"SNR: {results['snr']:.2f} dB\n"
        )
        
        if 'spectral_efficiency' in results:
            report += f"Spectral Efficiency: {results['spectral_efficiency']:.4f} bps/Hz\n"
        
        if 'distance' in results:
            report += f"Estimated Transmission Distance: {results['distance']:.2f} meters\n"
        
        self.analysis_text.config(state=tk.NORMAL)
        self.analysis_text.delete("1.0", tk.END)
        self.analysis_text.insert("1.0", report)
        self.analysis_text.config(state=tk.DISABLED)