
import re

from django import forms
from django.template.loader import render_to_string
from django.conf import settings

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from account.models import Profile
from account.metaresolver import classmaker

class ProfileForm(forms.ModelForm):
	def clean_email(self):
			"""
			Validate that the supplied email address is unique for the
			site.
			
			"""
			if User.objects.filter(email__iexact=self.cleaned_data['email']):
					raise forms.ValidationError("This email address is already in use. Please supply a different email address.")
			return self.cleaned_data['email']

	class Meta:
	    model = Profile
	    exclude = ('user')
	
attrs_dict = {'class': 'required'}
class RegistrationForm(ProfileForm):
	username = forms.RegexField(regex=r'^[\w\.@-]+$',
                            max_length=30,
                            widget=forms.TextInput(attrs=attrs_dict),
                            label="Username",
                            error_messages={'invalid': "This value must contain only letters, numbers, dashes, periods, and underscores."})
#	email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
#	                                                           maxlength=75)),
#												 label="Email address")
	password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
															label="Password")
	password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
															label="Password (again)")
	
	def clean_username(self):
			"""
			Validate that the username is alphanumeric and is not already
			in use.
			
			"""
			try:
					user = User.objects.get(username__iexact=self.cleaned_data['username'])
			except User.DoesNotExist:
					return self.cleaned_data['username']
			raise forms.ValidationError("A user with that username already exists.")
	
	def clean(self):
			"""
			Verifiy that the values entered into the two password fields
			match. Note that an error here will end up in
			``non_field_errors()`` because it doesn't apply to a single
			field.
			
			"""
			if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
					if self.cleaned_data['password1'] != self.cleaned_data['password2']:
							raise forms.ValidationError("The two password fields didn't match.")
			return self.cleaned_data
	
	def save(self):
			username = self.cleaned_data["username"]
			password = self.cleaned_data["password1"]
			email = self.cleaned_data["email"]
			firstname = self.cleaned_data["firstname"]
			lastname = self.cleaned_data["lastname"]
			new_user = User.objects.create_user(username, email, password)
			new_user.first_name=firstname
			new_user.last_name=lastname
			new_user.save()

			p = Profile.objects.create(
				user = new_user,
				email = email,
				phone = self.cleaned_data["phone"],
				mobilephone = self.cleaned_data["mobilephone"] if 'mobilephone' in self.cleaned_data else None,
				fax = self.cleaned_data["fax"] if 'fax' in self.cleaned_data else None,
				companyname = self.cleaned_data["companyname"] if 'companyname' in self.cleaned_data else None,
				firstname = firstname,
				lastname = lastname,
				middlename = self.cleaned_data["middlename"] if 'middlename' in self.cleaned_data else None,
				address1 = self.cleaned_data["address1"],
				address2 = self.cleaned_data["address2"] if 'address2' in self.cleaned_data else None,
				city = self.cleaned_data["city"],
				state = self.cleaned_data["state"],
				zipcode = self.cleaned_data["zipcode"],
				country = self.cleaned_data["country"])
			
			return username, password # required for authenticate()

class LoginForm(forms.Form):

    username = forms.CharField(label="Username", max_length=30, widget=forms.TextInput())
    password = forms.CharField(label="Password", widget=forms.PasswordInput(render_value=False))

    user = None

    def clean(self):
        if self._errors:
            return
        user = authenticate(username=self.cleaned_data["username"], password=self.cleaned_data["password"])
        if user:
            if user.is_active:
                self.user = user
            else:
                raise forms.ValidationError("This account is currently inactive.")
        else:
            raise forms.ValidationError("The username and/or password you specified are not correct.")
        return self.cleaned_data

    def login(self, request):
        if self.is_valid():
            login(request, self.user)
            request.user.message_set.create(message="Successfully logged in as %(username)s." % {'username': self.user.username})
            return True
        return False

class UserForm(forms.Form):
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(UserForm, self).__init__(*args, **kwargs)

class ChangePasswordForm(UserForm):

    oldpassword = forms.CharField(label="Current Password", widget=forms.PasswordInput(render_value=False))
    password1 = forms.CharField(label="New Password", widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label="New Password (again)", widget=forms.PasswordInput(render_value=False))

    def clean_oldpassword(self):
        if not self.user.check_password(self.cleaned_data.get("oldpassword")):
            raise forms.ValidationError("Please type your current password.")
        return self.cleaned_data["oldpassword"]

    def clean_password2(self):
        if "password1" in self.cleaned_data and "password2" in self.cleaned_data:
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                raise forms.ValidationError("You must type the same password each time.")
        return self.cleaned_data["password2"]

    def save(self):
        self.user.set_password(self.cleaned_data['password1'])
        self.user.save()
        self.user.message_set.create(message="Password successfully changed.")


class ResetPasswordForm(forms.Form):

    email = forms.EmailField(label="Email", required=True, widget=forms.TextInput(attrs={'size':'30'}))

    def clean_email(self):
        if User.objects.filter(email__iexact=self.cleaned_data["email"]).count() == 0:
            raise forms.ValidationError("No user associated with Email address provided")
        return self.cleaned_data["email"]

    def save(self):
        for user in User.objects.filter(email__iexact=self.cleaned_data["email"]):
					new_password = User.objects.make_random_password()
					user.set_password(new_password)
					user.save()
					subject = "Password reset for " + settings.SITE_NAME
					message = render_to_string("password_reset_message.txt", {
					    "user": user,
					    "new_password": new_password,
					})
					from django.core.mail import send_mail
					send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        return self.cleaned_data["email"]
