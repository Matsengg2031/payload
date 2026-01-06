// @ts-nocheck
const fs = require('fs');
const PNG = require('pngjs').PNG;

class Steganography {
    /**
     * Hides data into a PNG file using LSB (Least Significant Bit).
     * @param {string} inputPngPath Path to source image.
     * @param {string} outputPngPath Path to save the stego image.
     * @param {string} data The data string to hide.
     * @param {string} key Optional key for seeding (not used in simple LSB).
     */
    hide(inputPngPath, outputPngPath, data, _key) {
        return new Promise((resolve, reject) => {
            fs.createReadStream(inputPngPath)
                .pipe(new PNG())
                .on('parsed', function() {
                    // Prepare data: Length (4 bytes) + Data
                    const dataBuffer = Buffer.from(data);
                    const lengthBuffer = Buffer.alloc(4);
                    lengthBuffer.writeUInt32BE(dataBuffer.length, 0);
                    
                    const fullData = Buffer.concat([lengthBuffer, dataBuffer]);
                    const bitsNeeded = fullData.length * 8;
                    
                    if (bitsNeeded > this.width * this.height * 3) { // 3 channels (RGB)
                        reject(new Error("Image too small to hold data"));
                        return;
                    }

                    console.log(`[Stego] Embedding ${fullData.length} bytes into image...`);

                    let dataIndex = 0;
                    let bitIndex = 0;

                    for (let y = 0; y < this.height; y++) {
                        for (let x = 0; x < this.width; x++) {
                            const idx = (this.width * y + x) << 2; // RGBA

                            // Modify R, G, B channels
                            for (let channel = 0; channel < 3; channel++) {
                                if (dataIndex < fullData.length) {
                                    // Get current bit to write
                                    const byte = fullData[dataIndex];
                                    const bit = (byte >> (7 - bitIndex)) & 1;

                                    // Clear LSB and OR with new bit
                                    this.data[idx + channel] = (this.data[idx + channel] & 0xFE) | bit;

                                    bitIndex++;
                                    if (bitIndex === 8) {
                                        bitIndex = 0;
                                        dataIndex++;
                                    }
                                }
                            }
                        }
                    }

                    this.pack().pipe(fs.createWriteStream(outputPngPath))
                        .on('finish', () => {
                            console.log(`[Stego] Saved to ${outputPngPath}`);
                            resolve();
                        });
                })
                .on('error', (err) => reject(err));
        });
    }
}

module.exports = new Steganography();
