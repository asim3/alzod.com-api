(function() {

var ViewBase = function(obj_id) {
    var index = Controller.auto_id++;
    obj_id = obj_id || "view_" + index;
    return {
        "id": obj_id,
        "index": index,
        "hide": function() {
            var div = document.getElementById(obj_id);
            if(div) { div.setAttribute("class", "none"); }
            else { Controller.error.show(obj_id + " not found!"); }
        },
        "show": function() {
            for (var view in Controller.running) {
                if(Controller.running.hasOwnProperty(view)) {
                    Controller.running[view].hide(); 
                }
            }
            var div = document.getElementById(obj_id);
            div.setAttribute("class", "view_root");
            Controller.loading.hide();
        },
        "remove": function() {
            document.getElementById(obj_id).remove();
            delete Controller.running[obj_id];
            Controller.show_last_view();
        }
    };
};

Controller.model.fetch_script = function(obj) {
    var head = document.getElementsByTagName('head')[0];
    var script = document.createElement('script');
    script.id = "js_script_" + obj.type;
    script.type = 'text/javascript';
    script.onload = function() { 
        if(obj.type in Controller.view) {
            Controller.add(obj);
        }
        else{ 
          Controller.error.show('Controller.view does not contain '+obj.type);
        }
    };
    script.onerror = function() { Controller.error.show('adding script!'); };
    head.appendChild(script);
    script.src = "/static/"+ obj.type +".js";
};

Controller.show_last_view = function() {
    var last = "view_home";
    var index = 0;
    for (var view in Controller.running) { 
        if(index < Controller.running[view].index) { 
            last = view; 
        }
    }
    Controller.show(last);
};

Controller.remove_last_view = function() {
    var last = null;
    var index = 90;
    for (var view in Controller.running) { 
        if(index < Controller.running[view].index) { 
            last = view; 
        }
    }
    if(last) {
        Controller.remove(last);
    }
    Controller.show_last_view();
};

Controller.add = function(obj) {
    if(obj.type in Controller.view) {
        var view = ViewBase();
        view.type = obj.type;
        view.href = obj.href;
        view.content = obj.content;

        var view_div = document.createElement('div');
        view_div.className = "none";
        view_div.id = view.id;

        try {
            var head_div = Controller.view.head(view);
            var content_div = Controller.view[view.type](view);
            view_div.appendChild(head_div);
            view_div.appendChild(content_div);
        }
        catch(error) { 
            Controller.error.show("veiw ("+ view.type +") error: " + error); 
        }
        document.getElementById('all_views').appendChild(view_div);
        
        Controller.running[view.id] = view;
        Controller.show(view.id);
        
        if(obj.status !== "in memory") {
            obj.status = "in memory";
            var page_info = {
                index: Controller.current_index++, 
                obj: obj
            };
            window.history.pushState(page_info, null, page_info.obj.href);
        }
    }
    else {
        Controller.model.fetch_script(obj);
    }
};

Controller.auto_id = 100;

Controller.running.view_home = ViewBase("view_home");
Controller.running.view_home.index = 1;

if(!Controller.initial_item) {
    Controller.show('view_home');
}

if("onpopstate" in window) {
    window.onpopstate = function(event) {
        if(event.state) {
            if(event.state.index >= Controller.current_index) {
                Controller.current_index++;
                Controller.add(event.state.obj);
                return null;
            }
        }
        Controller.current_index--;
        Controller.remove_last_view();
    };
}
})();