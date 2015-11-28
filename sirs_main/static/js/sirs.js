"use strict";

(function(root, factory) {
    root.sirs = factory();
})(this, function() {
    var IV_SIZE = 16;
    var KEY_SIZE = 32;
    var CIPHER = "AES-CBC";
    var sirs = {};

    // Generates a random key with size = KEY_SIZE
    var generateKey = function() {
        return forge.random.getBytesSync(KEY_SIZE);
    }

    // Generates a random IV with size = IV_SIZE
    var generateIV = function() {
        return forge.random.getBytesSync(IV_SIZE);
    }

    // Converts the given bytes to base64
    var encode = function(bytes) {
        return forge.util.encode64(bytes);
    }

    // Converths the given base64 string into bytes
    var decode = function(str) {
        return forge.util.decode64(str);
    }

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
    }

    return sirs;
});