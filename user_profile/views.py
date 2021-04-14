from django.shortcuts import render
from reviews.models import Review
from IMDB.settings import TMDB_KEY
from IMDB_user.forms import UserForm
import requests
# Create your views here.
base_url = 'https://api.themoviedb.org/3'


def profile_view(request):
    watch_list_movies = []
    recomendations = []
    watch_list = request.user.watch_list
    for movie in watch_list.all():
        movie_path = f'/movie/{movie.tmdb_id}'
        movie_endpoint = f'{base_url}{movie_path}?api_key={TMDB_KEY}'
        movie_request = requests.get(movie_endpoint)
        if movie_request.status_code in range(200, 299):
            movie_data = movie_request.json()
            watch_list_movies.append(movie_data)
            movie_id = movie_data['id']
            recomendations_path = f'/movie/{movie_id}/recommendations'
            recomendations_endpoint = f'{base_url}{recomendations_path}?api_key={TMDB_KEY}'
            recomendations_endpoint_request = requests.get(
                recomendations_endpoint)
            if recomendations_endpoint_request.status_code in range(200, 299):
                recomendations_data = recomendations_endpoint_request.json()
                for recomendations_data in recomendations_data['results']:
                    if not request.user.watch_list.filter(
                            name=recomendations_data['title']):
                        recomendations.append(recomendations_data)
    reviews = Review.objects.filter(user=request.user)
    context = {
            'reviews': reviews,
            'watch_list': watch_list_movies,
            'recomendations': recomendations}
    if watch_list_movies:
        context.update({'test': watch_list_movies[0]})
    if recomendations:
        context.update({'test2': recomendations[0]})
    return render(
        request,
        'profile.html',
        context)


def edit_profile(request):
    form = UserForm()
    user = request.user
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
    if form.is_valid():
        data = form.cleaned_data
        user.displayname = data['displayname']
        user.profile_pic = data['profile_pic']
        user.bio = data['bio']
        user.save()
    return render(request,'editprofile.html', {'form': form})