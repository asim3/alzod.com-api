Controller.view['search'] = function(view){
    var root = document.createElement('div');
    for (var i=0; i < view.content.length; i++) {
      var id = view.content[i].id;
      var href_root = document.createElement('a');
      href_root.className = "list_box";
      href_root.href = "/" + id;
      href_root.onclick = function(event) {
        event.preventDefault();
        Controller.fetch(this);
      }.bind(id);
      for (var key in view.content[i]) {
        if (view.content[i].hasOwnProperty(key)) {
          var elem = document.createElement('div');
          elem.innerHTML = view.content[i][key];
          if(key == 'img') {
            elem.innerHTML = "";
            elem.style = "background-image: url(" + view.content[i][key] + ");";
          }
          elem.className = key;
          href_root.appendChild(elem);
        }
      }
      root.appendChild(href_root);
    }
    return root
}