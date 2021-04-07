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
    def get(self, request, imbd_id):
        form = ReviewForm()
        if Movie.objects.filter(imbd_id=imbd_id).exists():
            movie = Movie.objects.get(imbd_id=imbd_id)
        else:
            movie = Movie.objects.create(imbd_id=imbd_id)
        reviews = Review.objects.filter(movie=movie)
        return render(request, 'reviews.html', {'reviews': reviews, 'form': form})
    
    def post(self, request, imbd_id):
        form = ReviewForm(request.POST)
        if Movie.objects.filter(imbd_id=imbd_id).exists():
            movie = Movie.objects.get(imbd_id=imbd_id)
        else:
            movie = Movie.objects.create(imbd_id=imbd_id)
        if form.is_valid():
            data = form.cleaned_data
            Review.objects.create(
                user=request.user,
                movie=movie,
                text=data['text']
            )
        reviews = Review.objects.filter(movie=movie)
        return render(request, 'reviews.html', {'reviews': reviews, 'form': form})