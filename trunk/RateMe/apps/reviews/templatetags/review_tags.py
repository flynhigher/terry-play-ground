from django.conf import settings
from django import template
from reviews.models import Review

register = template.Library()

def show_review(image, user, show_username=False):
    reviews = Review.objects.filter(image=image)
    score_range = range(1, settings.REVIEWS_MAX_SCORE + 1)
    empty_review = Review(score=0, comment="")
    return {"image": image, "reviews": reviews, "empty_review": empty_review,
            "user": user, "score_range": score_range, "show_username": show_username}
register.inclusion_tag("review.html")(show_review)

def show_review_item(image, review, user, score_range, show_username):
    #current user is authenticated
    #and there's no review and owner's judge is current user
    # or there's review and the reviewer is current user and can change already reviewed item
    enabled = user.is_authenticated() \
            and ( (review.user and review.user == user and settings.REVIEWS_CAN_CHANGE_VOTE)\
               or (not review.user and image.member.get_profile().myjudge.user == user))
    return {"image": image, "review": review, "user": user, "score_range": score_range,
            "disabled": not enabled, "enabled": enabled, "show_username": show_username,
            "media_url": settings.MEDIA_URL,}
register.inclusion_tag("review_item.html")(show_review_item)

def show_rate_item(image_id, value, score, disabled):
    checked = value == score
    return {"image_id": image_id, "value": value, "checked": checked, "disabled": disabled}
register.inclusion_tag("rate_item.html")(show_rate_item)

def show_comment_item(image_id, comment, disabled):
    value = comment
    return {"image_id": image_id, "value": value, "disabled": disabled}
register.inclusion_tag("comment_item.html")(show_comment_item)
