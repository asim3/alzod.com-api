alzod.View.scripts.item = function(view){
    var obj = {
        innerHTML: "test " + view.type + ` id(${view.id})`,
        append: {innerHTML: "<h1>"+ view.description + "</h1>"}
    }

    return obj
}