const modalDiv = document.getElementById('modal1')
const loginButton = document.getElementById('loginButton')

loginButton.addEventListener('click', () => {
    modalDiv.classList.toggle("modal")
})