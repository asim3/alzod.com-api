View.scripts.head = function(view) {
    var obj = {
        style: "font-size:30px;",
        append: [{ 
            html: view.type +" - "+ view.id + "X",
            onclick: function() { history.back(); }
        }]
    };
    return obj
};