const { generateRandomKey: _generateRandomKey } = require('../utilities/randomizer.js');

class Obfuscator {
    constructor() {
        // Custom substitution alphabet for Layer 3 (Simple Vigenere-like or Substitution)
        this.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
    }

    /**
     * Layer 1: Standard Base64 Encoding
     */
    base64Encode(data) {
        return Buffer.from(data).toString('base64');
    }

    /**
     * Layer 2: XOR Encryption with a rolling key
     */
    xorEncrypt(data, key) {
        let result = '';
        for (let i = 0; i < data.length; i++) {
            const charCode = data.charCodeAt(i);
            const keyChar = key.charCodeAt(i % key.length);
            // XOR and convert to hex to avoid unprintable chars issues in next layer
            const xorVal = charCode ^ keyChar;
            result += xorVal.toString(16).padStart(2, '0');
        }
        return result;
    }

    /**
     * Layer 3: Custom Transposition/Cipher (Simple Shift for demo)
     * Real implementation would use a more complex shuffled alphabet based on a seed.
     */
    customCipher(data, seed) {
        // Simple Caesar shift concept based on seed value
        let shift = 0;
        for (let i = 0; i < seed.length; i++) {
            shift += seed.charCodeAt(i);
        }
        shift = shift % 128; // Keep reasonably small

        let result = '';
        for (let i = 0; i < data.length; i++) {
            const charCode = data.charCodeAt(i);
            // Shift char code
            const newChar = String.fromCharCode((charCode + shift) % 256);
            result += newChar;
        }
        // Re-encode to Hex/Base64 to ensure transportability
        return Buffer.from(result, 'binary').toString('hex');
    }

    encrypt(payload, xorKey, customSeed) {
        console.log(`[Obfuscator] Starting encryption...`);
        
        // 1. Base64
        const b64 = this.base64Encode(payload);
        console.log(`[Obfuscator] Layer 1 (Base64) complete. Size: ${b64.length}`);

        // 2. XOR
        const xored = this.xorEncrypt(b64, xorKey);
        console.log(`[Obfuscator] Layer 2 (XOR) complete. Size: ${xored.length}`);

        // 3. Custom Cipher
        const final = this.customCipher(xored, customSeed);
        console.log(`[Obfuscator] Layer 3 (Custom) complete. Size: ${final.length}`);

        return final;
    }
}

module.exports = new Obfuscator();
