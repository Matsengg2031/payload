const crypto = require('crypto');

function generateRandomKey(length) {
    return crypto.randomBytes(length).toString('hex');
}

function generateJunkData(length) {
    return crypto.randomBytes(length).toString('base64').substring(0, length);
}

function generateIV() {
    return crypto.randomBytes(16).toString('hex');
}

module.exports = {
    generateRandomKey,
    generateJunkData,
    generateIV
};
