from django.shortcuts import render, redirect
from reviews.models import Review
# from IMDB.settings import TMDB_KEY
from IMDB_user.forms import ProfilePicForm, DisplaynameForm, BioForm
from django.views.generic import View
from IMDB_user.models import MyCustomUser

from movies.helpers import ApiPaths
from django.contrib.auth.decorators import login_required

# Create your views here.
base_url = 'https://api.themoviedb.org/3'


@login_required
def profile_view(request, user_id):
    recomendations = []
    user = MyCustomUser.objects.get(id=user_id)
    can_edit = False
    if request.user == user:
        can_edit = True
    pic_form = ProfilePicForm(
            initial={'profile_pic': user.profile_pic},)
    displayname_form = DisplaynameForm()
    bio_form = BioForm(
        initial={'bio': user.bio})

    if request.method == 'POST':
        if 'save_bio' in request.POST:
            bio_form = BioForm(request.POST)
            if bio_form.is_valid():
                data = bio_form.cleaned_data
                user.bio = data['bio']
                user.save()
        if 'save_displayname' in request.POST:
            displayname_form = DisplaynameForm(
                request.POST)
            if displayname_form.is_valid():
                data = displayname_form.cleaned_data
                user.displayname = data['displayname']
                user.save()
        if 'save_profile_pic' in request.POST:
            pic_form = ProfilePicForm(
                request.POST, request.FILES)
            if pic_form.is_valid():
                data = pic_form.cleaned_data
                user.profile_pic = data['profile_pic']
                user.save()
        return redirect(f'/profile/{user.id}#about')

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
            'user': user,
            'can_edit': can_edit,
            'bio_form': bio_form,
            'pic_form': pic_form,
            'displayname_form': displayname_form,

            }
    return render(
        request,
        'profile.html',
        context)


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
