const loginDiv = document.getElementById('modalDiv')
const loginButton = document.getElementById('loginButton')
const closeBtn = document.getElementById('closeButton')


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
