from django.shortcuts import redirect
from reviews.models import Vote, Review
# Create your views here.


def helpful_unhelpful(request, review_id, value):
    if value == 0:
        value = -1
    user = request.user
    review = Review.objects.get(id=review_id)
    vote = Vote.objects.create(
        value=value,
    )
    review.likedby.add(user)
    review.votes.add(vote)
    review.save()
    review.user.karma_score += value*20
    review.user.save()
    return redirect(f'/reviews/{review.movie.tmdb_id}/')
