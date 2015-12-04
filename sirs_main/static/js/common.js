"use strict";

$(function() {
    $("#btnCipher").click(function() {
        var file = $("#id_file")[0].files[0];
        var publicPem = $("#id_pubKey").val();

        sirs.readFile(file, function(filename, content) {
            var result = sirs.cipher(content);
            var cipheredKey = sirs.cipherKey(publicPem, result.key);

            $("#id_name").val(filename);
            $("#id_iv").val(result.iv);
            $("#id_ct").val(result.ct);
            $("#id_key").val(cipheredKey);
        });
    });

    $("#btnDownload").click(function() {
        var obj = {};
        var keyCT = $("#id_key").val();
        var privatePem = $("#id_privKey")[0].files[0];

        sirs.readFile(privatePem, function(_, content) {
            var decipheredKey = sirs.decipherKey(content, keyCT);
            $("#id_key").val(decipheredKey);
            obj.filename = $("#id_name").val();
            obj.iv = $("#id_iv").val();
            obj.key = decipheredKey;
            obj.ct = $("#id_ct").val();
            var result = sirs.decipher(obj);
            sirs.download(obj.filename, result);
        });
    });

    $("#btnDecipher").click(function() {
        $("#btnDownload").trigger('click');
    });

    $("#btnRegister").prop('disabled', true);
    $("#btnConfirmShare").prop('disabled', true);

    $("#btnGenerate").click(function(event) {
        var text = "Generating asymmetric keys...";
        $("#parInfo").text(text);
        sirs.generateKeyPair(function() {
            text += ".";
            $("#parInfo").text(text);
        }, function(publicPem, privatePem) {
            $("#parInfo").text("Done!");
            $("#id_publicKey").val(publicPem);
            sirs.download("public.pem", publicPem);
            sirs.download("private.pem", privatePem);
            $("#btnGenerate").prop('disabled', true);
            $("#btnRegister").prop('disabled', false);
        });
    });

    $("#btnShare").click(function (event) {
        var keyCT = $("#id_key").val();
        var privatePem = $("#id_privKey")[0].files[0];
        var publicKey = $("#id_pubKey").val();
        sirs.readFile(privatePem, function (_, content) {
            var decipheredKey = sirs.decipherKey(content, keyCT);
            var cipheredKeyWithPK = sirs.cipherKey(publicKey, decipheredKey)
            $("#id_key").val(cipheredKeyWithPK)
        });
        $("#btnShare").prop('disabled', true);
        $("#btnConfirmShare").prop('disabled',false);
    });


});