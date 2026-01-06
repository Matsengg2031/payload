import base64

class Decoder:
    @staticmethod
    def xor_decrypt(data_hex, key):
        """Reverses the XOR encryption."""
        # Input is Hex string from custom cipher -> Convert back to chars for XOR
        # Wait, the pipeline was: Base64 -> XOR -> Custom(Shift) -> Hex
        # So Decrypt pipeline: Hex -> Custom(Reverse Shift) -> XOR -> Base64
        
        # 1. Hex to Bytes/String is implicit in next step
        pass # Logic handled in pipeline
        
    @staticmethod
    def reverse_custom_cipher(hex_data, seed):
        """Reverses the custom shift cipher."""
        # 1. Hex to String
        # (Using raw bytes simpler, but keeping string for consistency with JS demo)
        bytes_data = bytes.fromhex(hex_data)
        data = bytes_data.decode('latin1') # usage of latin1 preserves byte values 0-255
        
        # Calculate shift
        shift = 0
        for char in seed:
            shift += ord(char)
        shift = shift % 128
        
        result = []
        for char in data:
            code = ord(char)
            # Reverse shift: (code - shift) mod 256
            # Python's % handles negative numbers correctly for this (e.g. -5 % 256 = 251)
            new_code = (code - shift) % 256
            result.append(chr(new_code))
            
        return "".join(result)

    @staticmethod
    def reverse_xor(data_str, key):
        """Reverses rolling XOR."""
        # Input is the string from previous step (which was hex characters in JS before shift)
        # But wait, JS: XOR -> result (hex formatted string)
        # So data_str here is a hex string
        
        result_chars = []
        # Process 2 chars at a time (Hex)
        for i in range(0, len(data_str), 2):
            hex_pair = data_str[i:i+2]
            val = int(hex_pair, 16)
            
            # Key index
            # The original loop used index in the STRING
            # We must map current hex-pair index to original byte index
            byte_index = i // 2
            key_char = key[byte_index % len(key)]
            
            xor_val = val ^ ord(key_char)
            result_chars.append(chr(xor_val))
            
        return "".join(result_chars)

    @staticmethod
    def decode_pipeline(encrypted_payload, xor_key, custom_seed):
        try:
            # 1. Reverse Custom Cipher
            step1 = Decoder.reverse_custom_cipher(encrypted_payload, custom_seed)
            
            # 2. Reverse XOR
            # step1 is now the Hex string that resulted from XOR
            step2 = Decoder.reverse_xor(step1, xor_key)
            
            # 3. Base64 Decode
            # step2 is the Base64 string
            final_bytes = base64.b64decode(step2)
            
            return final_bytes
        except Exception as e:
            print(f"Decode error: {e}")
            return None
