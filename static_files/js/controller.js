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
        form_data.event_target = event.target;
        Controller.fetch(event.target.action, "post", form_data);
    }
    catch(error) { 
        Controller.error.show("on submit form error: " + error); 
    }
};


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

// Controller attributes:



// Controller methods:


Controller.fetch = function(href, type, data) { 
    Controller.loading.show();
    Model.fetch(href, type, data);
};


Controller.handle_response = function(status, href, response, data) {
    var response_json = "";
    try { 
        response_json = JSON.parse(response); 
        response_json.href = href;
        response_json.clean_href = href.replace(/.*\/\/[^\/]+/, '')
            .replace("api/item/", "");
    }
    catch(error) { Controller.error.show("JSON.parse(response): " + error); }

    if(Controller.is_JSON(response_json)) {
        if(status == 200 || status == 201) {
            View.handle_good_response(response_json);
        }
        else if(status == 400) {
            View.handle_form_error(response_json, data.event_target);
            Controller.loading.hide();
        }
        else if(status == 401 || status == 403) {
            console.warn(response_json, data);
            console.log(data.event_target);
            Controller.loading.hide();
        }
        else {
            Controller.error.show("Error in handle_response: status("+ status +")");
        }
    }
    else {
        Controller.error.show('response is not JSON!');
    }
};


Controller.loading = {
    show: function() {
        var loading_div = document.getElementById('loading_div');
        loading_div.setAttribute("class", "loading_root");
    },
    hide: function() {
        var loading_div = document.getElementById('loading_div');
        loading_div.setAttribute("class", "none");
    }
};


Controller.error = {
    display: false,
    show: function(html) {
        Controller.error.display = true;
        var error_div = document.getElementById('error_div');
        error_div.innerHTML = "<div class='error_text'>"+ html +"</div>";
        error_div.setAttribute("class", "error_root");
        console.error(html);
    },
    hide: function() {
        Controller.error.display = false;
        var error_div = document.getElementById('error_div');
        error_div.innerHTML = "hide";
        error_div.setAttribute("class", "none");
        Controller.loading.hide();
    }
};


Controller.is_JSON = function(obj) {
    if(typeof obj === "object") {
        if(obj.constructor === Object) {
            return true;
        }
    }
    return false;
};


// run after load:


Controller.fetch("/api/auth/");

if(Controller.initial_url) {
    var args = Controller.initial_data;
    Controller.handle_response(args[0], args[1], args[2]);
}
else { View.show('view_home'); }
}); // end of controller function.