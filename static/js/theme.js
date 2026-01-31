function toggleTheme() {
    const theme = document.getElementById('themeStylesheet');
    if (theme.getAttribute('href').includes('light.css')) {
        theme.setAttribute('href', '/static/css/dark.css');
    } else {
        theme.setAttribute('href', '/static/css/light.css');
    }
}