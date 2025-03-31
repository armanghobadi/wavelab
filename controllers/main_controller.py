from tkinter import messagebox
from threading import Thread
from models.signal_model import SignalModel
from models.modulation_model import ModulationModel
from models.encryption_model import EncryptionModel
from controllers.analysis_controller import AnalysisController
from services.audio_service import AudioService
from services.file_service import FileService
from services.plot_service import PlotService
from utils.validator import validate_parameters
import numpy as np  # این خط را در ابتدای فایل اضافه کنید

class MainController:
    def __init__(self, view):
        self.view = view
        self.signal_model = SignalModel()
        self.modulation_model = ModulationModel()
        self.encryption_model = EncryptionModel()
        self.analysis_controller = AnalysisController(self.view.analysis_frame)
        
        self.setup_event_handlers()
        
    def setup_event_handlers(self):
        self.view.generate_btn.config(command=self.handle_generate_signal)
        self.view.play_btn.config(command=self.handle_play_audio)
        self.view.save_signal_btn.config(command=self.handle_save_signal)
        self.view.save_plots_btn.config(command=self.handle_save_plots)
        self.view.analyze_btn.config(command=self.handle_analyze_signal)
        self.view.save_analysis_btn.config(command=self.handle_save_analysis)
        
    def handle_generate_signal(self):
        try:
            params = validate_parameters(self.view.get_parameters())
            
            if params['encrypt']:
                encrypted_text = self.encryption_model.encrypt(params['text'], params['aes_key'])
                if not encrypted_text:
                    return
                params['text'] = encrypted_text
            
            digital_data = self.signal_model.text_to_bits(params['text'])
            if not digital_data:
                return
                
            signal_data = self.modulation_model.generate_signal(digital_data, params)
            self.view.display_signal(signal_data)
            
        except Exception as e:
            messagebox.showerror("Error", f"Signal generation failed: {str(e)}")
    
    def handle_play_audio(self):
        if not self.modulation_model.has_signal():
            messagebox.showwarning("Warning", "Please generate signal first")
            return
            
        Thread(target=AudioService.play_audio, 
              args=(self.modulation_model.get_audio_signal(), 
                    self.view.get_sampling_rate())).start()
    
    def handle_save_signal(self):
        if not self.modulation_model.has_signal():
            messagebox.showwarning("Warning", "Please generate signal first")
            return
            
        FileService.save_signal(
            self.modulation_model.get_audio_signal(),
            self.view.get_sampling_rate()
        )
    
    def handle_save_plots(self):
        PlotService.save_plots(self.view.get_figure())
    
    def handle_analyze_signal(self):
        if not self.modulation_model.has_signal():
            messagebox.showwarning("Warning", "Please generate signal first")
            return
            
        params = self.view.get_parameters()
        try:
            self.analysis_controller.analyze(
                self.modulation_model.get_audio_signal(),
                params['sampling_rate'],
                params.get('bit_rate'),
                params['tx_power'],
                params['carrier_freq'],
                params['snr_threshold']
            )
        except Exception as e:
            messagebox.showerror("Analysis Error", f"Failed to analyze signal: {str(e)}")
    
    def handle_save_analysis(self):
        self.analysis_controller.save_results()