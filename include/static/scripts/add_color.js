function compute() {
   // if (!(document.getElementById('view').value === 'Fundamentals')) return;
    var latest_price = document.getElementById('latest_price');
    var previous_price = document.getElementById('previous_price');
    if (latest_price == null) return;
    var high = document.getElementById('high');
    var low = document.getElementById('low');

    var open = document.getElementById('open');
    var close = document.getElementById('close');

    var latest_vol = document.getElementById('latest-volume');
    var previous_vol = document.getElementById('previous-volume');

    var high52 = document.getElementById('high52');
    var low52 = document.getElementById('low52');

    if (compare(latest_price, previous_price) ) {
        set_high(document.getElementById('change') );
        set_high(document.getElementById('change_percent') );
    }
    else {
        set_low(document.getElementById('change') );
        set_low(document.getElementById('change_percent') );
    }

    _ = compare(high, low);

    _ = compare(open, close);

    _ = compare(latest_vol, previous_vol);

    _ = compare(high52, low52);

}

function compare(ob1, ob2) {
    if (parseFloat(ob1.innerText) >= parseFloat(ob2.innerText)) {
        set_high(ob1);
        set_low(ob2);
        return true;
    }
    set_low(ob1);
    set_high(ob2);
    return false;
}

function set_high(ob) {
    ob.classList.add('high');
}

function set_low(ob) {
    ob.classList.add('low');
}