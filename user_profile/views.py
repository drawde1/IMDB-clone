from django.shortcuts import render
from reviews.models import Review
# from IMDB.settings import TMDB_KEY
from IMDB_user.forms import UserForm
from IMDB_user.models import MyCustomUser
# import requests
from movies.helpers import ApiPaths
# Create your views here.
base_url = 'https://api.themoviedb.org/3'


def profile_view(request, user_id):
    recomendations = []
    user = MyCustomUser.objects.get(id=user_id)
    for movie in user.watch_list.all():
        recomendations_path = f'/movie/{movie.tmdb_id}/recommendations'
        recomendations_data = ApiPaths.grab_data(recomendations_path)
        for recomendations_data in recomendations_data['results']:
            if not user.watch_list.filter(
                    name=recomendations_data['title']):
                recomendations.append(recomendations_data)
    reviews = Review.objects.filter(user=user)
    context = {
            'reviews': reviews,
            'recomendations': recomendations,
            'user': user
            }
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
