(function(model) {
    var View = alzod.View;
    var Model = alzod.Model;
    var Controller = alzod.Controller;
    if("Model" in alzod) { model(View, Model, Controller); }
    else { console.log('Model not in alzod') }
})(function(View, Model, Controller) {

// Model attributes:


// Model methods:


Model.post = function(href, type, data) {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function() {
        if(this.readyState == 4) {
            Controller.handle_response(
                this.status, href, request.responseText, data);
        }
    };
    request.open(type, href, true);
    if(data === undefined) { request.send(); }
    else {
        var Content_type = 'application/x-www-form-urlencoded';
        var post_data = data;
        if(typeof data === "object" && data.constructor === Object) {
            Content_type = 'application/json; charset=utf-8';
            post_data = JSON.stringify(data);
        }
        if("get_cookie" in Model) {
            request.setRequestHeader(
                'X-CSRFToken', Model.get_cookie("csrftoken"));
        }
        request.setRequestHeader('Content-type', Content_type);
        request.send(post_data);
    }
};

Model.fetch_script = function(obj) {
    var head = document.getElementsByTagName('head')[0];
    var script = document.createElement('script');
    script.id = "js_script_" + obj.type;
    script.type = 'text/javascript';
    script.onload = function() { 
      if(obj.type in View.scripts) { View.add(obj); }
      else { 
        Controller.error.show('fetch_script error. '+ obj.type+' not found!');
      }
    };
    script.onerror = function() {
        var error_text = 'adding script to head error!';
        Controller.error.show(error_text);
        window.onerror(error_text, "controller.js")
    };
    head.appendChild(script);
    script.src = "/static/js/"+ obj.type +".js";
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