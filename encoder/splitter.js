const { generateJunkData } = require('../utilities/randomizer.js');

class Splitter {
    /**
     * Splits data into multiple chunks with junk data.
     * @param {string} data The encrypted payload string.
     * @param {number} numChunks Number of chunks to split into.
     */
    split(data, numChunks = 5) {
        const totalLen = data.length;
        const chunkSize = Math.floor(totalLen / numChunks);
        const chunks = [];
        const metadata = {
            order: [], // To randomize order later if needed
            junkMap: [] // To know where junk is (though we will format chunks as JSON to make it easier)
        };

        let currentPos = 0;
        for (let i = 0; i < numChunks; i++) {
            // Last chunk takes remaining
            let end = (i === numChunks - 1) ? totalLen : currentPos + chunkSize;
            
            // Allow some randomness in chunk size
            if (i < numChunks - 1) {
                const variance = Math.floor(Math.random() * 10) - 5; // +/- 5 chars
                end += variance;
            }

            const chunkData = data.substring(currentPos, end);
            currentPos = end;

            // Generate junk
            const junkBefore = generateJunkData(Math.floor(Math.random() * 20) + 5); // 5-25 chars junk
            const junkAfter = generateJunkData(Math.floor(Math.random() * 20) + 5);

            // Structure the chunk
            // In a real sophisticated scenario, we wouldn't use JSON wrapping to save size/sig, 
            // but for this implementation:
            chunks.push({
                id: i,
                data: chunkData,
                j_prefix: junkBefore, 
                j_suffix: junkAfter
            });
            
            metadata.order.push(i);
        }

        return chunks;
    }
}

module.exports = new Splitter();
