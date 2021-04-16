from django.shortcuts import render
from movies.forms import MovieSearchForm, AllSearchForm
from IMDB_user.models import MyCustomUser
from IMDB.settings import TMDB_KEY, OMDB_KEY
from movies.models import Movie
from movies.forms import MovieSearchForm
import requests
import random

# Create your views here.
tmdb_base_url = 'https://api.themoviedb.org/3'
omdb_base_url = 'http://www.omdbapi.com/'


def homepage(request):
    details = {}
    latest_path = '/movie/now_playing'
    popular_path = '/movie/popular'
    top_path = '/movie/top_rated'
    upcoming_path = '/movie/upcoming'
    actors_path = '/person/popular'
    latest_endpoint = f'{tmdb_base_url}{latest_path}?api_key={TMDB_KEY}'
    popular_endpoint = f'{tmdb_base_url}{popular_path}?api_key={TMDB_KEY}'
    top_endpoint = f'{tmdb_base_url}{top_path}?api_key={TMDB_KEY}'
    upcoming_endpoint = f'{tmdb_base_url}{upcoming_path}?api_key={TMDB_KEY}'
    actors_endpoint = f'{tmdb_base_url}{actors_path}?api_key={TMDB_KEY}'
    latest_request = requests.get(latest_endpoint)
    popular_request = requests.get(popular_endpoint)
    top_request = requests.get(top_endpoint)
    upcoming_request = requests.get(upcoming_endpoint)
    actors_request = requests.get(actors_endpoint)
    latest_data = latest_request.json()
    popular_data = popular_request.json()
    top_data = top_request.json()
    upcoming_data = upcoming_request.json()
    actors_data = actors_request.json()
    actors = actors_data['results']
    if request.user.is_authenticated:
        current_user = MyCustomUser.objects.get(id=request.user.id)
        if current_user.watch_list.all():
            watchlist = current_user.watch_list.all()
            details.update({'watchlist': watchlist})
        if current_user.favorites_list.all():
            favorites = current_user.favorites_list.all()
            fave_movie = random.choice(favorites)
            movie_id = fave_movie.tmdb_id
            recommendations_path = f'/movie/{movie_id}/recommendations'
            recommendations_endpoint = f'{tmdb_base_url}{recommendations_path}?api_key={TMDB_KEY}'
            recommendations_request = requests.get(recommendations_endpoint)
            if recommendations_request.status_code in range(200, 299):
                recommendations_data = recommendations_request.json()
                if not recommendations_data['results'] == []:
                    details.update({
                        'fave_movie': fave_movie,
                        'recommendations': recommendations_data})
            details.update({'favorites': favorites})
    details.update({
        'latest': latest_data,
        'popular': popular_data,
        'top': top_data,
        'upcoming': upcoming_data,
        'actors': actors
    })
    return render(request, 'homepage.html', details)


def search_all(request):
    if request.method == 'POST':
        form = AllSearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            search_keyword = data['search_all']
            search_path = f'/search/multi'
            endpoint = f'{tmdb_base_url}{search_path}?api_key={TMDB_KEY}&query={search_keyword}'
            search_request = requests.get(endpoint)
            if search_request.status_code in range(200, 299):
                request_data = search_request.json()
                results = request_data['results']
                return render(
                    request, 'movies/all_results.html', {'results': results})
    form = AllSearchForm()
    return render(request, 'homepage.html', {'form': form})


def search_movie(request):
    if request.method == 'POST':
        form = MovieSearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            movie_name = data['search_movie']
            id_path = '/search/movie'
            endpoint = f'{tmdb_base_url}{id_path}?api_key={TMDB_KEY}&query={movie_name}'
            id_request = requests.get(endpoint)
            if id_request.status_code in range(200, 299):
                request_data = id_request.json()
                results = request_data['results']
                return render(
                    request, 'movies/movie_results.html', {'results': results})
    form = MovieSearchForm()
    return render(request, 'general_form.html', {'form': form})


def movie_detail(request, movie_id):
    details = {}
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
    recommendations_path = f'/movie/{movie_id}/recommendations'
    recommendations_endpoint = f'{tmdb_base_url}{recommendations_path}?api_key={TMDB_KEY}'
    recommendations_request = requests.get(recommendations_endpoint)
    if recommendations_request.status_code in range(200, 299):
        recommendations_data = recommendations_request.json()
        if not recommendations_data['results'] == []:
            details.update({'recommendations': recommendations_data})
    video = {}
    related_videos = []
    if not video_data['results'] == []:
        video = video_data['results'][0]
        details.update({'video': video})
    if len(video_data['results']) > 1:
        related_videos = video_data['results'][1:5]
        details.update({'videos': related_videos})
    rotten_tomatoes = ''
    if omdb_data['Ratings']:
        for rating in omdb_data['Ratings']:
            if rating['Source'] == 'Rotten Tomatoes':
                rotten_tomatoes = rating['Value']
                details.update({'rotten_tomatoes': rotten_tomatoes})
    if request.user.is_authenticated:
        current_user = MyCustomUser.objects.get(id=request.user.id)
        is_favorited = current_user.favorites_list.filter(tmdb_id=movie_id).exists()
        in_watchlist = current_user.watch_list.filter(tmdb_id=movie_id).exists()
        details.update({'is_favorited': is_favorited, 'in_watchlist': in_watchlist})
    details.update({
        'data': movie_data,
        'reviews': reviews_data,
        'omdb': omdb_data,
        'actors': actors,
        'directors': directors,
        'writers': writers
    })
    poster_url = f"https://image.tmdb.org/t/p/w342{movie_data['poster_path']}"
    if not Movie.objects.filter(tmdb_id=movie_id).exists():
        Movie.objects.create(
            tmdb_id=movie_id,
            name=movie_data['title'],
            poster_url=poster_url
        )
    return render(request, 'movies/movie_detail.html', details)
