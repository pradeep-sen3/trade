document.getElementById('shares-input').addEventListener('input', function() {
    var shares = this.value;
    var total = document.getElementById('total');
    var price = parseFloat(document.getElementById('price').innerText.split(' ')[1]);
    if (isNaN(shares) || isNaN(parseInt(shares)) ) {
        total.innerText = `Total: ${price}`;
        return;
    }
    var shares = parseInt(shares);
    total.innerText = `Total: ${(shares * price).toFixed(4)}`;
});