from django.contrib.sites.models import Site, Site
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, get_host
from django.template import RequestContext
from django.db.models import Q
from django.http import Http404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from photologue.models import *
from pictures.models import Image, Pool
from pictures.forms import PhotoUploadForm, PhotoEditForm


@login_required
def upload(request, form_class=PhotoUploadForm,
        template_name="pictures/upload.html", group_slug=None, bridge=None):
    """
    upload form for photos
    """
    
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None


    photo_form = form_class()
    if request.method == 'POST':
        if request.POST.get("action") == "upload":
            photo_form = form_class(request.user, request.POST, request.FILES)
            if photo_form.is_valid():
                photo = photo_form.save(commit=False)
                photo.member = request.user
                photo.save()
                
                # in group context we create a Pool object for it
                if group:
                    pool = Pool()
                    pool.photo = photo
                    group.associate(pool)
                    pool.save()
                
                request.user.message_set.create(message="Successfully uploaded your picture")
                __send_email_to_judge(request.user, photo)
                include_kwargs = { "username": request.user.username, }
                if group:
                    redirect_to = bridge.reverse("profile_detail", group, kwargs=include_kwargs)
                else:
                    redirect_to = reverse("profile_detail", kwargs=include_kwargs)
                
                return HttpResponseRedirect(redirect_to)

    return render_to_response(template_name, {
        "group": group,
        "photo_form": photo_form,
        "myjudge": request.user.get_profile().myjudge,
    }, context_instance=RequestContext(request))


@login_required
def rate(request, template_name="pictures/rate.html", group_slug=None, bridge=None):
    """
    photos to rate for logged in judge
    """

    photos = Image.objects.filter(member__profile__myjudge__user=request.user, review=None)

    photos = photos.order_by("-date_added")

    return render_to_response(template_name, {
        "photos": photos,
        "show_username": True,
    }, context_instance=RequestContext(request))

@login_required
def yourphotos(request, template_name="pictures/yourphotos.html", group_slug=None, bridge=None):
    """
    photos for the currently authenticated user
    """
    
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None
    
    photos = Image.objects.filter(member=request.user)
    
    if group:
        photos = group.content_objects(photos, join="pool")
    else:
        photos = photos.filter(pool__object_id=None)
    
    photos = photos.order_by("-date_added")
    
    return render_to_response(template_name, {
        "group": group,
        "photos": photos,
    }, context_instance=RequestContext(request))


@login_required
def photos(request, template_name="pictures/latest.html", group_slug=None, bridge=None):
    """
    latest photos
    """
    
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None
    
    photos = Image.objects.filter(
        Q(is_public=True) |
        Q(is_public=False, member=request.user)
    )
    
    if group:
        photos = group.content_objects(photos, join="pool")
    else:
        photos = photos.filter(pool__object_id=None)
    
    photos = photos.order_by("-date_added")
    
    return render_to_response(template_name, {
        "group": group,
        "photos": photos,
    }, context_instance=RequestContext(request))


@login_required
def details(request, id, template_name="pictures/details.html", group_slug=None, bridge=None):
    """
    show the photo details
    """
    
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None
    
    photos = Image.objects.all()
    
    if group:
        photos = group.content_objects(photos, join="pool")
    else:
        photos = photos.filter(pool__object_id=None)
    
    photo = get_object_or_404(photos, id=id)
    
    # @@@: test
    if not photo.is_public and request.user != photo.member:
        raise Http404
    
    photo_url = photo.get_display_url()
    
    title = photo.title
    host = "http://%s" % get_host(request)
    
    if photo.member == request.user:
        is_me = True
    else:
        is_me = False
    
    return render_to_response(template_name, {
        "group": group,
        "host": host,
        "photo": photo,
        "photo_url": photo_url,
        "is_me": is_me,
    }, context_instance=RequestContext(request))


@login_required
def memberphotos(request, username, template_name="pictures/memberphotos.html", group_slug=None, bridge=None):
    """
    Get the members photos and display them
    """
    
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None
    
    user = get_object_or_404(User, username=username)
    
    photos = Image.objects.filter(
        member__username = username,
        is_public = True,
    )
    
    if group:
        photos = group.content_objects(photos, join="pool")
    else:
        photos = photos.filter(pool__object_id=None)
    
    photos = photos.order_by("-date_added")
    
    return render_to_response(template_name, {
        "group": group,
        "photos": photos,
    }, context_instance=RequestContext(request))


@login_required
def edit(request, id, form_class=PhotoEditForm,
        template_name="pictures/edit.html", group_slug=None, bridge=None):
    
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None
    
    photos = Image.objects.all()
    
    if group:
        photos = group.content_objects(photos, join="pool")
    else:
        photos = photos.filter(pool__object_id=None)
    
    photo = get_object_or_404(photos, id=id)
    photo_url = photo.get_display_url()

    if request.method == "POST":
        if photo.member != request.user:
            request.user.message_set.create(message="You can't edit photos that aren't yours")
            
            include_kwargs = {"id": photo.id}
            if group:
                redirect_to = bridge.reverse("photo_details", group, kwargs=include_kwargs)
            else:
                redirect_to = reverse("photo_details", kwargs=include_kwargs)
            
            return HttpResponseRedirect(reverse('photo_details', args=(photo.id,)))
        if request.POST["action"] == "update":
            photo_form = form_class(request.user, request.POST, instance=photo)
            if photo_form.is_valid():
                photoobj = photo_form.save(commit=False)
                photoobj.save()
                
                request.user.message_set.create(message=_("Successfully updated photo '%s'") % photo.title)
                
                include_kwargs = {"id": photo.id}
                if group:
                    redirect_to = bridge.reverse("photo_details", group, kwargs=include_kwargs)
                else:
                    redirect_to = reverse("photo_details", kwargs=include_kwargs)
                
                return HttpResponseRedirect(redirect_to)
        else:
            photo_form = form_class(instance=photo)

    else:
        photo_form = form_class(instance=photo)

    return render_to_response(template_name, {
        "group": group,
        "photo_form": photo_form,
        "photo": photo,
        "photo_url": photo_url,
    }, context_instance=RequestContext(request))

@login_required
def destroy(request, id, group_slug=None, bridge=None):
    
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None
    
    photos = Image.objects.all()
    
    if group:
        photos = group.content_objects(photos, join="pool")
    else:
        photos = photos.filter(pool__object_id=None)
    
    photo = get_object_or_404(photos, id=id)
    title = photo.title
    
    if group:
        redirect_to = bridge.reverse("photos_yours", group)
    else:
        redirect_to = reverse("photos_yours")
    
    if photo.member != request.user:
        request.user.message_set.create(message="You can't delete photos that aren't yours")
        return HttpResponseRedirect(redirect_to)

    if request.method == "POST" and request.POST["action"] == "delete":
        photo.delete()
        request.user.message_set.create(message=_("Successfully deleted photo '%s'") % title)
    
    return HttpResponseRedirect(redirect_to)

def __send_email_to_judge(user, photo):
    profile = user.get_profile()
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
        "emailconfirmation/picture_uploaded_subject.txt", context)
    # remove superfluous line breaks
    subject = "".join(subject.splitlines())
    message = render_to_string(
        "emailconfirmation/picture_uploaded_message.txt", context)
    #send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
    #          [email_address.email], priority="high")
    msg = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [myjudge.user.email])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()