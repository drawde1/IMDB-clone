from django.urls import path

from movies import views

urlpatterns = [
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('results/', views.index, name='movie_results')
]