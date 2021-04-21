from django.shortcuts import redirect
from reviews.models import Vote, Review
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
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
    return redirect(request.META.get(
            'HTTP_REFERER', 'redirect_if_referer_not_found'))
