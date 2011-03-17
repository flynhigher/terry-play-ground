from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.template.loader import render_to_string

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from judges.models import Judge, Judge

from rateme_profiles.models import Profile
from rateme_profiles.forms import ProfileForm
from pictures.models import Image

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None


def profiles(request, template_name="rateme_profiles/judges.html"):
    users = User.objects.all().order_by("-date_joined")
    search_terms = request.GET.get('search', '')
    order = request.GET.get('order')
    if not order:
        order = 'date'
    if search_terms:
        users = users.filter(username__icontains=search_terms)
    if order == 'date':
        users = users.order_by("-date_joined")
    elif order == 'name':
        users = users.order_by("username")
    return render_to_response(template_name, {
        'users':users,
        'order' : order,
        'search_terms' : search_terms
    }, context_instance=RequestContext(request))


def judges(request, template_name="rateme_profiles/judges.html"):
    users = User.objects.filter(judge__is_active = True).order_by("-date_joined")
    search_terms = request.GET.get('search', '')
    order = request.GET.get('order')
    if not order:
        order = 'date'
    if search_terms:
        users = users.filter(username__icontains=search_terms)
    if order == 'date':
        users = users.order_by("-date_joined")
    elif order == 'name':
        users = users.order_by("username")
    return render_to_response(template_name, {
        'users':users,
        'order' : order,
        'search_terms' : search_terms
    }, context_instance=RequestContext(request))

def profile(request, username, template_name="rateme_profiles/profile.html"):
    
    other_user = get_object_or_404(User, username=username)
    
    if request.user.is_authenticated():
        if request.user == other_user:
            is_me = True
        else:
            is_me = False
    else:
        is_me = False

    photos = Image.objects.filter(member=other_user)

    return render_to_response(template_name, {
        "is_me": is_me,
        "other_user": other_user,
        "photos": photos,
        "myjudge": request.user.get_profile().myjudge if is_me else None,
    }, context_instance=RequestContext(request))


@login_required
def profile_edit(request, form_class=ProfileForm, **kwargs):
    
    template_name = kwargs.get("template_name", "rateme_profiles/profile_edit.html")
    
    if request.is_ajax():
        template_name = kwargs.get(
            "template_name_facebox",
            "rateme_profiles/profile_edit_facebox.html"
        )
    
    profile = request.user.get_profile()
    
    if request.method == "POST":
        prev_judge = profile.myjudge
        profile_form = form_class(request.POST, instance=profile)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)

            profile.user = request.user
            profile.save()
            if not prev_judge or prev_judge.id != profile.myjudge.id:
                __send_email_to_judge(request.user, profile)

            return HttpResponseRedirect(reverse("profile_detail", args=[request.user.username]))
    else:
        profile_form = form_class(instance=profile)
    
    return render_to_response(template_name, {
        "profile": profile,
        "profile_form": profile_form,
    }, context_instance=RequestContext(request))

@login_required
def profile_judge_edit(request):
    if request.is_ajax():
        pass

    profile = request.user.get_profile()

    if request.method == "POST":
        prev_judge = profile.myjudge
        judge_id = request.POST["id_myjudge"]
        if prev_judge and prev_judge.id == judge_id:
            return HttpResponseRedirect(reverse("judge_list"))

        judge = Judge.active_objects.get(id=judge_id)
        if judge:
            profile.myjudge = judge
            profile.save()
            __send_email_to_judge(request.user, profile)
            request.user.message_set.create(message="The judge, " + profile.myjudge.user.get_profile().name + " has been successfully assigned to you")
            return HttpResponseRedirect(reverse("judge_list"))
        else:
            request.user.message_set.create(message="The submitted form is not valid")
            return HttpResponseRedirect(reverse("judge_list"))

    request.user.message_set.create(message="The form is not submitted properly")
    return HttpResponseRedirect(reverse("judge_list"))

def __send_email_to_judge(user, profile):
    myjudge = profile.myjudge
    if not myjudge or not myjudge.user.email:
        return
    current_site = Site.objects.get_current()

    context = {
        "user": user,
        "profile": profile,
        "judge": myjudge,
        "rate_url": reverse("photo_rate"),
        "current_site": current_site,
    }
    subject = render_to_string(
        "emailconfirmation/judge_selected_subject.txt", context)
    # remove superfluous line breaks
    subject = "".join(subject.splitlines())
    message = render_to_string(
        "emailconfirmation/judge_selected_message.txt", context)
    #send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
    #          [email_address.email], priority="high")
    msg = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [myjudge.user.email])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()
