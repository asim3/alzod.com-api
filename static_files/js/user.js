alzod.View.scripts.user = function(view){
    var FormObj = alzod.Controller.Form;
    var obj = {innerHTML: `<h1> id(${view.id}) <h1><br />`, append: []}
    
    if(view.content.auth){
        obj.append.push({innerHTML: JSON.stringify(view.content)});
    }

    else {
        var inputs = ['username','password'];
        obj.append.push(FormObj("/login/", inputs, view.id, true));
    }
    
    return obj
}