(function(controller) {
    if("add" in View) {
        controller();
    }
    else {
        console.log('add not in View')
    }
})(function() {

var form_to_json = function(elements) {
    return [].reduce.call(elements, function(data, elm) {
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
};


document.onsubmit = function(event) {
    event.preventDefault();
    event.stopPropagation();
    try {
        var elements = event.target.elements;
        var form_data = form_to_json(elements);
        Controller.fetch(event.target.action, "post", form_data);
    }
    catch(error) { 
        Controller.error.show("on submit form error: " + error); 
    }
};
    

Controller.handle_fetch = function(status, href, response) {
    if(status == 200 || status == 201) {
        try {
            var response_json = JSON.parse(response);
            if('type' in response_json) {
                response_json.href = href;
                if(href !== "/api/auth/") {
                    View.add(response_json);
                }
                else { console.log(href + " == /api/auth/"); }
            }
            else {
                Controller.error.show('Controller.type not found');
            }
        }
        catch(error) {
            if(error instanceof SyntaxError) {
                Controller.error.show("JSON.parse(response): " + error);
            }
            else { Controller.error.show("View.add(obj): " + error); }
        }
    }
    else if(status == 400 || status == 401 || status == 403) {
        console.warn(response);
        Controller.loading.hide();
    }
    else {
        Controller.error.show("Handle fetch status: " + status);
    }
};


Model.fetch_script = function(obj) {
    var head = document.getElementsByTagName('head')[0];
    var script = document.createElement('script');
    script.id = "js_script_" + obj.type;
    script.type = 'text/javascript';
    script.onload = function() { 
        if(obj.type in View.scripts) {
            View.add(obj);
        }
        else{ 
          Controller.error.show('View.scripts does not contain: '+obj.type);
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


if("onpopstate" in window) {
    window.onpopstate = function(event) {
        if(event.state) {
            if(event.state.index >= View.current_index) {
                View.current_index++;
                View.add(event.state.obj);
                return null;
            }
        }
        View.current_index--;
        View.remove_last_view();
        Controller.error.hide();
    };
}
else { window.onerror("onpopstate not in window!", "controller.js"); }


});