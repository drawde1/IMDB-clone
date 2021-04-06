from django.shortcuts import redirect
from movies.models import Movie

# Create your views here.


def add_watchlist(request, imbd_id):
    user = request.user
    movie = Movie.objects.get(imbd_id=imbd_id)
    user.watch_list.add(movie)
    return redirect('/')


def add_seen(request, imbd_id):
    user = request.user
    movie = user.watch_list.get(id=imbd_id)
    movie.seen = True
    movie.save()
    return redirect('/')
