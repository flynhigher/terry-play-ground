from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser
from django.db.models.signals import post_save
from django.contrib.localflavor.us.models import USStateField

class Profile(models.Model):
	user = models.ForeignKey(User, unique=True, verbose_name='user')
	email = models.EmailField()
	phone = models.CharField(max_length=50)
	mobilephone = models.CharField(max_length=50, blank=True, null=True)
	fax = models.CharField(max_length=50, blank=True, null=True)
	companyname = models.CharField(max_length=100, blank=True, null=True)
	firstname = models.CharField(max_length=50)
	lastname = models.CharField(max_length=50)
	middlename = models.CharField(max_length=50, blank=True, null=True)
	address1 = models.CharField(max_length=300)
	address2 = models.CharField(max_length=300, blank=True, null=True)
	city = models.CharField(max_length=50)
	state = USStateField()
	zipcode = models.CharField(max_length=15)
	country = models.CharField(max_length=100, blank=True, null=True)
	
	def __unicode__(self):
	    return self.user.username
	
	class Meta:
	    verbose_name = 'profile'
	    verbose_name_plural = 'profiles'

def create_profile(sender, instance=None, **kwargs):
    if instance is None:
        return
    profile, created = Profile.objects.get_or_create(user=instance)

#post_save.connect(create_profile, sender=User)???
