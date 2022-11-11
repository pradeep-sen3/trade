function parseJSON(json_obj) {
    html = '';
    html += '<tr>' +
                '<th>' + 'Logo' + '</th>' +
                '<th>' + 'Symbol' + '</th>' +
                '<th>' + 'Shares' + '</th>' +
            '</tr>'
    for (var i in json_obj) {
        html += `<tr class = "trigger">
                    <td><img class="small-logo" src="${json_obj[i].logo}" alt=""></td>
                    <td>${json_obj[i].stock_id}</td>
                    <td>${json_obj[i].shares}</td>
                </tr>`
    }
    return html
}

document.getElementById('symbol').addEventListener('input', load_stocks_by_symbol);
document.getElementById('name').addEventListener('input', load_stocks_by_name);

async function load_stocks_by_symbol() {
    let response = await fetch(`/search_ownership?sym=${this.value}`);
    let data = await response.json();
    document.getElementById('ownership').innerHTML = parseJSON(data);
    initialize();
}

async function load_stocks_by_name() {
    let response = await fetch(`/search_ownership?nm=${this.value}`);
    let data = await response.json();
    document.getElementById('ownership').innerHTML = parseJSON(data);
    initialize();
}

function initialize() {
    Array.from(document.getElementById('ownership').getElementsByClassName('trigger')).forEach(element =>  {
        console.log(element)
        element.addEventListener('click', async function() {
            var type = document.getElementById('plot').value.toLowerCase();
            var sym = this.getElementsByTagName('td')[1].innerText;
            var prd = document.getElementById('period').value;
            document.getElementsByClassName('hidden-info')[0].getElementsByTagName('p')[0].innerText = sym;
            plot(type, sym, prd, this);
        });
    });
}