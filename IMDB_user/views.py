from django.shortcuts import redirect
from movies.models import Movie
from django.contrib.auth.decorators import login_required
import requests

from IMDB_user.models import MyCustomUser



# Create your views here.
tmdb_base_url = 'https://api.themoviedb.org/3'
tmdb_key = 'ea3f0ae618db2e67cd3f57ba270936c4'
omdb_base_url = 'http://www.omdbapi.com/'
omdb_key = 'd361bf3'

# Create your views here.
base_url = 'https://api.themoviedb.org/3'
api_key = 'ea3f0ae618db2e67cd3f57ba270936c4'


@login_required
def add_watchlist(request, tmdb_id):
    if Movie.objects.filter(tmdb_id=tmdb_id).exists():
        movie = Movie.objects.get(tmdb_id=tmdb_id)
        current_user = MyCustomUser.objects.get(id=request.user.id)
        if not current_user.watch_list.filter(tmdb_id=tmdb_id).exists():
            current_user.watch_list.add(movie)
            current_user.save()
        return redirect(request.META.get(
            'HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        movie_path = f'/movie/{tmdb_id}'
        movie_endpoint = f'{tmdb_base_url}{movie_path}?api_key={tmdb_key}'
        movie_request = requests.get(movie_endpoint)
        movie_data = movie_request.json()
        poster = movie_data['poster_path']
        movie = Movie.objects.create(
            tmdb_id=movie_data['id'],
            name=movie_data['title'],
            poster_url=f'https://image.tmdb.org/t/p/w342{poster}'
        )
        current_user = MyCustomUser.objects.get(id=request.user.id)
        current_user.watch_list.add(movie)
        current_user.save()
        return redirect(request.META.get(
            'HTTP_REFERER', 'redirect_if_referer_not_found'))


def remove_watchlist(request, tmdb_id):
    current_user = MyCustomUser.objects.get(id=request.user.id)
    movie = Movie.objects.get(tmdb_id=tmdb_id)
    current_user.watch_list.remove(movie)
    current_user.save()
    return redirect(
        request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@login_required
def add_favorites(request, movie_id):
    if Movie.objects.filter(tmdb_id=movie_id).exists():
        movie = Movie.objects.get(tmdb_id=movie_id)
        current_user = MyCustomUser.objects.get(id=request.user.id)
        if not current_user.favorites_list.filter(tmdb_id=movie_id).exists():
            current_user.favorites_list.add(movie)
            current_user.save()
        return redirect(request.META.get(
            'HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        movie_path = f'/movie/{movie_id}'
        movie_endpoint = f'{tmdb_base_url}{movie_path}?api_key={tmdb_key}'
        movie_request = requests.get(movie_endpoint)
        movie_data = movie_request.json()
        poster = movie_data['poster_path']
        movie = Movie.objects.create(
            tmdb_id=movie_data['id'],
            name=movie_data['title'],
            poster_url=f'https://image.tmdb.org/t/p/w342{poster}'
        )
        current_user = MyCustomUser.objects.get(id=request.user.id)
        current_user.favorites_list.add(movie)
        current_user.save()
        return redirect(request.META.get(
            'HTTP_REFERER', 'redirect_if_referer_not_found'))


@login_required
def remove_favorites(request, movie_id):
    current_user = MyCustomUser.objects.get(id=request.user.id)
    movie = Movie.objects.get(tmdb_id=movie_id)
    current_user.favorites_list.remove(movie)
    current_user.save()
    return redirect(request.META.get(
        'HTTP_REFERER', 'redirect_if_referer_not_found'))
