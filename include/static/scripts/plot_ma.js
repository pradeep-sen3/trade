document.getElementById('share').addEventListener('change', async function() {
    var sym = this.value;
    var prd = document.getElementById('period').value;
    plot(sym, prd);
});

document.getElementById('period').addEventListener('change', async function() {
    var prd = this.value;
    var sym = document.getElementById('share').value;
    plot(sym, prd);
});

async function plot(sym, prd) {
    let response = await fetch(`/plot_moving_avg?sym=${sym}&prd=${prd}`);
    let data = await response.json();
    let html = data['file'];
    iframe = document.getElementById('specific-plot');
    iframe.contentDocument.write(html);
    iframe.contentDocument.close();
}