(function() {

var AppBase = function(obj_id) {
    var index = Controller.auto_id++;
    obj_id = obj_id || "app_" + index;
    return {
        "id": obj_id,
        "index": index,
        "hide": function() {
            var div = document.getElementById(obj_id);
            if(div) { div.setAttribute("class", "none"); }
            else { Controller.error.show(obj_id + " not found!"); }
        },
        "show": function() {
            for (var app in Controller.running) { 
                Controller.running[app].hide(); 
            }
            var div = document.getElementById(obj_id);
            div.setAttribute("class", "app");
            Controller.loading.hide();
        },
        "remove": function() {
            document.getElementById(obj_id).remove();
            delete Controller.running[obj_id];
            Controller.show_last_app();
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

Controller.show_last_app = function() {
    var last = "app_home";
    var index = 0;
    for (var app in Controller.running) { 
        if(index < Controller.running[last].index) { 
            last = app; 
        }
    }
    Controller.show(last);
};

Controller.add = function(obj) {
    if(obj.type in Controller.view) {
        var app = AppBase();
        app.type = obj.type;
        app.href = obj.href;
        app.content = obj.content;
        var content = Controller.view[obj.type](app);
        var app_div = document.createElement('div');
        app_div.className = "none";
        app_div.id = app.id;
        app_div.appendChild(content);
        document.getElementById('app_root').appendChild(app_div);
        Controller.running[app.id] = app;
        Controller.show(app.id);
    }
    else {
        Controller.model.fetch_script(obj);
    }
};

Controller.auto_id = 100;

Controller.running.app_home = AppBase("app_home");
Controller.running.app_home.index = 1;
if(!Controller.initial_item) {
    Controller.show('app_home');
}
})();