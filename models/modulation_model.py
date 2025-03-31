import numpy as np

class ModulationModel:
    def __init__(self):
        self.audio_signal = None
        
    def has_signal(self):
        return self.audio_signal is not None
        
    def get_audio_signal(self):
        return self.audio_signal
        
    def generate_signal(self, digital_data, params):
        t = np.linspace(0, params['duration'], int(params['sampling_rate'] * params['duration']), endpoint=False)
        time_per_bit = int(params['sampling_rate'] / params['bit_rate'])
        
        digital_signal = np.repeat(digital_data, time_per_bit)
        carrier = params['amplitude'] * np.sin(2 * np.pi * params['carrier_freq'] * t)
        
        if params['digital_mod'] == "FSK":
            modulated = self._generate_fsk(t, digital_data, time_per_bit, params)
        elif params['digital_mod'] == "PSK":
            modulated = self._generate_psk(t, digital_data, time_per_bit, params)
        elif params['digital_mod'] == "ASK":
            modulated = self._generate_ask(t, digital_data, time_per_bit, params)
        elif params['analog_mod'] == "AM":
            modulated = self._generate_am(t, params)
        elif params['analog_mod'] == "FM":
            modulated = self._generate_fm(t, params)
            
        self.audio_signal = modulated
        return {
            'time': t,
            'digital_signal': digital_signal,
            'carrier': carrier,
            'modulated': modulated,
            'params': params
        }
    
    def _generate_fsk(self, t, digital_data, time_per_bit, params):
        modulated = np.zeros(len(t))
        for i, bit in enumerate(digital_data):
            start = i * time_per_bit
            end = (i+1) * time_per_bit
            freq = params['f1'] if bit == 1 else params['carrier_freq']
            modulated[start:end] = params['amplitude'] * np.sin(2 * np.pi * freq * t[start:end])
        return modulated
    
    def _generate_psk(self, t, digital_data, time_per_bit, params):
        modulated = np.zeros(len(t))
        for i, bit in enumerate(digital_data):
            start = i * time_per_bit
            end = (i+1) * time_per_bit
            phase = 0 if bit == 1 else np.pi
            modulated[start:end] = params['amplitude'] * np.sin(2 * np.pi * params['carrier_freq'] * t[start:end] + phase)
        return modulated
    
    def _generate_ask(self, t, digital_data, time_per_bit, params):
        modulated = np.zeros(len(t))
        for i, bit in enumerate(digital_data):
            start = i * time_per_bit
            end = (i+1) * time_per_bit
            amp = params['amplitude'] if bit == 1 else 0
            modulated[start:end] = amp * np.sin(2 * np.pi * params['carrier_freq'] * t[start:end])
        return modulated
    
    def _generate_am(self, t, params):
        message_freq = 440
        message = 0.5 * np.sin(2 * np.pi * message_freq * t)
        carrier = params['amplitude'] * np.sin(2 * np.pi * params['carrier_freq'] * t)
        return (1 + message) * carrier
    
    def _generate_fm(self, t, params):
        message_freq = 440
        beta = 5
        return params['amplitude'] * np.sin(2 * np.pi * params['carrier_freq'] * t + 
                                      beta * np.sin(2 * np.pi * message_freq * t))