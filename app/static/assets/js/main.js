const navLinks = document.querySelectorAll('.nav__link');
const currentPath = window.location.pathname;

navLinks.forEach(link => {
    const linkPath = link.getAttribute('href');
    
    if (currentPath === linkPath) {
        link.classList.add('active-link');
    } else {
        link.classList.remove('active-link');
    }
});

