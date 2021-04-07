from django.shortcuts import render
from movies.models import Movie
from movies.forms import MovieSearchForm
import requests

# Create your views here.
base_url = 'https://api.themoviedb.org/3'
api_key = 'ea3f0ae618db2e67cd3f57ba270936c4'

def index(request):
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
                return render(request, 'movies/movie_results.html', {'results': results})
    form = MovieSearchForm()
    return render(request, 'general_form.html', {'form': form})

def movie_detail(request, movie_id):
    movie_path = f'/movie/{movie_id}'
    reviews_path = f'/movie/{movie_id}/reviews'
    movie_endpoint = f'{base_url}{movie_path}?api_key={api_key}'
    reviews_endpoint = f'{base_url}{reviews_path}?api_key={api_key}'
    movie_request = requests.get(movie_endpoint)
    reviews_request = requests.get(reviews_endpoint)
    if movie_request.status_code in range(200, 299):
        movie_data = movie_request.json()
        reviews_data = reviews_request.json()
        if not Movie.objects.filter(imbd_id=movie_id).exists():
            Movie.objects.create(imbd_id=movie_id)

        return render(request, 'movies/movie_detail.html', {'data': movie_data, 'reviews': reviews_data})
