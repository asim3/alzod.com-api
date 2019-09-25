Controller.view['test'] = function(view){
    const content_div = document.createElement('div');
    content_div.innerHTML = view.content;
    return content_div
}