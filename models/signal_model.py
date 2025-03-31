
import numpy as np  # این خط را در ابتدای فایل اضافه کنید



class SignalModel:
    def text_to_bits(self, text):
        """Convert text to binary bits"""
        bytes_data = text.encode('utf-8')
        bits = ''.join(format(byte, '08b') for byte in bytes_data)
        return [int(bit) for bit in bits]