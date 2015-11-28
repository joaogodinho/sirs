"use strict";

(function(root, factory) {
    root.sirs = factory();
})(this, function() {
    var IV_SIZE = 16;
    var KEY_SIZE = 32;
    var CIPHER = "AES-CBC";
    var PAIR_SIZE = 2048;
    var PAIR_EXP = 0x10001;
    var sirs = {};

    // Generates a random key with size = KEY_SIZE
    var generateKey = function() {
        return forge.random.getBytesSync(KEY_SIZE);
    };

    // Generates a random IV with size = IV_SIZE
    var generateIV = function() {
        return forge.random.getBytesSync(IV_SIZE);
    };

    // Converts the given bytes to base64
    var encode = function(bytes) {
        return forge.util.encode64(bytes);
    };

    // Converths the given base64 string into bytes
    var decode = function(str) {
        return forge.util.decode64(str);
    };

    // Ciphers the given content using a random key and IV and
    // returns an object with fields key, iv and ct, all base64 encoded
    sirs.cipher = function(content) {
        if (content) {
            var iv = generateIV();
            var key = generateKey();
            var cipher = forge.cipher.createCipher(CIPHER, key);

            cipher.start({iv: iv});
            cipher.update(forge.util.createBuffer(content));
            cipher.finish();

            var encrypted = cipher.output;
            var output = {key: encode(key),
                          iv: encode(iv),
                          ct: encode(encrypted.data)}
            return output;    
        } else {
            throw "Cipher content cannot be null."
        }
        
    };

    // Deciphers the given ct from object, that must contain key, IV and ct
    // and returns the ct deciphered as bytes
    sirs.decipher = function(obj) {
        if (obj) {
            if (obj.iv && obj.key && obj.ct) {
                var iv = decode(obj.iv);
                var key = decode(obj.key);
                var ct = decode(obj.ct);

                var decipher = forge.cipher.createDecipher(CIPHER, key);
                decipher.start({iv: iv});
                decipher.update(forge.util.createBuffer(ct));
                decipher.finish();

                var deciphered = decipher.output.data;
                return deciphered;
            } else {
                throw "Decipher invalid object."
            }
        } else {
            throw "Decipher object cannot be null."
        }

    };

    // Prompts a download on the browser for file with filename
    // and content.
    sirs.download = function(filename, content) {
        if (filename && content) {
            content = encode(content);
            var pom = document.createElement('a');

            pom.setAttribute('href',
                             'data:application/octet-stream;base64,' + encodeURIComponent(content));
            pom.setAttribute('download', filename);

            if (document.createEvent) {
                var event = document.createEvent('MouseEvents');
                event.initEvent('click', true, true);
                pom.dispatchEvent(event);
            } else {
                pom.click();
            }
        } else {
            throw "Download filename and content cannot be null."
        }
    };

    // Asynchronosly generates a key pair, on every step calls
    // step_func, when done calls done_func and passes the keys as
    // argument
    sirs.generateKeyPair = function(step_func, done_func) {
        var rsa = forge.pki.rsa;
        var pki = forge.pki;
        var state = rsa.createKeyPairGenerationState(PAIR_SIZE, PAIR_EXP);
        var step = function() {
            if(!rsa.stepKeyPairGenerationState(state, 100)) {
                setTimeout(step,1);
                step_func();
            } else {
                var publicPem = publicKeyToPem(state.keys.publicKey);
                var privatePem = privateKeyToPem(state.keys.privateKey);
                done_func(publicPem, privatePem);
            }
        };
        setTimeout(step);
    };

    // Converts a public key object to PEM format
    var publicKeyToPem = function(key) {
        return forge.pki.publicKeyToPem(key);
    };

    // Converts a PEM public key to an object
    var publicKeyFromPem = function(pem) {
        return forge.pki.publicKeyFromPem(pem);
    };

    // Converts a private key object to PEM format
    var privateKeyToPem = function(key) {
        return forge.pki.privateKeyToPem(key);
    };

    // Converts a PEM private key to an object
    var privateKeyFromPem = function(pem) {
        return forge.pki.privateKeyFromPem(pem);
    };

    // Takes public key object and key object and
    // ciphers {key}pubKey
    sirs.cipherKey = function(pubKey, key) {
        pubKey = publicKeyFromPem(pubKey);
        key = decode(key);
        var result = encode(pubKey.encrypt(key));
        return result;
    };

    sirs.decipherKey = function(privKey, ct) {
        privKey = privateKeyFromPem(privKey);
        ct = decode(ct);
        var result = encode(privKey.decrypt(ct));
        return result;
    }

    // Takes a file object and a success function,
    // reads the file and calls success function with
    // filename and content as params
    sirs.readFile = function(file, succ_func) {
        if (file) {
            var filename = file.name;
            var reader = new FileReader();
            reader.onload = function(e) {
                var content = e.target.result;
                if (content) {
                    succ_func(filename, content);
                } else {
                    throw "Coudln't get file content.";
                }
            };
            reader.readAsBinaryString(file);
        } else {
            throw "Couldn't get file."
        }
    };

    return sirs;
});