function Menu(e) { 
    console.log("Menu icon clicked!");
    let list = document.getElementById('menuList');
    if (e.name === 'menu') {
        e.name = "close";
        list.classList.remove('top-[-400px]');
        list.classList.add('top-16', 'opacity-100');
    } else {
        e.name = "menu";
        list.classList.add('top-[-400px]');
        list.classList.remove('top-16', 'opacity-100');
    }
}
