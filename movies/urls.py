from django.urls import path

from movies.views import search_movie, movie_detail

urlpatterns = [
    path('<int:movie_id>/', movie_detail, name='movie_detail'),
    path('search/', search_movie, name='search_movie')
]