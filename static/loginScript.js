const wrapper = document.querySelector('.wrapper');
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.register-link');
const btnPopup = document.querySelector('.btnLogin-popup');
const iconClose = document.querySelector('.icon-close');

registerLink.addEventListener('click', ()=>{
    wrapper.classList.add('active');
});

loginLink.addEventListener('click', ()=>{
    wrapper.classList.remove('active');
});

btnPopup.addEventListener('click', ()=>{
    wrapper.classList.add('active-popup');
});

iconClose.addEventListener('click', ()=>{
    wrapper.classList.remove('active-popup');
});

function validateForm() {
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    var role_student = document.getElementById("role_student").checked;
    var role_teacher = document.getElementById("role_teacher").checked;
    var role_admin = document.getElementById("role_admin").checked;

    if (email === "") {
        alert("Please input email");
        return false;
    }

    if (password === "") {
        alert("Please input password");
        return false;
    }

    if (!role_student && !role_teacher && !role_admin) {
        alert("Please select a role");
        return false;
    }

    return true;
}