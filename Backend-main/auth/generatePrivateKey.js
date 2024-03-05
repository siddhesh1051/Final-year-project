const forge = require('node-forge');
const fs = require('fs');

// Generate an RSA key pair
const rsaKeyPair = forge.pki.rsa.generateKeyPair({ bits: 2048 });

// Convert the private key to PEM format
const privateKeyPem = forge.pki.privateKeyToPem(rsaKeyPair.privateKey);

// Save the private key to a file
fs.writeFileSync('private.pem', privateKeyPem);

console.log('Private key generated and saved to private.pem');
