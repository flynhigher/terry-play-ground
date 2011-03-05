from django import forms
from django.template.loader import render_to_string
from django.conf import settings

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from tools.models import Contact

#class ContactForm(forms.Form):
#	name = forms.CharField(max_length=50)
#	email = forms.EmailField(max_length=100)
#	phone = forms.CharField(max_length=20)
#	message = forms.CharField(max_length=1000,widget=forms.Textarea(attrs={'size':'1000'}))


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
