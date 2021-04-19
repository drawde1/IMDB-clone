function toggle() {
    const blur = document.getElementById('main-container')
    blur.classList.toggle('active')
    const popup = document.getElementById('popup')
    popup.classList.toggle('active')
    const dots = document.getElementById('bio-dots')
    dots.classList.toggle('active')
}
