from django.urls import path

from IMDB_user.views import add_favorites

urlpatterns = [
    path('favorites/<int:movie_id>/', add_favorites, name='add_favorites')
]