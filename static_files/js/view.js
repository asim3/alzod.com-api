(function(view) {
    if("View" in alzod) {
        view();
    }
    else {
        console.log('View not in alzod')
    }
})(function() {

var ViewBase = function(obj_id) {
    var index = View.auto_id++;
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
            for (var view in View.running) {
                if(View.running.hasOwnProperty(view)) {
                    View.running[view].hide(); 
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


View.running = {};

View.scripts = {};

View.add = function(obj) {
    if(obj.type in View.scripts) {
        obj.href = obj.href.replace("api/item/", "");
        var view = ViewBase();
        view.type = obj.type;
        view.href = obj.href;
        view.content = obj.content;

        var view_div = {
            className: "none",
            id: view.id,
            append: []
        }
        try {
            view_div.append.push(View.scripts.head(view));
            view_div.append.push(View.scripts[view.type](view));
        }
        catch(error) {
            var error_text = "veiw ("+ view.type +") error: " + error;
            Controller.error.show(error_text);
            window.onerror(error_text, "controller.js");
        }
        document.getElementById('all_views').append_by_obj(view_div);
        
        View.running[view.id] = view;
        View.show(view.id);
        if(!obj.in_memory) {
            obj.in_memory = true;
            var page_info = {
                index: View.current_index++, 
                obj: obj
            };
            window.history.pushState(page_info, null, page_info.obj.href);
        }
    }
    else {
        Model.fetch_script(obj);
    }
};


View.show = function(view) { 
    View.running[view].show(); 
};


View.remove = function(view) { 
    View.running[view].remove(); 
};


View.show_last_view = function() {
    var last = "view_home";
    var index = 0;
    for (var view in View.running) { 
        if(index < View.running[view].index) { 
            last = view; 
        }
    }
    View.show(last);
};


View.remove_last_view = function() {
    var last = null;
    var index = 90;
    for (var view in View.running) { 
        if(index < View.running[view].index) { 
            last = view; 
        }
    }
    if(last) {
        View.remove(last);
    }
    View.show_last_view();
};


View.auto_id = 100;

View.running.view_home = ViewBase("view_home");
View.running.view_home.index = 1;


if(!View.initial_item) {
    View.show('view_home');
}

});