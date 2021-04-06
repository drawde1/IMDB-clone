from django.shortcuts import render
from reviews.forms import ReviewForm
from reviews.models import Review
# Create your views here.


def reviews(request, movie):
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Review.objects.create(
                user=request.user(),
                movie='movie',
                text=data['text']
            )
    reviews = Review.objects.filter(movie=movie)
    return render(request, 'reviews.html', {'reviews': reviews, 'form': form})
