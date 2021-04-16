const loginDiv = document.getElementById('modal1')
const signupDiv = document.getElementById('modal2')
const loginButton = document.getElementById('loginButton')
const signupButton = document.getElementById('signupButton')


loginButton.addEventListener('click', () => {
    loginDiv.classList.toggle("modal")
})

signupButton.addEventListener('click', () => {
    signupDiv.classList.toggle("modal")
})