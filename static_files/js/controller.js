(function(controller) {
    var View = alzod.View;
    var Model = alzod.Model;
    var Controller = alzod.Controller;
    var timer = 0;
    var check_add_method = function() {
        if("add" in View && "fetch_script" in Model) {
            controller(View, Model, Controller);
        }
        else {
            clearTimeout(timer);
            if(Controller.handle_repetition < Controller.max_repetition) {
                timer = setTimeout(check_add_method, 100);
                console.log('add not in View');
            }
        }
    };
    //check_add_method();
    setTimeout(check_add_method, 1000);
})(function(View, Model, Controller) {

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


document.onsubmit = function(event) {
    event.preventDefault();
    event.stopPropagation();
    try {
        var form_data = event.target.serialize();
        form_data.event_target = event.target;
        Controller.fetch(event.target.action, "post", form_data);
    }
    catch(error) { 
        View.show_error("on submit form error: " + error); 
    }
};


window.onpopstate = function(event) {
    if(event.state) {
        if(event.state.index >= View.current_index) {
            View.current_index++;
            View.handle_ok_response(event.state.content);
            return null;
        }
    }
    View.current_index--;
    View.remove_last_view();
    View.hide_error();
};

// Controller attributes:



// Controller methods:


Controller.handle_response = function(status, url, request, data) {
    if(1 < status) {
        var content = "";
        try { 
            content = JSON.parse(request.responseText);
            content.type = content.type || "test";
            content.url = url;
            content.url_path = url.replace(/.*\/\/[^\/]+/, '')
            content.url_clean = content.url_path
                .replace(/(?:^\/|\/$)/g, "")
                .replace("api/item/", "");
        } 
        catch(error) { View.show_error("JSON.parse(response): " + error); }

        if(typeof content === "object" && content.constructor === Object) {
            Controller.handle_JSON_response(status, content, data);
        } 
        else { View.show_error('response is not JSON!'); }
    } 
    else { View.show_error('Internet connection is offline!'); }
};


Controller.handle_JSON_response = function(status, content, data) {
    // https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
    console.log(">>>>>>>>>>>status",status);
    console.log(">>>>>>>>>>>content",content);
    console.log(">>>>>>>>>>>data",data);
    if(status == 200 || status == 201) { // 200 OK, 201 Created
        View.handle_ok_response(content);
    }
    else if(status == 400) { // 400 Bad Request
        View.handle_form_error(content, data.event_target);
    }
    else if(status == 401) { // 401 Unauthorized
        console.warn(content, data);
        console.log(data.event_target);
        View.hide_loading();
    }
    else if(status == 403) { // 403 Forbidden
        console.log("403 Forbidden");
        View.hide_loading();
    }
    else if(status == 404) { // 404 Not Found
        console.log("404 Not Found");
        View.hide_loading();
    }
    else {
        // 202 Accepted
        // 500 Internal Server Error
        // 501 Not Implemented
        // 503 Service Unavailable
        View.show_error("Error in handle_response: status("+ status +")");
    }
};


Controller.push_to_history = function(content) {
    if(!content.in_history) {
        content.in_history = true;
        var page_info = {
            index: View.current_index++, 
            content: content
        };
        var url = page_info.content.url_clean;
        url = isNaN(url) ? url : "/" + url;
        if(View.blocked(url)) {
            url = "/user/";
        }
        try { window.history.pushState(page_info, null, url); }
        catch(error) { 
            window.history.pushState(page_info, null, "/error")
            View.show_error("history.pushState: " + error); 
        }
    }
};






// run after load:

Controller.fetch("/api/auth/");

if(Controller.initial_data) {
    var args = Controller.initial_data;
    Controller.handle_response(args[0], args[1], args[2]);
}
else { View.show('view_home'); }
}); // end of controller function.