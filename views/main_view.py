import numpy as np  
import tkinter as tk
from tkinter import ttk ,  PhotoImage
from PIL import Image, ImageTk  
from ttkthemes import ThemedStyle
from views.components.parameter_frame import ParameterFrame
from views.components.modulation_frame import ModulationFrame
from views.components.encryption_frame import EncryptionFrame
from views.components.analysis_frame import AnalysisFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg





class MainView:
    def __init__(self, root):
        self.root = root
        self.root.title(" WaveLab 0.1 - Advanced Modulation Simulator")
        self.root.geometry("1200x800")

        icon = PhotoImage(file="static/img/icon/icon.png")
        self.root.iconphoto(False, icon)
        
        self._setup_style()
        self._create_widgets()
        
    def _setup_style(self):
        self.style = ThemedStyle(self.root)
        self.style.set_theme("xpnative")
        self.font = ('Tahoma', 10)
        
    def _create_widgets(self):
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left panel (controls)
        left_panel = ttk.Frame(main_container, width=450)
        left_panel.pack(side=tk.LEFT, fill=tk.Y)

        # Right panel (plots)
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create component frames
        self.parameter_frame = ParameterFrame(left_panel, self.font)
        self.parameter_frame.pack(fill=tk.X, pady=5)
        
        self.modulation_frame = ModulationFrame(left_panel, self.font)
        self.modulation_frame.pack(fill=tk.X, pady=5)
        
        self.encryption_frame = EncryptionFrame(left_panel, self.font)
        self.encryption_frame.pack(fill=tk.X, pady=5)
        
        self.analysis_frame = AnalysisFrame(left_panel, self.font)
        self.analysis_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Button panel
        self._create_button_panel(left_panel)
        
        # Plot area
        self._create_plot_area(right_panel)
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def _create_button_panel(self, parent):
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, pady=10)
        
        self.generate_btn = ttk.Button(btn_frame, text="Generate Signal")
        self.generate_btn.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        self.play_btn = ttk.Button(btn_frame, text="Play Audio")
        self.play_btn.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        self.save_signal_btn = ttk.Button(btn_frame, text="Save Signal")
        self.save_signal_btn.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        self.save_plots_btn = ttk.Button(btn_frame, text="Save Plots")
        self.save_plots_btn.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        self.analyze_btn = ttk.Button(btn_frame, text="Analyze Signal")
        self.analyze_btn.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        self.save_analysis_btn = ttk.Button(btn_frame, text="Save Analysis")
        self.save_analysis_btn.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)

        self.info_btn = ttk.Button(
        btn_frame, 
        text="Info",
        command=self.show_copyright  
        )
        self.info_btn.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
    
    def _create_plot_area(self, parent):
        self.fig = plt.figure(figsize=(10, 8), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def get_parameters(self):
        params = {
            'text': self.parameter_frame.get_text(),
            'bit_rate': self.parameter_frame.get_bit_rate(),
            'carrier_freq': self.parameter_frame.get_carrier_freq(),
            'sampling_rate': self.parameter_frame.get_sampling_rate(),
            'duration': self.parameter_frame.get_duration(),
            'amplitude': self.parameter_frame.get_amplitude(),
            'digital_mod': self.modulation_frame.get_digital_mod(),
            'f1': self.modulation_frame.get_f1(),
            'analog_mod': self.modulation_frame.get_analog_mod(),
            'encrypt': self.encryption_frame.get_encrypt_state(),
            'aes_key': self.encryption_frame.get_aes_key(),
            'tx_power': self.parameter_frame.get_tx_power(),
            'snr_threshold': self.parameter_frame.get_snr_threshold()
        }
        return params
    
    def get_sampling_rate(self):
        return self.parameter_frame.get_sampling_rate()
        
    def get_figure(self):
        return self.fig
        
    def display_signal(self, signal_data):
        self.fig.clf()
        params = signal_data['params']
        
        if params['digital_mod']:
            self._plot_digital_signal(signal_data)
        elif params['analog_mod']:
            self._plot_analog_signal(signal_data)
            
        self.fig.tight_layout()
        self.canvas.draw()
        self.update_status("Signal generated successfully")
    
    def _plot_digital_signal(self, signal_data):
        t = signal_data['time']
        digital_signal = signal_data['digital_signal']
        carrier = signal_data['carrier']
        modulated = signal_data['modulated']
        params = signal_data['params']
        
        # Plot digital signal
        ax1 = self.fig.add_subplot(6, 1, 1)
        ax1.plot(t[:len(digital_signal)], digital_signal)
        ax1.set_title('Digital Signal (Input Data)')
        ax1.set_ylim(-0.5, 1.5)
        
        # Plot carrier
        ax2 = self.fig.add_subplot(6, 1, 2)
        ax2.plot(t, carrier)
        ax2.set_title('Carrier Signal')
        
        # Plot modulated signal
        ax3 = self.fig.add_subplot(6, 1, 3)
        ax3.plot(t, modulated)
        ax3.set_title(f'Modulated Signal ({params["digital_mod"]})')
        
        # Plot Modulated Signal + Digital Signal

        ax4 = self.fig.add_subplot(6, 1, 4)
        digital_normalized = digital_signal / np.max(np.abs(digital_signal))
        modulated_normalized = modulated / np.max(np.abs(modulated))
        
        ax4.plot(t[:len(digital_signal)], digital_normalized, 'r', label='Digital Signal', alpha=0.7)
        ax4.plot(t, modulated_normalized, 'b', label=f'Modulated Signal', alpha=0.5)
        ax4.set_title('Signal Comparison')
        ax4.legend()
        ax4.grid(True)



        # Plot spectrum
        ax5 = self.fig.add_subplot(6, 1, 5)
        fft_result = np.fft.fft(modulated)
        fft_freq = np.fft.fftfreq(len(modulated), 1/params['sampling_rate'])
        magnitude_db = 20 * np.log10(np.abs(fft_result[:len(fft_freq)//2]) + 1e-10)
        valid_freq = fft_freq[:len(fft_freq)//2]
        max_freq = params['sampling_rate']/2
        mask = (valid_freq >= 0) & (valid_freq <= max_freq)

        ax5.semilogy(valid_freq[mask], np.abs(fft_result[:len(fft_freq)//2][mask]))
        ax5.set_title('Frequency Spectrum (Linear Scale)')
        ax5.set_xlabel('Frequency (Hz)')
        ax5.set_ylabel('Magnitude')
        ax5.grid(True)

        if params['digital_mod'] == "FSK":
            ax5.axvline(x=params['carrier_freq'], color='r', linestyle='--', alpha=0.5, 
                        label=f'F0: {params["carrier_freq"]} Hz')
            ax5.axvline(x=params['f1'], color='g', linestyle='--', alpha=0.5, 
                        label=f'F1: {params["f1"]} Hz')
            ax5.legend()

        

        ax6 = self.fig.add_subplot(6, 1, 6)
        ax6.plot(valid_freq[mask], magnitude_db[mask])
        ax6.set_title('Frequency Spectrum (dB Scale)')
        ax6.set_xlabel('Frequency (Hz)')
        ax6.set_ylabel('Magnitude (dB)')
        ax6.grid(True)

        if params['digital_mod'] == "FSK":
            ax6.axvline(x=params['carrier_freq'], color='r', linestyle='--', alpha=0.5)
            ax6.axvline(x=params['f1'], color='g', linestyle='--', alpha=0.5)
    
    def _plot_analog_signal(self, signal_data):
        t = signal_data['time']
        message = signal_data['message']
        carrier = signal_data['carrier']
        modulated = signal_data['modulated']
        params = signal_data['params']
        
        ax1 = self.fig.add_subplot(3, 1, 1)
        ax1.plot(t, message)
        ax1.set_title('Message Signal')
        
        ax2 = self.fig.add_subplot(3, 1, 2)
        ax2.plot(t, carrier)
        ax2.set_title('Carrier Signal')
        
        ax3 = self.fig.add_subplot(3, 1, 3)
        ax3.plot(t, modulated)
        ax3.set_title(f'Modulated Signal ({params["analog_mod"]})')
    
    def update_status(self, message):
        self.status_bar.config(text=message)


    
    def show_copyright(self):
            
            copyright_window = tk.Toplevel(self.root)
            copyright_window.title("About WaveLab 0.1")
            copyright_window.geometry("420x420")
            copyright_window.resizable(False, False)
            copyright_window.configure(bg="#222")  

            
            try:
                icon = tk.PhotoImage(file="static/img/icon/icon.png")
                copyright_window.iconphoto(False, icon)
            except:
                print("⚠ Icon not found!")

            frame = ttk.Frame(copyright_window, padding=20, style="Custom.TFrame")
            frame.pack(fill=tk.BOTH, expand=True)

            
            try:
                image = Image.open("static/img/icon/icon.png")
                image = image.resize((200, 150), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                image_label = tk.Label(frame, image=photo, bg="#222")
                image_label.image = photo  #
                image_label.pack(pady=(0, 10))
                
            except:
                print("⚠ Your photo was not found!")

            
            title_label = ttk.Label(
                frame, text="WaveLab 0.1", font=('Helvetica', 16, 'bold'), style="Custom.TLabel"
            )
            title_label.pack(pady=(0, 10))

            
            version_label = ttk.Label(
                frame, text="Advanced Modulation Simulator\nVersion 0.1 (Beta)", font=('Tahoma', 10),
                style="Custom.TLabel"
            )
            version_label.pack(pady=5)

            
            copyright_label = ttk.Label(
                frame, text="© 2025 Arman Ghobadi\nAll Rights Reserved", font=('Tahoma', 9),
                style="Custom.TLabel"
            )
            copyright_label.pack(pady=10)

            
            close_btn = ttk.Button(frame, text="Close", command=copyright_window.destroy, width=15)
            close_btn.pack(pady=10)

            
            copyright_window.update_idletasks()
            width = copyright_window.winfo_width()
            height = copyright_window.winfo_height()
            x = (copyright_window.winfo_screenwidth() // 2) - (width // 2)
            y = (copyright_window.winfo_screenheight() // 2) - (height // 2)
            copyright_window.geometry(f'+{x}+{y}')

        