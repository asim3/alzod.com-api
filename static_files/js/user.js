alzod.View.scripts.user = function(view){
    var obj = {innerHTML: `<h1> id(${view.id}) <h1><br />`, append: []}
    if(view.content.auth){
        obj.append.push({innerHTML: JSON.stringify(view.content)});
    }
    else {
        obj.append.push({element:"input", id: view.id + "username", name:"username",
            type:"textbox", placeholder: "username"
        });
        obj.append.push({element:"input", id: view.id + "password", name:"password",
            type:"password", placeholder: "password"
        });
        obj.append.push({element:"input",type:"submit", value:"Search", 
            onclick: function(){
                var username = document.getElementById(view.id+"username");
                var password = document.getElementById(view.id+"password");
                var data = "username="+ username.value + "&password=" + password.value;
                alzod.Controller.fetch("/login/", "POST", data);
            }
        });
    }
        
    return obj
}