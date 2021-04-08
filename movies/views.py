from django.shortcuts import render
from IMDB.settings import TMDB_KEY, OMDB_KEY
from movies.forms import MovieSearchForm
import requests

# Create your views here.
tmdb_base_url = 'https://api.themoviedb.org/3'
omdb_base_url = 'http://www.omdbapi.com/'


def homepage(request):
    latest_path = '/movie/now_playing'
    popular_path = '/movie/popular'
    top_path = '/movie/top_rated'
    upcoming_path = '/movie/upcoming'
    latest_endpoint = f'{tmdb_base_url}{latest_path}?api_key={TMDB_KEY}'
    popular_endpoint = f'{tmdb_base_url}{popular_path}?api_key={TMDB_KEY}'
    top_endpoint = f'{tmdb_base_url}{top_path}?api_key={TMDB_KEY}'
    upcoming_endpoint = f'{tmdb_base_url}{upcoming_path}?api_key={TMDB_KEY}'
    latest_request = requests.get(latest_endpoint)
    popular_request = requests.get(popular_endpoint)
    top_request = requests.get(top_endpoint)
    upcoming_request = requests.get(upcoming_endpoint)
    latest_data = latest_request.json()
    popular_data = popular_request.json()
    top_data = top_request.json()
    upcoming_data = upcoming_request.json()
    return render(request, 'homepage.html',{
        'latest': latest_data,
        'popular': popular_data,
        'top': top_data,
        'upcoming': upcoming_data
    })


def search_movie(request):
    if request.method == 'POST':
        form = MovieSearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            movie_name = data['search_movie']
            id_path = f'/search/movie'
            endpoint = f'{tmdb_base_url}{id_path}?api_key={TMDB_KEY}&query={movie_name}'
            id_request = requests.get(endpoint)
            if id_request.status_code in range(200, 299):
                request_data = id_request.json()
                results = request_data['results']
                return render(request, 'movies/movie_results.html', {'results': results})
    form = MovieSearchForm()
    return render(request, 'general_form.html', {'form': form})

def movie_detail(request, movie_id):
    movie_path = f'/movie/{movie_id}'
    video_path = f'/movie/{movie_id}/videos'
    reviews_path = f'/movie/{movie_id}/reviews'
    movie_endpoint = f'{tmdb_base_url}{movie_path}?api_key={TMDB_KEY}'
    video_endpoint = f'{tmdb_base_url}{video_path}?api_key={TMDB_KEY}'
    reviews_endpoint = f'{tmdb_base_url}{reviews_path}?api_key={TMDB_KEY}'
    movie_request = requests.get(movie_endpoint)
    video_request = requests.get(video_endpoint)
    reviews_request = requests.get(reviews_endpoint)
    movie_data = movie_request.json()
    imdb_id = movie_data['imdb_id']
    video_data = video_request.json()
    reviews_data = reviews_request.json()
    omdb_endpoint = f'{omdb_base_url}?i={imdb_id}&apikey={OMDB_KEY}'
    omdb_request = requests.get(omdb_endpoint)
    omdb_data = omdb_request.json()
    rotten_tomatoes = omdb_data['Ratings'][1]
    video = video_data['results'][0]
    return render(request, 'movies/movie_detail.html',{
        'data': movie_data,
        'reviews': reviews_data,
        'video': video,
        'omdb': omdb_data,
        'rotten_tomatoes': rotten_tomatoes
    })
