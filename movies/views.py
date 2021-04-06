from django.shortcuts import render

from movies.forms import MovieSearchForm
import requests

# Create your views here.
base_url = 'https://api.themoviedb.org/3'
api_key = 'ea3f0ae618db2e67cd3f57ba270936c4'

def movie_search(request):
    search_results = {}
    if request.method == 'POST':
        form = MovieSearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            movie_name = data['search_movie']
            id_path = f'/search/movie'
            endpoint = f'{base_url}{id_path}?api_key={api_key}&query={movie_name}'
            id_request = requests.get(endpoint)
            if id_request.status_code in range(200, 299):
                request_data = id_request.json()
                results = request_data['results']
                search_results.update({'results': results})
    form = MovieSearchForm()
    search_results.update({'form': form})
    return render(request, 'movie_results.html', search_results)

def movie_detail(request, movie_id):
    movie_path = f'/movie/{movie_id}'
    endpoint = f'{base_url}{movie_path}?api_key={api_key}'
    movie_request = requests.get(endpoint)
    if movie_request.status_code in range(200, 299):
        request_data = movie_request.json()
        return render(request, 'movie_detail.html', {'data': request_data})
