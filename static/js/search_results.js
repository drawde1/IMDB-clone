const all = document.getElementById("all")
const movies = document.getElementById("movies")
const actors = document.getElementById("actors")
const search_form = document.getElementById("search_form")
const search_input = document.getElementById("search_input")

all.addEventListener("click", () => {
    search_form.action = "/search/all/"
    search_input.setAttribute("name", "search_all")
})

movies.addEventListener("click", () => {
    search_form.action = "/movies/search/"
    search_input.setAttribute("name", "search_movie")
})

actors.addEventListener("click", () => {
    search_form.action = "/actors/search/"
    search_input.setAttribute("name", "search_actor")
})
