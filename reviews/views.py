from django.shortcuts import render, redirect
from IMDB.settings import TMDB_KEY
from reviews.forms import ReviewForm
from reviews.models import Review
from movies.models import Movie
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import requests

tmdb_base_url = 'https://api.themoviedb.org/3'

class ReviewView(LoginRequiredMixin, View):
    def get(self, request, tmdb_id):
        form = ReviewForm()
        if Movie.objects.filter(tmdb_id=tmdb_id).exists():
            movie = Movie.objects.get(tmdb_id=tmdb_id)
        reviews_by_time = Review.objects.filter(
            movie=movie).order_by('-creation_time')
        reviews_by_votes = sorted(Review.objects.filter(
            movie=movie), key=lambda review: review.vote_total)
        return render(
            request,
            'reviews.html',
            {
                'reviews_by_time': reviews_by_time,
                'reviews_by_votes': reviews_by_votes,
                'form': form,
                'movie': movie})

    def post(self, request, tmdb_id):
        form = ReviewForm(request.POST)
        if Movie.objects.filter(tmdb_id=tmdb_id).exists():
            movie = Movie.objects.get(tmdb_id=tmdb_id)
        if form.is_valid():
            data = form.cleaned_data
            review = Review.objects.create(
                user=request.user,
                movie=movie,
                text=data['text']
            )
            request.user.karma_score += 100
            request.user.save()
            return redirect(f'/reviews/{tmdb_id}/#{review.id}')
        reviews = Review.objects.filter(movie=movie).order_by('creation_time')
        # reviews = reviews.reverse()
        return render(
            request, 'reviews.html',
            {'reviews': reviews, 'form': form, 'movie': movie})

@login_required
def user_reviews(request, tmdb_id):
    movie_api_path = f'/movie/{tmdb_id}'
    movie_api_endpoint = f'{tmdb_base_url}{movie_api_path}?api_key={TMDB_KEY}'
    movie_api_request = requests.get(movie_api_endpoint)
    movie_api_data = movie_api_request.json()
    movie = Movie.objects.get(tmdb_id=tmdb_id)
    reviews_by_time = Review.objects.filter(movie=movie).order_by('creation_time')
    reviews_by_votes = sorted(Review.objects.filter(
            movie=movie), key=lambda review: review.vote_total)
    return render(request, 'user_reviews.html', {
        'reviews_by_time': reviews_by_time,
        'reviews_by_votes': reviews_by_votes,
        'movie': movie,
        'movie_api': movie_api_data
    })