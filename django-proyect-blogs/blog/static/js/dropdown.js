document.addEventListener('DOMContentLoaded', function () {
    const menuButton = document.getElementById('menu-button');
    const menu = document.getElementById('dropdown-menu');

    menuButton.addEventListener('click', function () {
        console.log('Botón de menú presionado'); // Para depuración
        menu.classList.toggle('hidden');
        const isExpanded = menuButton.getAttribute('aria-expanded') === 'true';
        menuButton.setAttribute('aria-expanded', !isExpanded);
    });
    
    // Cerrar el menú si se hace clic fuera de él
    window.addEventListener('click', function (event) {
        if (!menuButton.contains(event.target) && !menu.contains(event.target)) {
            menu.classList.add('hidden');
            menuButton.setAttribute('aria-expanded', 'false');
        }
    });
});
