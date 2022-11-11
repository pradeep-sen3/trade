async function overview(route) {
    let response = await fetch(`/plot_overview_${route}`);
    let data = await response.json();
    let html = data['file'];
    iframe = document.getElementById('shares-distribution');
    iframe.style.height = '500px';
    iframe.src = "blank.html";
    iframe.contentDocument.write(html);
    iframe.contentDocument.close();
  }

document.getElementById('view').addEventListener('change', async function() {
  var type = this.value.toLowerCase();
  overview(type);
});