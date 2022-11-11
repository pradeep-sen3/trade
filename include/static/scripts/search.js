function parseJSON(json_obj) {
    html = '';
    html += '<tr>' +
                '<th>' + 'Symbol' + '</th>' +
                '<th>' + 'Company Name' + '</th>' +
                '<th>' + 'Options' + '</th>' +
            '</tr>'
    for (var i in json_obj) {
        html += `<tr>
                    <td>${json_obj[i].symbol}</td>
                    <td>${json_obj[i].name}</td>
                    <td>
                        <div class="btns">
                            <a href="quote?sym=${json_obj[i].symbol}"><button class="info info-border info-txt info-highlight">Quote</button></a>
                            <a href="/buy?sym=${json_obj[i].symbol}"><button class="success success-border success-txt success-highlight">Buy</button></a>
                        </div>
                    </td>
                </tr>`
    }
    return html
}

document.getElementById('symbol').addEventListener('input', load_stocks_by_symbol);
document.getElementById('name').addEventListener('input', load_stocks_by_name);

async function load_stocks_by_symbol() {
    let response = await fetch(`/search?sym=${this.value}`);
    let data = await response.json();
    document.getElementById('table').querySelector('table').innerHTML = parseJSON(data);
}

async function load_stocks_by_name() {
    let response = await fetch(`/search?nm=${this.value}`);
    let data = await response.json();
    document.getElementById('table').querySelector('table').innerHTML = parseJSON(data);
}