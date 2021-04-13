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
from django.urls import path, include
from reviews.views import reviews
from movies.views import homepage, search_all
# from IMDB_user.views import add_watchlist
from authentication.views import LoginView, logout_view, SignupView
urlpatterns = [
    path('', homepage, name='homepage'),
    path('users/', include('IMDB_user.urls')),
    path('movies/', include('movies.urls')),
    path('actors/', include('actors.urls')),
    path('search/all/', search_all, name="search_all"),
    path('reviews/<str:imbd_id>/', reviews),
    # path('watchlist/<str:imbd_id>/', add_watchlist),
    path("logout/", logout_view, name="logout"),
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", SignupView.as_view(), name="signup"),
    path('admin/', admin.site.urls),
]
