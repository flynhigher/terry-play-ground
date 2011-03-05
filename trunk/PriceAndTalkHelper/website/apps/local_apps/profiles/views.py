from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden

from profile.models import Profile
from profile.forms import ProfileForm

def profile(request, username, template_name="profiles/profile.html"):
    if request.user.is_authenticated():
        if request.method == "POST":
            if request.POST["action"] == "update":
                profile_form = ProfileForm(request.POST, instance=user.get_profile())
                if profile_form.is_valid():
                    profile = profile_form.save(commit=False)
                    profile.user = user
                    profile.save()
        else:
            profile_form = ProfileForm(instance=user.get_profile())
    else:
        profile_form = None

    return render_to_response(template_name, {
        "profile_form": profile_form,
    }, context_instance=RequestContext(request))
