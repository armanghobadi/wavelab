import sounddevice as sd
import numpy as np
import threading
from tkinter import messagebox

class AudioService:
    @staticmethod
    def play_audio(signal, sampling_rate):
        """Play audio with robust sample rate handling and error recovery"""
        try:
            # 1. Validate and sanitize input
            if not isinstance(signal, np.ndarray):
                raise ValueError("Signal must be a numpy array")
                
            sampling_rate = int(sampling_rate)
            if not 8000 <= sampling_rate <= 192000:
                raise ValueError(f"Sample rate {sampling_rate}Hz out of range (8k-192k)")

            # 2. Normalize audio signal
            signal = signal / np.max(np.abs(signal)) if np.max(np.abs(signal)) > 0 else signal
            audio = np.int16(signal * 32767)

            # 3. Check device capabilities
            device_info = sd.query_devices(None, 'output')
            supported_rates = (
                device_info['default_samplerate'],
                int(device_info['default_samplerate'] * 0.8),
                int(device_info['default_samplerate'] * 1.25)
            )

            # 4. Try playback with fallback rates
            for rate in [sampling_rate] + list(supported_rates):
                try:
                    sd.play(audio, rate)
                    sd.wait()
                    return True
                except sd.PortAudioError:
                    continue

            # 5. Final fallback to standard rates
            for rate in [44100, 48000, 16000]:
                try:
                    messagebox.showwarning(
                        "Sample Rate Adjusted",
                        f"Using fallback rate {rate}Hz (original {sampling_rate}Hz not supported)"
                    )
                    sd.play(audio, rate)
                    sd.wait()
                    return True
                except sd.PortAudioError:
                    continue

            raise RuntimeError("All playback attempts failed")

        except Exception as e:
            error_msg = (
                f"Audio Error: {str(e)}\n\n"
                f"Sample Rate: {sampling_rate}Hz\n"
                f"Signal Length: {len(signal)} samples\n"
                f"Device: {sd.query_devices(None, 'output')['name']}"
            )
            messagebox.showerror("Playback Failed", error_msg)
            return False