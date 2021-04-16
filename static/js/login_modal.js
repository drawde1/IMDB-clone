const loginDiv = document.getElementById('modalDiv')
const loginButton = document.getElementById('loginButton')
const closeBtn = document.getElementById('closeButton')
// const signupDiv = document.getElementById('modal2')
// const signupButton = document.getElementById('signupButton')


loginButton.addEventListener('click', () => {
    loginDiv.style.display = 'block'
})

closeBtn.addEventListener('click', () => {
    loginDiv.style.display = 'none';
})

window.addEventListener('click', (e) => {
    if (e.target === loginDiv){
        loginDiv.style.display = 'none';
    }
})

// signupButton.addEventListener('click', () => {
//     signupDiv.classList.toggle("modal")
// })