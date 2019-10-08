(function(view) {
    var View = alzod.View;
    var Model = alzod.Model;
    var Controller = alzod.Controller;
    if("View" in alzod) { view(View, Model, Controller); }
    else { console.log('View not in alzod') }
})(function(View, Model, Controller) {

var ViewBase = function(obj, view_name) {
    var index = View.auto_id++;
    var obj_id = view_name || "view_" + index;
    return {
        "id": obj_id,
        "index": index,
        "type": obj.type,
        "href": obj.href,
        "clean_href": obj.clean_href,
        "content": obj,
        "hide": function() {
            var div = document.getElementById(obj_id);
            if(div) { div.setAttribute("class", "none"); }
            else { Controller.error.show(obj_id + " not found!"); }
        },
        "show": function() {
            for (var key in View.running) {
                if(View.running.hasOwnProperty(key)) {
                    View.running[key].hide(); 
                }
            }
            var div = document.getElementById(obj_id);
            div.setAttribute("class", "view_root");
            Controller.loading.hide();
        },
        "remove": function() {
            document.getElementById(obj_id).remove();
            delete View.running[obj_id];
            View.show_last_view();
        }
    };
};


// View attributes:

View.current_index = 1;

View.scripts = {};

View.auto_id = 100;

View.running = { view_home: ViewBase({}, "view_home") };

View.running.view_home.index = 1;


// View methods:


View.add = function(obj) {
    if(obj.type in View.scripts) {
        if(View.not_blocked(obj.clean_href)) {
            var view = ViewBase(obj);
            try {
                document.getElementById('all_views').append_by_obj({
                    className: "none", id: view.id, append: [
                        View.scripts.head(view),
                        View.scripts[view.type](view)
                    ]
                });
            }
            catch(error) {
                Controller.error.show("scripts[" + view.type + "]: " + error);
            }
            View.running[view.id] = view;
            View.show(view.id);
            View.push_to_history(obj); // onpopstate => View.add(obj);
        }
    }
    else {
        Controller.error.show('View.scripts['+ obj.type +'] not found!');
    }
};

View.push_to_history = function(obj) {
    if(!obj.in_memory) {
        obj.in_memory = true;
        var page_info = {
            index: View.current_index++, 
            obj: obj
        };
        window.history.pushState(page_info, null, page_info.obj.clean_href);
    }
};

View.show = function(view) { View.running[view].show(); };

View.remove = function(view) { View.running[view].remove(); };

View.show_last_view = function() {
    var last = "view_home";
    var index = 0;
    for (var key in View.running) { 
        if(index < View.running[key].index) { 
            last = key; 
        }
    }
    View.show(last);
};

View.remove_last_view = function() {
    var last = null;
    var index = 90;
    for (var key in View.running) { 
        if(index < View.running[key].index) { 
            last = key; 
        }
    }
    if(last) {
        View.remove(last);
    }
    View.show_last_view();
};


View.handle_good_response = function(response_obj) {
    if('type' in response_obj) {
        if(response_obj.type in View.scripts) {
            View.add(response_obj);
        }
        else {
            Model.fetch_script(response_obj);
        }
    }
    else {
        Controller.error.show('Controller.type not found');
    }
};


View.handle_form_error = function(response_obj, event_target) {
    for (const key in response_obj) {
        if (response_obj.hasOwnProperty(key)) {
            var element = event_target.querySelector("[name="+key+"]");
            if(element){ element.style = "border: 2px solid red;"; }
        }
    }
};


View.not_blocked = function(href) {
    var blocked_href = ["api/auth", "logout", "login"];
    href = href.replace(/(?:^\/|\/$)/g, "");
    if(blocked_href.indexOf(href) === -1) {
        console.log("%c "+href, "color: #fff; background: green;")
        return true;
    }
    console.log("%c blocked "+href, "color: #fff; background: red;")
    return false;
};

}); // end of view function.