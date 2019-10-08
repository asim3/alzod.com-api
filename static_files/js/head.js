alzod.View.scripts.head = function(view) {
    console.log("%chead.js ", "background: blue;", view)
    var obj = {
        style: "font-size:30px;",
        append: [{ 
            innerHTML: view.type +" - "+ view.id + " [x]<br />",
            onclick: function() { history.back(); }
        }]
    };

    var login = {};

    
    return obj
};