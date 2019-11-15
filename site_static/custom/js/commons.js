$(document).ready(function() {
    var file_input = $('#file_input');
    var file_name = $('#file_name');
    var submit_btn = $('#submit_btn');

    file_input.on('change', onFileSelected);

    /**
     * Utility method to format bytes into the most logical magnitude (KB, MB,
     * or GB).
     */
    Number.prototype.formatBytes = function() {
        var units = ['B', 'KB', 'MB', 'GB', 'TB'],
            bytes = this,
            i;

        /* i=0: B(from 1-1023 Bytes)
         * i=1:KB(from 1KB-1023KB)
         * i=2:MB(from 1MB-1023MB)
         * i=3:GB(from 1GB-1023GB)
         * i=4:TB(1TB and Above)
         */
        for (i = 0; bytes >= 1024 && i < 4; i++) {
            bytes /= 1024;
        }

        return bytes.toFixed(2) + units[i];
    }

    /**
     * Displays selected file name and size and enables the submit button for uploading.
     */
    function onFileSelected(e) {
        var file = e.target.files[0];

        file_name.append(file.name + '(' + file.size.formatBytes() + ')');

        file_name.show();
        submit_btn.attr('disabled', false);
    }
});

var size = 0;
var sliceSize = 1048576;  // 1MB= 1048576, 10MB=10485760 Send 10MB Chunks
var uploadId = null;
var isLastChunk = false;

/*
* On submit start Process
*/
function processFile() {
    var file = $("#file_input").prop('files'); // This is your file object
    var start = 0;
    size = file[0].size;
    uploadId = Date.now().toString();
    console.log('Sending File of Size: ' + size);
    send(file, 0, sliceSize);
}

/*
* slicing the file from start to end
*/
function slice(file, start, end) {
    var slice = 'slice'
    if(file[0].mozSlice){
        slice = file.mozSlice
    }else if(file[0].webkitSlice){
        slice = file.webkitSlice
    }
    return file[0][slice](start, end);
}

/*
* Send file chunks
*/
function send(file, start, end) {
    var formdata = new FormData();
    var xhr = new XMLHttpRequest();

    if (size - end < 0) {
        end = size;
    }
    if (end < size) {
        xhr.onreadystatechange = function () {
            if (xhr.readyState == XMLHttpRequest.DONE) {
                console.log('Done Sending Chunk');
                send(file, start + sliceSize, start + (sliceSize * 2));
            }
        }
    } else {
        xhr.onreadystatechange = function () {
            if (xhr.readyState == XMLHttpRequest.DONE) {
                var response = JSON.parse(xhr.responseText);
                var msg = "Successful Job ID=" + response.job
                $("#file_name").html(msg)
            }
        }
        isLastChunk = true;
        console.log('Upload complete');
    }

    xhr.open('POST', '/upload/', true);

    var slicedPart = slice(file, start, end);

    formdata.append('start', start);
    formdata.append('end', end);
    formdata.append('uploadId', uploadId);
    formdata.append('isLastChunk', isLastChunk);
    formdata.append('file', slicedPart);
    console.log('Sending Chunk (Start - End): ' + start + ' ' + end);
    xhr.setRequestHeader("X-CSRFToken", $("#hiddenCsrf").val());
    xhr.send(formdata);
}