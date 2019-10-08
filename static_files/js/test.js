alzod.View.scripts.test = function(view){
    var obj = {
        innerHTML: "test " + view.type + ` id(${view.id})`
    }

    return obj
}