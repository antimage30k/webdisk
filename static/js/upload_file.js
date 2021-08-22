var log = console.log.bind(console, new Date().toLocaleDateString())

var e = function (selector) {
    return document.querySelector(selector)
}

var fileTempalate = function (filename, url) {
    return `
        <div class="class-file-cell">
            <span>${filename} ${url}</span>
        </div>
    `
}


var getSize = function () {
    var fileInput = e('#id-file')
    fileInput.onchange = function () {
        var file = fileInput.files[0]
        var size = file.size
        var sizeInput = e('#id-size')
        log('file size', size)
        sizeInput.value = size
    }
}


var main = function () {
    getSize()
}