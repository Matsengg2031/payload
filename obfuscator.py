
import zlib
import base64
import hashlib
import random
import string

class Obfuscator:
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
    def encrypt_payload(payload_bytes: bytes, key_str: str) -> str:
        """
        Pipeline:
        1. Zlib Compression
        2. RC4 Encryption (Key derived from SHA256 of input key)
        3. Base85 Encoding (Stealthier than Base64)
        """
        # 1. Compress
        compressed = zlib.compress(payload_bytes, level=9)
        
        # 2. Key Derivation (SHA256)
        rc4_key = hashlib.sha256(key_str.encode()).digest()
        
        # 3. Encrypt
        encrypted = Obfuscator.rc4(compressed, rc4_key)
        
        # 4. Encode (Base85)
        # b85encode returns bytes, we want string
        encoded = base64.b85encode(encrypted).decode('utf-8')
        
        return encoded

    @staticmethod
    def generate_junk_code():
        """Generates random Python comments/variables to break signature."""
        vars = [''.join(random.choices(string.ascii_lowercase, k=5)) for _ in range(3)]
        junk = [
            f"# {random.randint(1000,9999)}",
            f"{vars[0]} = {random.randint(1,100)} * {random.randint(1,50)}",
            f"if {vars[0]} > 5000: pass"
        ]
        return "\n".join(junk)

if __name__ == "__main__":
    # Test/Usage
    import sys
    if len(sys.argv) > 1:
        path = sys.argv[1]
        try:
            with open(path, 'rb') as f:
                content = f.read()
            
            # Use 'ROLLING_DAILY_KEY_123' as default key for test
            # In production this comes from the server config
            key = "ROLLING_DAILY_KEY_123"
            result = Obfuscator.encrypt_payload(content, key)
            
            # Print length vs original
            print(f"Original: {len(content)} | Obfuscated: {len(result)}")
            
            # Save to payload.bin for testing
            with open('payload.bin', 'w') as f:
                f.write(result)
            print("Encrypted payload saved to payload.bin")
            
        except Exception as e:
            print(f"Error: {e}")
