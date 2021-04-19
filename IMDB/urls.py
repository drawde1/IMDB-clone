"""IMDB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
# from reviews.views import reviews
from movies.views import homepage, search_all
from reviews.views import ReviewView
# from IMDB_user.views import add_watchlist
from user_profile.views import profile_view, followed_view, following_view, follow, unfollow
from IMDB_user.views import add_watchlist, remove_watchlist
from authentication.views import LoginView, logout_view, SignupView
from karma.views import helpful_unhelpful
# from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('', homepage, name='homepage'),
    path('users/', include('IMDB_user.urls')),
    path('movies/', include('movies.urls')),
    path('actors/', include('actors.urls')),
    path('search/all/', search_all, name="search_all"),
    path("logout/", logout_view, name="logout"),
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", SignupView.as_view(), name="signup"),
    path('movies/', include('movies.urls')),
    path('reviews/<str:tmdb_id>/', ReviewView.as_view(), name="post_review"),
    path('admin/', admin.site.urls),
    # path('reviews/<str:tmdb_id>/', login_required(ReviewView.as_view()), name="post_review"),
    path('watchlist/<str:tmdb_id>/', add_watchlist, name="add_watchlist"),
    path("logout/", logout_view, name="logout"),
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", SignupView.as_view(), name="signup"),
    path('followed/<int:user_id>', followed_view, name='users_being_followed'),
    path('following/<int:user_id>', following_view, name='users_following'),
    path('follow/<int:user_id>', follow, name='follow'),
    path('unfollow/<int:user_id>', unfollow, name='unfollow'),
    path(
        'watchlist/remove/<str:tmdb_id>/',
        remove_watchlist,
        name='remove_watchlist'),
    path('profile/<int:user_id>', profile_view, name='profile'),
    path('vote/<str:review_id>/<int:value>/', helpful_unhelpful),
    path('admin/', admin.site.urls)
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
