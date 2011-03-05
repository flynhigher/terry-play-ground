
from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from account.forms import ProfileForm, RegistrationForm, LoginForm, ChangePasswordForm, ResetPasswordForm

def logout(request):
	auth_logout(request)
	default_redirect_to = '/'
	redirect_to = request.REQUEST.get("next")
	# light security check -- make sure redirect_to isn't garbage.
	if not redirect_to or "://" in redirect_to or " " in redirect_to:
		redirect_to = default_redirect_to
	return HttpResponseRedirect(redirect_to)
	
def profile(request, template_name="profile.html"):
    if request.user.is_authenticated():
        if request.method == "POST":
            if request.POST["action"] == "update":
                profile_form = ProfileForm(request.POST, instance=request.user.get_profile())
                if profile_form.is_valid():
									email = profile_form.cleaned_data["email"]
									firstname = profile_form.cleaned_data["firstname"]
									lastname = profile_form.cleaned_data["lastname"]
									if profile.email != email or profile.firstname != firstname or profile.lastname != lastname:
										profile.email = request.user.email = email
										profile.firstname = request.user.firstname = firstname
										profile.lastname = request.user.lastname = lastname
										request.user.save()
									profile_form.save()
        else:
            profile_form = ProfileForm(instance=request.user.get_profile())
    else:
        profile_form = None

    return render_to_response(template_name, {
        "form": profile_form,
    }, context_instance=RequestContext(request))
profile = login_required(profile)

def login(request, form_class=LoginForm, template_name="login.html"):
    if request.method == "POST":
        default_redirect_to = getattr(settings, "LOGIN_REDIRECT_URLNAME", None)
        if default_redirect_to:
            default_redirect_to = reverse(default_redirect_to)
        else:
            default_redirect_to = settings.LOGIN_REDIRECT_URL
        redirect_to = request.REQUEST.get("next")
        # light security check -- make sure redirect_to isn't garabage.
        if not redirect_to or "://" in redirect_to or " " in redirect_to:
            redirect_to = default_redirect_to
        form = form_class(request.POST)
        if form.login(request):
            return HttpResponseRedirect(redirect_to)
    else:
        form = form_class()
    return render_to_response(template_name, {
        "form": form,
    }, context_instance=RequestContext(request))

def signup(request, form_class=RegistrationForm,
        template_name="content/register.html", success_url=None):
    if success_url is None:
        success_url = reverse("home")
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            username, password = form.save()
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            request.user.message_set.create(message="Successfully logged in as %(username)s." % {'username': user.username})
            return HttpResponseRedirect(success_url)
    else:
        form = form_class()
    return render_to_response(template_name, {
        "form": form,
    }, context_instance=RequestContext(request))

def password_change(request, form_class=ChangePasswordForm,
        template_name="password_change.html"):
    if request.method == "POST":
        password_change_form = form_class(request.user, request.POST)
        if password_change_form.is_valid():
            password_change_form.save()
            password_change_form = form_class(request.user)
    else:
        password_change_form = form_class(request.user)
    return render_to_response(template_name, {
        "form": password_change_form,
    }, context_instance=RequestContext(request))
password_change = login_required(password_change)

def password_reset(request, form_class=ResetPasswordForm,
        template_name="password_reset.html",
        template_name_done="password_reset_done.html"):
    if request.method == "POST":
        password_reset_form = form_class(request.POST)
        if password_reset_form.is_valid():
            email = password_reset_form.save()
            return render_to_response(template_name_done, {
                "email": email,
            }, context_instance=RequestContext(request))
    else:
        password_reset_form = form_class()
    
    return render_to_response(template_name, {
        "form": password_reset_form,
    }, context_instance=RequestContext(request))
