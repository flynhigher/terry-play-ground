from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect

import urllib
from forms import ContactForm
from django.conf import settings

def contact(request, template_name="about/contactus.html"):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            from datetime import datetime
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['message']
            subject = "Contact Us message from " + name
            if request.user.is_authenticated():
                form.submitter = request.user
            form.submitteddate = datetime.now()
            contact = form.save()
            message = 'Email: %s\nPhone: %s\n\n' % (email, phone) + message
            recipients = settings.CONTACT_EMAIL.split(';')

            from django.core.mail import send_mail
            try:
                send_mail(subject, message, settings.CONTACT_EMAIL, recipients)
            except:
                pass
            request.user.message_set.create(message="Contact Us message has been successfully submitted")
            return HttpResponseRedirect(reverse('contactus')) # Redirect after POST
    else:
        if request.user.is_authenticated():
            profile = request.user.get_profile()
            kwargs = { "email": request.user.email, "name": profile.name, }
            form = ContactForm(initial=kwargs)
        else:
            form = ContactForm()

    return render_to_response(template_name, {
        "form": form,
    }, context_instance=RequestContext(request))
