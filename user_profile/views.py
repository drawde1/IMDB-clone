from django.shortcuts import render, redirect
from reviews.models import Review
from IMDB.settings import TMDB_KEY
from IMDB_user.forms import UserForm
from IMDB_user.models import MyCustomUser
import requests

# Create your views here.
base_url = 'https://api.themoviedb.org/3'


def profile_view(request, user_id):
    watch_list_movies = []
    recomendations = []
    user = MyCustomUser.objects.get(id=user_id)
    following_num = MyCustomUser.objects.filter(followed_list__in=[user]).count
    watch_list = user.watch_list
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
                    if not user.watch_list.filter(
                            name=recomendations_data['title']):
                        recomendations.append(recomendations_data)
    reviews = Review.objects.filter(user=user)
    context = {
            'reviews': reviews,
            'watch_list': watch_list_movies,
            'recomendations': recomendations,
            'user': user,
            'following_num': following_num
            }
    if watch_list_movies:
        context.update({'test': watch_list_movies[0]})
    if recomendations:
        context.update({'test2': recomendations[0]})
    return render(
        request,
        'profile.html',
        context)


def edit_profile(request):
    user = request.user
    form = UserForm(initial={
        'bio': user.bio,
        'displayname': user.displayname,
        'profile_pic': user.profile_pic
    })
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
    if form.is_valid():
        data = form.cleaned_data
        user.displayname = data['displayname']
        user.profile_pic = data['profile_pic']
        user.bio = data['bio']
        user.save()
        return render(
        request,
        'profile.html',
        {"user": user})
    return render(
        request,
        'editprofile.html',
        {'form': form})

def followed_view(request, user_id):
    user = MyCustomUser.objects.get(id=user_id)
    follow_list = user.followed_list.all()
    return render(
        request,
        'followed.html',
        {'user': user, "followed_list": follow_list})

def following_view(request, user_id):
    user = MyCustomUser.objects.get(id=user_id)
    follow_list = MyCustomUser.objects.filter(followed_list__in=[user])
    return render(
        request,
        'followed.html',
        {'user': user, "followed_list": follow_list})


def follow(request, user_id):
    user_followed = MyCustomUser.objects.get(id=user_id)
    user_obj = MyCustomUser.objects.get(id=request.user.id)
    user_obj.followed_list.add(user_followed)
    user_obj.save()
    following_num = MyCustomUser.objects.filter(followed_list__in=[user_obj]).count
    return redirect('profile', user_id=request.user.id)


def unfollow(request, user_id):
    user_unfollowed = MyCustomUser.objects.get(id=user_id)
    user_obj = MyCustomUser.objects.get(id=request.user.id)
    user_obj.followed_list.remove(user_unfollowed)
    user_obj.save()
    following_num = MyCustomUser.objects.filter(followed_list__in=[user_obj]).count
    return redirect('profile', user_id=request.user.id)