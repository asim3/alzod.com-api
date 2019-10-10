(function(model) {
    var Model = alzod.Model;
    var Controller = alzod.Controller;
    if("Model" in alzod) { model(Model, Controller); }
    else { throw new Error('Model not in alzod'); }
})(function(Model, Controller) {

HTMLFormElement.prototype.serialize = function() {
    var obj = [].reduce.call(this.elements, function(data, elm) {
        var is_valid = false;
        if(elm.name && elm.value) {
            if(elm.type != 'radio' && elm.type != 'checkbox') {
                is_valid = true;
            }
            else { is_valid = elm.checked; }
        }
        if (is_valid) {
            if (elm.type === 'checkbox') {
                data[elm.name] = (data[elm.name] || []).concat(elm.value);
            }
            else if (elm.options && elm.multiple) {
                data[elm.name] = [].reduce.call(elm, function(val, option) {
                    return option.selected ? val.concat(option.value) : val;
                }, []);
            }
            else {
                data[elm.name] = elm.value;
            }
        }
        return data;
    }, {});
    if(obj.encode_url === "url") {
        var url_data = ""; var mark = "";
        for (const key in obj) {
            if (obj.hasOwnProperty(key)) {
                url_data += mark + key + "=" + encodeURIComponent(obj[key]);
                mark = "&";
            }
        }
        return url_data
    }
    return obj;
};

    
// Model attributes:


// Model methods:


Model.post = function(url, type, data) {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function() {
        if(this.readyState === 4) {
            Controller.handle_response(
                this.status, url, request, data);
        }
    };
    request.open(type, url, true);
    if(data === undefined) { request.send(); }
    else {
        var Content_type = 'application/x-www-form-urlencoded';
        var post_data = data.serialize();
        if(typeof post_data === "object" && post_data.constructor === Object) {
            Content_type = 'application/json; charset=utf-8';
            post_data = JSON.stringify(post_data);
        }
        if("get_cookie" in Model) {
            request.setRequestHeader(
                'X-CSRFToken', Model.get_cookie("csrftoken"));
        }
        request.setRequestHeader('Content-type', Content_type);
        request.send(post_data);
    }
};


Model.fetch_script = function(content) {
    var head = document.getElementsByTagName('head')[0];
    var script = document.createElement('script');
    script.id = "js_script_" + content.type;
    script.type = 'text/javascript';
    script.onload = function() {
        Controller.handle_fetch_script(content);
    };
    script.onerror = function() {
        var error_text = 'adding script to head error!';
        window.onerror(error_text, "js/model.js")
    };
    head.appendChild(script);
    script.src = "/static/js/"+ content.type +".js";
};


Model.get_cookie = function(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
};

}); // end of model function.