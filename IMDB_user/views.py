from django.shortcuts import redirect, render
from movies.models import Movie
from reviews.models import Review
import requests
# Create your views here.
base_url = 'https://api.themoviedb.org/3'
api_key = 'ea3f0ae618db2e67cd3f57ba270936c4'

def add_watchlist(request, imbd_id):
    user = request.user
    movie = Movie.objects.get(imbd_id=imbd_id)
    user.watch_list.add(movie)
    return redirect('/')

def profile_view(request):
    watch_list_movies = []
    recomendations = []
    watch_list = request.user.watch_list
    for movie in watch_list.all():
        movie_path = f'/movie/{movie.imbd_id}'
        movie_endpoint = f'{base_url}{movie_path}?api_key={api_key}'
        movie_request = requests.get(movie_endpoint)
        if movie_request.status_code in range(200, 299):
            movie_data = movie_request.json()
            watch_list_movies.append(movie_data)
            movie_id = movie_data['id']
            recomendations_path = f'/movie/{movie_id}/recommendations'
            recomendations_endpoint = f'{base_url}{recomendations_path}?api_key={api_key}'
            recomendations_endpoint_request = requests.get(recomendations_endpoint)
            if recomendations_endpoint_request.status_code in range(200, 299):
                    recomendations_data = recomendations_endpoint_request.json()
                    for recomendations_data in recomendations_data['results']:
                        recomendations.append(recomendations_data)
    reviews = Review.objects.filter(user=request.user)
    return render(request, 'profile.html', {'reviews': reviews, 'watch_list': watch_list_movies, 'recomendations': recomendations, 'test': watch_list_movies[0], 'test2': recomendations[0] or '' })
