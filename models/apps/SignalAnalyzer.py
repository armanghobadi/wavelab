
import numpy as np







class SignalAnalyzer:
    def __init__(self, signal, sampling_rate):
        self.signal = signal
        self.sampling_rate = float(sampling_rate)  # Ensure sampling_rate is float
        self.n = len(signal)
        self.duration = self.n / self.sampling_rate
        self.time = np.linspace(0, self.duration, self.n, endpoint=False)
    
    def calculate_bandwidth(self):
        """Calculate signal bandwidth using FFT"""
        fft_result = np.fft.fft(self.signal)
        fft_freq = np.fft.fftfreq(self.n, 1/self.sampling_rate)
        
        magnitude = np.abs(fft_result)
        threshold = 0.1 * np.max(magnitude)
        significant_freqs = fft_freq[magnitude > threshold]
        
        if len(significant_freqs) > 0:
            return np.max(significant_freqs) - np.min(significant_freqs)
        return 0
    
    def calculate_snr(self):
        signal_power = np.mean(self.signal**2)
        noise = self.signal - np.convolve(self.signal, np.ones(10)/10, mode='same') # استفاده از فیلتر میانگین گیر
        noise_power = np.mean(noise**2)
        return 10 * np.log10(signal_power / noise_power) if noise_power != 0 else float('inf')
    
    def calculate_spectral_efficiency(self, bit_rate):
        """Calculate spectral efficiency (bit/s/Hz)"""
        bandwidth = self.calculate_bandwidth()
        return bit_rate / bandwidth if bandwidth != 0 else 0
    
    def get_analysis_results(self, bit_rate=None):
        """Compile all analysis results"""
        results = {
            'duration': self.duration,
            'bandwidth': self.calculate_bandwidth(),
            'snr': self.calculate_snr(),
            'sampling_rate': self.sampling_rate,
            'samples_count': self.n
        }
        
        if bit_rate is not None:
            results['spectral_efficiency'] = self.calculate_spectral_efficiency(bit_rate)
        
        return results

