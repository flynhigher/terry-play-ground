import re

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.simple import direct_to_template
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden, Http404

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

import urllib
from forms import ContactForm
from django.conf import settings

def get_ultracart_data(request):
	if request.method == "POST":
		data = dict(request.POST.items())
		return urllib.urlopen(url, urllib.urlencode(data)).read()    	
	else:
		return ''

def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			from datetime import datetime
			name = form.cleaned_data['name']
			email = form.cleaned_data['email']
			phone = form.cleaned_data['phone']
			message = form.cleaned_data['message']
			subject = "Contact Us message from " + form.cleaned_data['name']
			if request.user.is_authenticated():
				form.submitter = request.user
			form.submitteddate = datetime.now()
			contact = form.save()
			message = 'Email: %s\nPhone: %s\n\n' % (email, phone) + message
			recipients = settings.CONTACT_EMAIL.split(';');
			
			from django.core.mail import send_mail
			send_mail(subject, message, settings.CONTACT_EMAIL, recipients)
			return HttpResponseRedirect('/contacttks.html') # Redirect after POST
	else:
		form = ContactForm()
	
	return direct_to_template(request, 'content/contactus.html', { 'form': form, })

def contact_list(request):
	pass