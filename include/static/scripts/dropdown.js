document.getElementsByClassName('menu-btn')[0].addEventListener('click', function() {
    this.classList.toggle('active');
    document.getElementsByClassName('navbar')[0].classList.toggle('active');
    document.getElementsByClassName('menu-links')[0].classList.toggle('active');
});