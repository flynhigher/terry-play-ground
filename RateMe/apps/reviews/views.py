from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseRedirect

from exceptions import *
from pictures.models import Image
from reviews.models import Review
from django.conf import settings

@login_required
def do_review(request, image_id):
    try:
        image = Image.objects.get(id=image_id)
    except Image.DoesNotExist:
        raise Http404('Invalid `image_id`.')
    user = request.user
    score = request.REQUEST["score_" + image_id]
    comment = request.REQUEST["comment_" + image_id]

    context = get_context()
    context['instance'] = image
    context.update({
        'score': score,
        'comment': comment,
    })

    had_voted = bool(Review.objects.filter(image=image, user=user))

    try:
        __validate_and_save(user, image, score, comment)
    except InvalidRating:
        request.user.message_set.create(message="Invalid review.")
        return invalid_rating_response(context)
    except CannotChangeReview:
        request.user.message_set.create(message="You cannot change your review.")
#    if had_voted:
#        request.user.message_set.create(message="You successfully changed the review.")
#    else:
#        request.user.message_set.create(message="You successfully changed the review.")

    return HttpResponseRedirect(reverse("photo_rate"))

def __validate_and_save(user, image, score, comment):
    try:
        score = int(score)
    except (ValueError, TypeError):
        raise InvalidRating("%s is not a valid choice for %s" % score)

    if score < 1 or score > settings.REVIEWS_MAX_SCORE:
        raise InvalidRating("%s is not a valid value for score" % score)

    review, created = Review.objects.get_or_create(
        image=image, user=user, defaults={'score': 0})

    if not created and not settings.REVIEWS_CAN_CHANGE_VOTE:
       raise CannotChangeReview()

    review.score = score
    review.comment = comment
    review.save()

def get_context(context={}):
    return context

def render_to_response(template, context):
    raise NotImplementedError

def rating_changed_response(context):
    response = HttpResponse('Review changed.')
    return response

def rating_added_response(context):
    response = HttpResponse('Review recorded.')
    return response

def authentication_required_response(context):
    response = HttpResponse('You must be logged in to vote.')
    response.status_code = 403
    return response

def cannot_change_vote_response(context):
    response = HttpResponse('You have already voted.')
    response.status_code = 403
    return response

def invalid_field_response(context):
    response = HttpResponse('Invalid field name.')
    response.status_code = 403
    return response

def invalid_rating_response(context):
    response = HttpResponse('Invalid rating value.')
    response.status_code = 403
    return response
