import base64
import zlib
import hashlib

class Decoder:
    @staticmethod
    def rc4(data: bytes, key: bytes) -> bytes:
        """RC4 Stream Cipher implementation."""
        S = list(range(256))
        j = 0
        for i in range(256):
            j = (j + S[i] + key[i % len(key)]) % 256
            S[i], S[j] = S[j], S[i]

        i = j = 0
        res = bytearray()
        for b in data:
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            res.append(b ^ S[(S[i] + S[j]) % 256])
        return bytes(res)

    @staticmethod
    def decode_pipeline(encrypted_payload, key_str, custom_seed_unused=None):
        """
        Reverse Pipeline:
        1. Base85 Decode
        2. RC4 Decrypt (Key derived from SHA256 of input key)
        3. Zlib Decompress
        """
        try:
            # 1. Base85 Decode
            # encrypted_payload is string
            step1_bytes = base64.b85decode(encrypted_payload)
            
            # 2. Key Derivation
            # Use same derivation as obfuscator
            rc4_key = hashlib.sha256(key_str.encode()).digest()
            
            # 3. RC4 Decrypt
            step2_bytes = Decoder.rc4(step1_bytes, rc4_key)
            
            # 4. Zlib Decompress
            final_bytes = zlib.decompress(step2_bytes)
            
            return final_bytes
        except Exception as e:
            print(f"dec-err: {e}") 
            return None

