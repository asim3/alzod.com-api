alzod.View.scripts.test = function(view){
    var obj = {
        innerHTML: "test " + view.type + ` id(${view.id})`,
        append: {innerHTML: "<pre>"+ JSON.stringify(view, null, 2) + "</pre>"}
    }

    return obj
}