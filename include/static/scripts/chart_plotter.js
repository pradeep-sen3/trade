Array.from(document.getElementById('ownership').getElementsByClassName('trigger')).forEach(element =>  {
    element.addEventListener('click', async function() {
        var type = document.getElementById('plot').value.toLowerCase();
        var sym = this.getElementsByTagName('td')[1].innerText;
        var prd = document.getElementById('period').value;
        document.getElementsByClassName('hidden-info')[0].getElementsByTagName('p')[0].innerText = sym;
        plot(type, sym, prd, this);
    });
});

document.getElementById('plot').addEventListener('change', async function() {
    var type = this.value.toLowerCase();
    var prd = document.getElementById('period').value;
    var sym = document.getElementsByClassName('hidden-info')[0].getElementsByTagName('p')[0].innerText;
    plot(type, sym, prd, this);
});

document.getElementById('period').addEventListener('change', async function() {
    var prd = this.value;
    var type = document.getElementById('plot').value.toLowerCase();
    var sym = document.getElementsByClassName('hidden-info')[0].getElementsByTagName('p')[0].innerText;
    plot(type, sym, prd, this);
});


async function plot(type, sym, prd, parent) {
    document.getElementsByClassName('transactions')[0].innerHTML = `
        <a href="quote?sym=${sym}"><button class="info info-border info-txt info-highlight">Quote</button></a>
        <a href="/buy?sym=${sym}"><button class="success success-border success-txt success-highlight">Buy</button></a>
        <a href="/sell?sym=${sym}"><button class="danger danger-border danger-txt danger-highlight">Sell</button></a>
    `;
    parent.style.cursor = 'wait';
    let response = await fetch(`/plot_${type}?sym=${sym}&prd=${prd}`);
    let data = await response.json();
    let html = data['file'];
    iframe = document.getElementById('specific-plot');
    //iframe.src = "blank.html";
    iframe.contentDocument.write(html);
    iframe.contentDocument.close();
    parent.style.cursor = 'default';
}