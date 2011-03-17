from django import forms
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _, ugettext

from judges.models import Judge

class SignupForm(forms.Form):

    email = forms.EmailField(label = _("Email"), required = True, widget = forms.TextInput())
    firstname = forms.CharField(label=_("First Name"), max_length=30, required=True, widget=forms.TextInput())
    lastname = forms.CharField(label=_("Last Name"), max_length=30, required=True, widget=forms.TextInput())
    bio = forms.CharField(label=_("Bio"), max_length=300, required=True, widget=forms.Textarea())

    def save(self, user):
        email = self.cleaned_data["email"]
        firstname = self.cleaned_data["firstname"]
        lastname = self.cleaned_data["lastname"]
        bio = self.cleaned_data["bio"]

        if email:
            new_judge = Judge.active_objects.create_judge(user, bio)
            if not new_judge:
                return None
            if user.email != email:
                user.email = email
                user.save()
            profile = user.get_profile()
            if profile.firstname != firstname or profile.lastname != lastname:
                profile.firstname = firstname
                profile.lastname = lastname
                profile.save()
            self.send_judge_signup_request_email(user, profile, new_judge)
            return new_judge
        return None

    def send_judge_signup_request_email(self, user, profile, judge):
        context = {
            "user": user,
            "profile": profile,
            "bio": judge.bio,
        }
        subject = render_to_string(
            "judges/email_signup_subject.txt", context)
        # remove superfluous line breaks
        subject = "".join(subject.splitlines())
        message = render_to_string(
            "judges/email_signup_message.txt", context)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
                  [settings.CONTACT_EMAIL])
