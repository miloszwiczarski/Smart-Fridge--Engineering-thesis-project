const register = document.getElementById('register-collapse');
const login = document.getElementById('login-collapse');
const searchParameters = document.getElementById("search-parameters-collapse")
const searchCollapseButton = document.getElementById('search-collapse-button')

document.onclick = function (e) {
    if (e.target.id === 'register-box-collapse') {
        register.classList.remove('show');
    }
    if (e.target.id === 'login-box-collapse') {
        login.classList.remove('show');
    }
}

searchCollapseButton.addEventListener('mouseenter', () => {
    searchCollapseButton.style.color = "#f4f9f4"
    searchCollapseButton.style.borderColor = "#403f48"
})
searchCollapseButton.addEventListener('mouseleave', () => {
    searchCollapseButton.style.color = ""
    searchCollapseButton.style.borderColor = ""
})


let isClicked = true;
searchCollapseButton.addEventListener('click', () => {


    if (isClicked) {
        searchCollapseButton.style.backgroundColor = "#616161"
        searchCollapseButton.style.color = "#8aae92"
        searchCollapseButton.style.transition = 'transform 250ms';
        searchCollapseButton.style.transform = 'rotate(180deg)';
        searchCollapseButton.style.borderColor = '#616161';

        searchCollapseButton.addEventListener('mouseleave', () => {
            searchCollapseButton.style.color = "#8aae92"
        });

    } else {
        searchCollapseButton.style.backgroundColor = "#8aae92"
        searchCollapseButton.style.color = "#403f48"
        searchCollapseButton.style.transition = 'transform 300ms';
        searchCollapseButton.style.transform = 'rotate(0deg)';
        searchCollapseButton.style.borderColor = '#8aae92';

        searchCollapseButton.addEventListener('mouseleave', () => {
            searchCollapseButton.style.color = "#403f48"
        });
    }
    isClicked = !isClicked;
});


function toLogin() {
    register.classList.remove('show')
    login.classList.toggle('show')
}

function toRegister() {
    login.classList.remove('show')
    register.classList.toggle('show')
}

function openLogin() {
    login.classList.toggle("show")
}

function openRegister() {
    register.classList.toggle("show")
}

function searchCollapse() {
    searchParameters.classList.toggle('show')
}

