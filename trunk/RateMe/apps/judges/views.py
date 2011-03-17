from django.core.urlresolvers import reverse
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, Http404

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from rateme_profiles.models import Profile
from rateme_profiles.forms import ProfileForm
from judges.models import Judge
from judges.forms import SignupForm
from pictures.models import Image

def judges(request, template_name="judges/judges.html"):
    judges = Judge.active_objects.all()
    myjudge = request.user.get_profile().myjudge if request.user.is_authenticated() else None

    return render_to_response(template_name, {
        'judges': judges,
        'myjudge': myjudge,
    }, context_instance=RequestContext(request))

def bio(request, username, template_name="judges/bio.html"):
    try:
        judge = Judge.active_objects.get(user__username=username)
    except Judge.DoesNotExist:
        raise Http404

    return render_to_response(template_name, {
        "judge": judge,
    }, context_instance=RequestContext(request))

@login_required()
def signup(request, form_class=SignupForm, template_name="judges/signup.html"):
    try:
        judge = Judge.objects.get(user=request.user)
    except Judge.DoesNotExist:
        judge = None

    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            judge = form.save(request.user)
            request.user.message_set.create(message="Successfully submitted the judge sign up form")
            return HttpResponseRedirect(reverse("judge_list"))
    else:
        profile = request.user.get_profile()
        kwargs = { "email": request.user.email, "firstname": profile.firstname, "lastname": profile.lastname, }
        form = form_class(initial=kwargs)

    return render_to_response(template_name, {
        'judge': judge,
        'form': form,
    }, context_instance=RequestContext(request))
