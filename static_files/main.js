(function() {
Controller.auto_id = 1;

Controller.model.fetch_script = function(obj) {
    var head = document.getElementsByTagName('head')[0];
    var script = document.createElement('script');
    script.id = "js_script_" + obj.type;
    script.type = 'text/javascript';
    script.onload = function() { 
        if(obj.type in Controller.view) {
            if(['head'].indexOf(obj.type) === -1) { 
                Controller.add(obj);
            }
        }
        else{ 
            ErrorDiv.show('Controller.view does not contain '+obj.type);
        }
    };
    script.onerror = function() { ErrorDiv.show('adding script!'); };
    head.appendChild(script);
    script.src = "http://localhost:8000/static/"+ obj.type +".js";
};

var AppBase = function(obj_id) {
    obj_id = obj_id || "app_" + Controller.auto_id++;
    return {
        "id": obj_id,
        "hide": function() { 
            var div = document.getElementById(obj_id);
            if(div) { div.setAttribute("class", "none"); }
            else { ErrorDiv.show(obj_id + " not found!"); }
        },
        "show": function() { 
            for (var app in Controller.running) { 
                Controller.running[app].hide(); 
            }
            if(obj_id == "app_last") {
                var last = "app_index";
                var sys_apps = ['app_load', 'app_last', 'app_error']
                for (var app in Controller.running) { 
                    if(sys_apps.indexOf(app) == -1) { 
                        last = app; 
                    }
                }
                Controller.running[last].show();
            }
            else {
                var div = document.getElementById(obj_id);
                div.setAttribute("class", "app");
            }
        },
        "remove": function() {
            document.getElementById(obj_id).remove();
            delete Controller.running[obj_id];
            Controller.running["app_last"].show();
        }
    };
};


Controller.add = function(obj) {
    if(obj.type in Controller.view) {
        var app = AppBase();
        app.type = obj.type;
        app.content = obj.content;
        var content = Controller.view[obj.type](app);
        var app_div = document.createElement('div');
        app_div.className = "none";
        app_div.id = app.id;
        app_div.appendChild(content);
        document.getElementById('app_root').appendChild(app_div);
        Controller.running[app.id] = app;
        app.show();
    }
    else {
        Controller.model.fetch_script(obj);
    }
};


Controller.running["app_index"] = AppBase("app_index");
Controller.running["app_load"] = AppBase("app_load");
Controller.running["app_last"] = AppBase("app_last");

Controller.running.app_index.show();
})()