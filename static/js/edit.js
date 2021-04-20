function editDisplayname() {
    const blur = document.getElementById('main-container')
    blur.classList.toggle('active')
    const display = document.getElementById('display')
    display.classList.toggle('active')
}

function editPhoto() {
    const blur = document.getElementById('main-container')
    blur.classList.toggle('active')
    const popup = document.getElementById('popup')
    popup.classList.toggle('active')
}

function editBio() {
    const blur = document.getElementById('main-container')
    blur.classList.toggle('active')
    const bio = document.getElementById('bio')
    bio.classList.toggle('active')
}

function followUser() {
    const blur = document.getElementById('main-container')
    blur.classList.toggle('active')
    const follow = document.getElementById('follow-user')
    follow.classList.toggle('active')
}

function unfollowUser() {
    const blur = document.getElementById('main-container')
    blur.classList.toggle('active')
    const unfollow = document.getElementById('unfollow-user')
    unfollow.classList.toggle('active')
}