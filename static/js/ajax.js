var log = console.log.bind(console)

var ajax = function (method, path, data, responseCallback) {
    log('ajax request', method, path, data, responseCallback)

    var r = new XMLHttpRequest()
    r.open(method, path, true)
    r.setRequestHeader('Content-Type', 'application/json')

    // response callback
    r.onreadystatechange = function () {
        if (r.readyState === 4) {
            log('ajax response data', r.response)
            var r_data = JSON.parse(r.response)
            responseCallback(r_data)
        }
    }
    data = JSON.stringify(data)
    r.send(data)
}

var ajaxUploadFile = function (method, path, data, responseCallback) {
    log('ajax request', method, path, data, responseCallback)

    var r = new XMLHttpRequest()
    r.open(method, path, true)

    // response callback
    r.onreadystatechange = function () {
        if (r.readyState === 4) {
            log('ajax response data', r.response)
            var r_data = JSON.parse(r.response)
            responseCallback(r_data)
        }
    }

    var form = new FormData()
    for (var key in data) {
        // 规范写法
        if (!data.hasOwnProperty(key)) continue;
        if (data[key] instanceof File) {
            log('is file')
            let f = data[key]
            form.append(key, f)
            form.append('size', f.size)
        } else {
            form.append(key, JSON.stringify(data[key].size))
        }
    }
    r.send(form)
}