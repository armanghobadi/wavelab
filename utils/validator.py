from tkinter import messagebox

def validate_parameters(params):
    try:
        validated = {
            'text': params['text'],
            'bit_rate': params['bit_rate'] if isinstance(params['bit_rate'], int) else int(params['bit_rate']),
            'carrier_freq': params['carrier_freq'] if isinstance(params['carrier_freq'], float) else float(params['carrier_freq']),
            'sampling_rate': params['sampling_rate'] if isinstance(params['sampling_rate'], int) else int(params['sampling_rate']),
            'duration': params['duration'] if isinstance(params['duration'], float) else float(params['duration']),
            'amplitude': params['amplitude'] if isinstance(params['amplitude'], float) else float(params['amplitude']),
            'digital_mod': params['digital_mod'],
            'f1': params['f1'] if isinstance(params['f1'], float) else float(params['f1']),
            'analog_mod': params['analog_mod'],
            'encrypt': params['encrypt'],
            'aes_key': params['aes_key'],
            'tx_power': params['tx_power'] if isinstance(params['tx_power'], float) else float(params['tx_power']),
            'snr_threshold': params['snr_threshold'] if isinstance(params['snr_threshold'], float) else float(params['snr_threshold'])
        }
        
        if validated['encrypt'] and len(validated['aes_key']) < 16:
            messagebox.showerror("Error", "AES key must be at least 16 characters")
            return None
            
        return validated
    except ValueError as e:
        messagebox.showerror("Error", f"Invalid parameter value: {str(e)}")
        return None