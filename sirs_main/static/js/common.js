$(function() {
    $("#btnCipher").click(function() {
        // Get the file content
        file = $("#id_file")[0].files[0];
        if (file) {
            filename = file.name;
            $("#id_name").val(filename);
            
            var reader = new FileReader();
            reader.onload = function(e) {
                var content = e.target.result;
                if (content) {
                    var result = sirs.cipher(content);
                    $("#id_iv").val(result.iv);
                    $("#id_key").val(result.key);
                    $("#id_ct").val(result.ct);
                } else {
                    throw "Couldn't get file content.";
                }
            }
            reader.readAsBinaryString(file);
        } else {
            throw "Couldn't get file."
        }
    });

    $("#btnDownload").click(function() {
        var obj = {};
        obj.filename = $("#id_name").val();
        obj.iv = $("#id_iv").val();
        obj.key = $("#id_key").val();
        obj.ct = $("#id_ct").val();
        var result = sirs.decipher(obj);
        sirs.download(obj.filename, result);
    });

    $("#btnDecipher").click(function() {
        $("#btnDownload").trigger('click');
    });

    $("#btnRegister").prop('disabled', true);

    $("#btnGenerate").click(function(event) {
        var text = "Generating asymmetric keys...";
        $("#parInfo").text(text);
        sirs.generateKeyPair(function() {
            text += ".";
            $("#parInfo").text(text);
        }, function(keys) {
            var publicKey = sirs.publicKeyToPem(keys.publicKey);
            var privateKey = sirs.privateKeyToPem(keys.privateKey);
            $("#parInfo").text("Done!");
            $("#id_publicKey").val(publicKey);
            sirs.download("public.pem", publicKey);
            sirs.download("private.pem", privateKey);
            $("#btnGenerate").prop('disabled', true);
            $("#btnRegister").prop('disabled', false);
        });
    });
});