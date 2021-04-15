import requests
from IMDB.settings import TMDB_KEY, OMDB_KEY
tmdb_base_url = 'https://api.themoviedb.org/3'
omdb_base_url = 'http://www.omdbapi.com/'


class ApiPaths():
    latest_path = '/movie/now_playing'
    popular_path = '/movie/popular'
    top_path = '/movie/top_rated'
    upcoming_path = '/movie/upcoming'
    search_path = '/search/multi'
    id_path = '/search/movie'

    def grab_cast(imdb_id):
        omdb_data = ApiPaths.grab_data(imdb_id, omdb=True)

        actors = omdb_data['Actors'].split(", ")
        directors = omdb_data['Director'].split(", ")
        writers = omdb_data['Writer'].split(", ")
        for index, director in enumerate(directors):
            if "(" in director:
                parens_index = director.find("(")
                directors[index] = director[:parens_index]
        for index, writer in enumerate(writers):
            if "(" in writer:
                parens_index = writer.find(" (")
                writers[index] = writer[:parens_index]
        return {'actors': actors, 'directors': directors, 'writers': writers}

    def grab_data(path, query=False, omdb=False):
        url = f'{tmdb_base_url}{path}?api_key={TMDB_KEY}'
        if query:
            url = f'{tmdb_base_url}{path}?api_key={TMDB_KEY}&query={query}'
        if omdb:
            url = f'{omdb_base_url}?i={path}&apikey={OMDB_KEY}'
        request = requests.get(url)
        if request.status_code in range(200, 299):
            data = request.json()
            return data
        return None
