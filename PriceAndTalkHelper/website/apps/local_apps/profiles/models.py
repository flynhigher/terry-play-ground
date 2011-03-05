from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Profile(models.Model):
	user = models.ForeignKey(User, unique=True, verbose_name=_('user'))
	phone = models.CharField(_('phone'), max_length=50)
	mobilephone = models.CharField(_('mobilephone'), max_length=50, blank=True, null=True)
	fax = models.CharField(_('fax'), max_length=50, blank=True, null=True)
	companyname = models.CharField(_('companyname'), max_length=100, blank=True, null=True)
	firstname = models.CharField(_('firstname'), max_length=50)
	lastname = models.CharField(_('lastname'), max_length=50)
	middlename = models.CharField(_('middlename'), max_length=50, blank=True, null=True)
	address1 = models.CharField(_('address1'), max_length=300)
	address2 = models.CharField(_('address2'), max_length=300, blank=True, null=True)
	city = models.CharField(_('city'), max_length=50)
	state = models.CharField(_('state'), max_length=50)
	zipcode = models.CharField(_('zipcode'), max_length=15)
	country = models.CharField(_('country'), max_length=100)
	
	def __unicode__(self):
	    return self.user.username
	
	def get_absolute_url(self):
	    return ('profile_detail', None, {'username': self.user.username})
	get_absolute_url = models.permalink(get_absolute_url)
	
	class Meta:
	    verbose_name = _('profile')
	    verbose_name_plural = _('profiles')

def create_profile(sender, instance=None, **kwargs):
    if instance is None:
        return
    profile, created = Profile.objects.get_or_create(user=instance)

post_save.connect(create_profile, sender=User)
