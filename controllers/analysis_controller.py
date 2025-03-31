from models.apps.SignalAnalyzer import SignalAnalyzer
from services.file_service import FileService
import numpy as np  # این خط را در ابتدای فایل اضافه کنید

class AnalysisController:
    def __init__(self, analysis_view):
        self.view = analysis_view
        self.results = None
        
    def analyze(self, signal, sampling_rate, bit_rate=None, tx_power=None, carrier_freq=None, snr_threshold=None):
        analyzer = SignalAnalyzer(signal, sampling_rate)
        self.results = analyzer.get_analysis_results(bit_rate)
        
        if tx_power and carrier_freq and snr_threshold:
            self.results['distance'] = self._calculate_distance(
                tx_power, carrier_freq, snr_threshold, self.results['snr'])
            
        self.view.display_results(self.results)
    
    def _calculate_distance(self, tx_power, frequency, snr_threshold, snr):
        if snr <= 0:
            return 0.0
            
        path_loss_exp = 3.5
        tx_power_w = 10**((tx_power - 30) / 10)
        rx_sensitivity_w = 10**(snr_threshold / 10)
        
        distance = ((tx_power_w / (rx_sensitivity_w * (4 * 3.14159 * frequency / 3e8) ** path_loss_exp))
                  ** (1 / path_loss_exp))
        return distance
    
    def save_results(self):
        if not self.results:
            return
            
        FileService.save_analysis(self.results)