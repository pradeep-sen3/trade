function create_table(transaction) {
    html = `
    <tr>
        <th>Logo</th>
        <th>Symbol</th>
        <th>Shares</th>
        <th>Price</th>
        <th>Date/Time</th>
    </tr>
    `
    for (var i in transaction) {
        html += `
        <tr>
            <td><img class="small-logo" src="${ transaction[i].logo }" alt=""></td>
            <td>${ transaction[i].sym }</td>
            <td>${ transaction[i].shares }</td>
            <td>${ transaction[i].price }</td>
            <td>${ transaction[i].datetime }</td>
        </tr>
        `
    }
    return html;
}

document.getElementById('symbol').addEventListener('input', async function() {
    let response = await fetch(`/history_sym?sym=${this.value}`);
    let data = await response.json();
    document.getElementById('transaction-tab').innerHTML = create_table(data);
});

document.getElementById('sort').addEventListener('change', async function() {
    let response = await fetch(`/history_sort?sort=${this.value}`);
    let data = await response.json();
    document.getElementById('transaction-tab').innerHTML = create_table(data);
});