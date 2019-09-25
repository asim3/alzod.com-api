Controller.view['search'] = function(view){
    const content_div = document.createElement('div');

    content_div.style = "font-size:30px;";
    const div = document.createElement('div');
    let m = ""
    view.content.map(x => {
        m += x.id + "<br />"
    })
    div.innerHTML = m
    content_div.appendChild(div);

    
    return content_div
};