from django import template

register = template.Library()

def show_profile(user):
    return {"user": user}
register.inclusion_tag("profile_item.html")(show_profile)

def show_rateme_profile(request, user):
    return {"user": user, "is_me": request.user == user}
register.inclusion_tag("profile_rateme_item.html")(show_rateme_profile)

def clear_search_url(request):
    getvars = request.GET.copy()
    if 'search' in getvars:
        del getvars['search']
    if len(getvars.keys()) > 0:
        return "%s?%s" % (request.path, getvars.urlencode())
    else:
        return request.path
register.simple_tag(clear_search_url)