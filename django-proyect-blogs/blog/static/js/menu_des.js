document.addEventListener('DOMContentLoaded', function() {
    const menuBtn = document.getElementById('floating-menu-btn');
    const menuList = document.getElementById('menuList');

    // Mostrar el botón flotante al hacer scroll
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            menuBtn.classList.remove('hidden');
        } else {
            menuBtn.classList.add('hidden');
        }
    });

    // Mostrar/ocultar el menú al hacer clic en el botón flotante
    menuBtn.addEventListener('click', function() {
        menuList.classList.toggle('hidden');
    });
});
