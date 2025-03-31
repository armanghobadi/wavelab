import numpy as np

def calculate_fft(signal, sampling_rate):
    fft_result = np.fft.fft(signal)
    fft_freq = np.fft.fftfreq(len(signal), 1/sampling_rate)
    return fft_result, fft_freq

def normalize_signal(signal):
    return signal / np.max(np.abs(signal))