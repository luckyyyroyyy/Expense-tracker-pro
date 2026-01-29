function toggleTheme() {
    let theme = localStorage.getItem("theme");

    if (theme === "dark") {
        setTheme("light");
    } else {
        setTheme("dark");
    }
}

function setTheme(theme) {
    document.getElementById("light-theme").disabled = theme !== "light";
    document.getElementById("dark-theme").disabled = theme !== "dark";
    localStorage.setItem("theme", theme);
}

window.onload = () => {
    const savedTheme = localStorage.getItem("theme") || "light";
    setTheme(savedTheme);
};