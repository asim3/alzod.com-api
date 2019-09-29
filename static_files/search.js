Controller.view['search'] = function(view){
    var root = document.createElement('div');
    for (var i=0; i < view.content.length; i++) {
        var div = document.createElement('div');
        div.className = "list_box";

        for (var key in view.content[i]) {
          if (view.content[i].hasOwnProperty(key)) {
            var box = document.createElement('div');
            box.className = key;
            box.innerHTML = view.content[i][key];
            div.appendChild(box);
          }
        }
        root.appendChild(div);
    }
    return root
}