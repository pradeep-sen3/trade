Array.from(document.getElementsByClassName('alert')).forEach(element => {
    element.getElementsByClassName('icon')[0].addEventListener('click', function() {
        element.remove();
    });
});