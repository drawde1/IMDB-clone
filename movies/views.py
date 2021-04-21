from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from movies.forms import MovieSearchForm, AllSearchForm
from IMDB.settings import TMDB_KEY
from IMDB_user.models import MyCustomUser
from movies.models import Movie
from reviews.models import Review
import random
import requests
from movies.helpers import ApiPaths

# Create your views here.
tmdb_base_url = 'https://api.themoviedb.org/3'
omdb_base_url = 'http://www.omdbapi.com/'


def homepage(request):
    details = {}
    latest_data = ApiPaths.grab_data(ApiPaths.latest_path)
    popular_data = ApiPaths.grab_data(ApiPaths.popular_path)
    top_data = ApiPaths.grab_data(ApiPaths.top_path)
    upcoming_data = ApiPaths.grab_data(ApiPaths.upcoming_path)
    actors_path = f'/person/popular'
    actors_endpoint = f'{tmdb_base_url}{actors_path}?api_key={TMDB_KEY}'
    actors_request = requests.get(actors_endpoint)
    actors_data = actors_request.json()
    actors = actors_data['results']

    details.update({
        'latest': latest_data,
        'popular': popular_data,
        'top': top_data,
        'upcoming': upcoming_data,
        'actors': actors
    })
    
    if request.user.is_authenticated:
        current_user = MyCustomUser.objects.get(id=request.user.id)
        posted_reviews = current_user.custom_user.all()
        reviewed_movies = [ r.movie for r in posted_reviews ]
        details.update({'reviewed_movies': reviewed_movies})
        if current_user.watch_list.all():
            watchlist = current_user.watch_list.all()
            details.update({'watchlist': watchlist})
        if current_user.favorites_list.all():
            favorites = current_user.favorites_list.all()
            fave_movie = random.choice(favorites)
            movie_id = fave_movie.tmdb_id
            recommendations_path = f'/movie/{movie_id}/recommendations'
            recommendations_data = ApiPaths.grab_data(recommendations_path)
            if recommendations_data:
                if not recommendations_data['results'] == []:
                    details.update({
                        'fave_movie': fave_movie,
                        'recommendations': recommendations_data})
            details.update({'favorites': favorites})
    return render(request, 'homepage.html', details)


def search_all(request):
    details = {}
    if request.user.is_authenticated:
        current_user = MyCustomUser.objects.get(id=request.user.id)
        posted_reviews = current_user.custom_user.all()
        reviewed_movies = [ r.movie for r in posted_reviews ]
        details.update({'reviewed_movies': reviewed_movies})
    if request.method == 'POST':
        form = AllSearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            search_keyword = data['search_all']
            request_data = ApiPaths.grab_data(
                ApiPaths.search_path, query=search_keyword)
            if request_data:
                results = request_data['results']
                details.update({'results': results})
                return render(
                    request, 'movies/all_results.html', details)
    form = AllSearchForm()
    details.update({'form': form})
    return render(request, 'homepage.html', details)


def search_movie(request):
    if request.method == 'POST':
        form = MovieSearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            movie_name = data['search_movie']
            request_data = ApiPaths.grab_data(
                ApiPaths.id_path, query=movie_name)
            if request_data:
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

    movie_data = ApiPaths.grab_data(movie_path)
    video_data = ApiPaths.grab_data(video_path)
    reviews_data = ApiPaths.grab_data(reviews_path)

    imdb_id = movie_data['imdb_id']
    omdb_data = ApiPaths.grab_data(imdb_id, omdb=True)
    details.update(ApiPaths.grab_cast(imdb_id))

    recommendations_path = f'/movie/{movie_id}/recommendations'
    recommendations_data = ApiPaths.grab_data(recommendations_path)

    if recommendations_data:
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

    if omdb_data.get('Ratings'):
        for rating in omdb_data['Ratings']:
            if rating['Source'] == 'Rotten Tomatoes':
                rotten_tomatoes = rating['Value']
                details.update({'rotten_tomatoes': rotten_tomatoes})

    if request.user.is_authenticated:
        current_user = MyCustomUser.objects.get(id=request.user.id)
        is_favorited = current_user.favorites_list.filter(
            tmdb_id=movie_id).exists()
        in_watchlist = current_user.watch_list.filter(
            tmdb_id=movie_id).exists()
        details.update(
            {'is_favorited': is_favorited, 'in_watchlist': in_watchlist})
    
    movie = Movie.objects.get(tmdb_id=movie_id)
    if Review.objects.filter(movie=movie).exists():    
        user_reviews = Review.objects.filter(movie=movie)
        details.update({'user_reviews': user_reviews})
    details.update({
        'data': movie_data,
        'reviews': reviews_data,
        'omdb': omdb_data,
    })
    if omdb_data.get('Ratings'):
        rotten_tomatoes = omdb_data['Ratings'][0]
    if video_data['results']:
        video = video_data['results'][0]
    poster_url = f"https://image.tmdb.org/t/p/w342{movie_data['poster_path']}"
    if not Movie.objects.filter(tmdb_id=movie_id).exists():
        Movie.objects.create(
            tmdb_id=movie_id,
            name=movie_data['title'],
            poster_url=poster_url
        )
    return render(request, 'movies/movie_detail.html', details)
