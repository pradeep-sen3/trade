document.getElementById('share2').addEventListener('change', async function() {
    var sym = this.value.toUpperCase();
    var prd = document.getElementById('period2').value;
    plot_pred(sym, prd, this);
});

document.getElementById('period2').addEventListener('change', async function() {
    var prd = this.value;
    var sym = document.getElementById('share2').value.toLowerCase();
    plot_pred(sym, prd, this);
});

async function plot_pred(sym, prd, parent) {
    parent.style.cursor = 'wait';
    let response = await fetch(`/get_prediction?sym=${sym}&prd=${prd}`);
    let data = await response.json();
    let html = data['plot'];
    iframe = document.getElementById('specific-plot2');
    iframe.contentDocument.write(html);
    iframe.contentDocument.close();
    parent.style.cursor = 'default';
}