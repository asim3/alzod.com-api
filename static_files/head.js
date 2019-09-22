SCRIPTS['head'] = function(app){
    const root_div = document.createElement('div');
    root_div.innerHTML = `
        <div style="font-size:30px;">
            ${app.content}  ${app.id} 
        </div>`
    const close_div = document.createElement('div');
    close_div.innerHTML = "X"
    close_div.onclick = app.remove
    root_div.appendChild(close_div)
    return root_div
}