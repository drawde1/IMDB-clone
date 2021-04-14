from django.shortcuts import render
from reviews.forms import ReviewForm
from reviews.models import Review
from movies.models import Movie
from django.views.generic import View
# Create your views here.


# def reviews(request, imbd_id):
#     form = ReviewForm()
#     if Movie.objects.filter(imbd_id=imbd_id).exists():
#         movie = Movie.objects.get(imbd_id=imbd_id)
#     else:
#         movie = Movie.objects.create(imbd_id=imbd_id)
#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             Review.objects.create(
#                 user=request.user,
#                 movie=movie,
#                 text=data['text']
#             )
#     reviews = Review.objects.filter(movie=movie)
#     return render(request, 'reviews.html', {'reviews': reviews, 'form': form})


class ReviewView(View):
    def get(self, request, tmdb_id):
        form = ReviewForm()
        if Movie.objects.filter(tmdb_id=tmdb_id).exists():
            movie = Movie.objects.get(tmdb_id=tmdb_id)
        reviews = Review.objects.filter(movie=movie)
        return render(
            request, 'reviews.html',
            {'reviews': reviews, 'form': form, 'movie': movie})

    def post(self, request, tmdb_id):
        form = ReviewForm(request.POST)
        if Movie.objects.filter(tmdb_id=tmdb_id).exists():
            movie = Movie.objects.get(tmdb_id=tmdb_id)
        if form.is_valid():
            data = form.cleaned_data
            Review.objects.create(
                user=request.user,
                movie=movie,
                text=data['text']
            )
            request.user.karma_score += 100
            request.user.save()
        reviews = Review.objects.filter(movie=movie)
        return render(
            request, 'reviews.html',
            {'reviews': reviews, 'form': form, 'movie': movie})
