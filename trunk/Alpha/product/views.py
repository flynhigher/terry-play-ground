import re

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden, Http404

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from product.models import *
#from product.admin import *
from product.forms import *
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.mail import send_mail

def products(request):
    products = Product.objects.order_by("category", "name")
    return render_to_response("products.html", {
        "products": products,
    }, context_instance=RequestContext(request))

from django.http import HttpResponseRedirect

def create(request, form_class=ProductForm, template_name="product/create.html"):
    if request.user.is_authenticated() and request.method == "POST":
        if request.POST["action"] == "create":
            product_form = form_class(request.POST)
            if product_form.is_valid():
                product = product_form.save(commit=False)
                product.creator = request.user
                product.save()
                return HttpResponseRedirect(product.get_absolute_url())
        else:
            product_form = form_class()
    else:
        product_form = form_class()
    
    return render_to_response(template_name, {
        "product_form": product_form,
    }, context_instance=RequestContext(request))

def delete(request, slug, redirect_url=None):
    product = get_object_or_404(Product, slug=slug)
    if not redirect_url:
        redirect_url = "/product/" # @@@ can't use reverse("product") -- what is URL name using things?
    
    # @@@ eventually, we'll remove restriction that product.creator can't leave product but we'll still require product.members.all().count() == 1
    if request.user.is_authenticated() and request.method == "POST" and request.user.is_staff:
        product.deleted = True
        product.save()
        request.user.message_set.add(message="Product %s deleted." % product)
        # @@@ no notification as the deleter must be the only member
    
    return HttpResponseRedirect(redirect_url)

def product(request, slug, form_class=ProductUpdateForm,
        template_name="product.html"):
    product = get_object_or_404(Product, slug=slug)
    
    if product.discontinued:
        raise Http404
    
    if request.user.is_authenticated() and request.method == "POST":
        if request.POST["action"] == "update": #and request.user.is_admin():
            product_form = form_class(request.POST, instance=product)
            if product_form.is_valid():
                product = product_form.save()
        else:
            product_form = form_class(instance=product)
    else:
        product_form = form_class(instance=product)
    
    schedules = Schedule.objects.filter(product=product).order_by('-created')
    total_schedules = schedules.count()
    
#    are_member = request.user in product.members.all()
    
    return render_to_response(template_name, {
        "product_form": product_form,
        "product": product,
        "schedules": schedules,
				"total_schedules": total_schedules,
#        "are_member": are_member,
    }, context_instance=RequestContext(request))

def category(request, slug,
					template_name="category.html"):
	pass

def schedule(request, slug, form_class=ScheduleForm,
        template_name="product.html"):
    schedule = get_object_or_404(Schedule, slug=slug)
    from datetime import datetime
#    if schedule.deleted:
#        raise Http404
    
    if request.method == "POST":
      if request.user.is_authenticated():
        schedule_form = form_class(request.POST)
        if schedule_form.is_valid():
          schedule = schedule_form.save(commit=False)
          schedule.price = price
          schedule.creator = request.user
          schedule.save()
          schedule_form = form_class() # @@@ is this the right way to reset it?
      else:
        return HttpResponseForbidden()
    else:
      schedule_form = form_class()
    
    return render_to_response(template_name, {
        "schedule": schedule,
        "schedule_form": schedule_form,
        "buyurl": '/product/signup/' + schedule.buycode,
    }, context_instance=RequestContext(request))

def get_statename_by_key(state_key):
	from django.contrib.localflavor.us.us_states import STATE_CHOICES
	for key, name in STATE_CHOICES:
		if key.lower() == state_key.lower():
			return name
	return None

def schedule_list(request, state, template_name="product.html"):
    return render_to_response(template_name, {
				"statename": get_statename_by_key(state),
        "schedules": Schedule.objects.filter(state__iexact = state).order_by("start"),
				"buyurl": '/product/signup/',
    }, context_instance=RequestContext(request))

def schedule_json(request):
	from datetime import datetime
	from django.core.urlresolvers import reverse
	
	start = int(request.GET.get('start', '0'))
	end = int(request.GET.get('end', '0'))
	start = datetime.fromtimestamp(start)
	end = datetime.fromtimestamp(end)
	res = []
	for s in Schedule.objects.all():#filter(Q(start__gte=start) | Q(start__lte=end)):
		res.append({"id":int(s.buycode),
							"title":s.title if s.title else s.product.name + ', ' + s.city + ', ' + s.state,
							"start":s.start.isoformat(),
							"end":s.end.isoformat(),
							"where":s.venue + ' at ' + s.city + ', ' + s.state,
							"url":reverse('product.views.schedule', kwargs={"slug":s.slug})
							})
	import simplejson as json
	return HttpResponse(json.dumps(res), mimetype='application/json')
	
@login_required
def your_class(request, template_name="your_class.html"):
    return render_to_response(template_name, {
        "schedules": Schedule.objects.filter(deleted=False, members=request.user).order_by("start"),
    }, context_instance=RequestContext(request))

def schedule_post_preview(request, id, template_name="schedule_post_preview.html"):
	schedule = get_object_or_404(Schedule, id=id)
	
	return render_to_response(template_name, {
			"schedule": schedule,
			"schedule_desc_len": 0 if schedule.description == None else len(schedule.description),
	}, context_instance=RequestContext(request))

def product_add(request, form_class=ProductForm, template_name="product_add.html"):
    if request.user.is_authenticated() and request.method == "POST":
        if request.POST["action"] == "create":
            product_form = form_class(request.POST)
            if product_form.is_valid():
                product = product_form.save(commit=False)
                product.creator = request.user
                product.save()
                return HttpResponseRedirect(product.get_absolute_url())
        else:
            product_form = form_class()
    else:
        product_form = form_class()
    
    return render_to_response(template_name, {
        "product_form": product_form,
    }, context_instance=RequestContext(request))

def schedule_add(request, form_class=ScheduleForm, template_name="schedule_add.html"):
    if request.user.is_authenticated() and request.method == "POST":
        if request.POST["action"] == "create":
            schedule_form = form_class(request.POST)
            if schedule_form.is_valid():
                schedule = schedule_form.save(commit=False)
                schedule.creator = request.user
                schedule.save()
#                schedule.members.add(request.user)
#                schedule.save()
                if notification:
                    # @@@ might be worth having a shortcut for sending to all users
                    notification.send(User.objects.all(), "schedule_new_schedule", {"schedule": schedule}, queue=True)
                    if friends: # @@@ might be worth having a shortcut for sending to all friends
                        notification.send((x['friend'] for x in Friendship.objects.friends_for_user(schedule.creator)), "schedule_friend_schedule", {"schedule": schedule})
                #return render_to_response("base.html", {
                #}, context_instance=RequestContext(request))
                return HttpResponseRedirect(schedule.get_absolute_url())
        else:
            schedule_form = form_class()
    else:
        schedule_form = form_class()
    
    return render_to_response(template_name, {
        "schedule_form": schedule_form,
    }, context_instance=RequestContext(request))

def signup(request, form_class=SignupForm,
        template_name="content/signup.html", id=None):
	if not id:
		raise Http404
	if request.method == "POST":
		form = form_class(request.POST)
		if form.is_valid():
			s = form.save(commit = False)
			s.schedulecode = id
			s.save()
			send_mail("Class Signup Notification", str(form.cleaned_data) + ", schedule code: " + str(id), settings.DEFAULT_FROM_EMAIL, ('terry_go@yahoo.com', 'contact@youalpha.com'))
			return HttpResponseRedirect(settings.BUY_URL_FORMAT + str(id))
	else:
		form = form_class()
	return render_to_response(template_name, {"form": form,}, context_instance=RequestContext(request))
