Controller.view['head'] = function(view){
    const content_div = document.createElement('div');
    content_div.style = "font-size:30px;";
    // content_div.innerHTML = view.content + " " + view.id;

    const close_div = document.createElement('div');
    close_div.innerHTML = view.type +" - "+ view.id + "X";
    close_div.onclick = function() { history.back(); };
    content_div.appendChild(close_div);
    
    return content_div
};