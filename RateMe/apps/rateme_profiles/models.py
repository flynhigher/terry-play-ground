from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from judges.models import Judge

class Profile(models.Model):

    user = models.ForeignKey(User, unique=True, verbose_name=_('user'))
    firstname = models.CharField(_('firstname'), max_length=30, null=True, blank=True)
    lastname = models.CharField(_('lastname'), max_length=30, null=True, blank=True)
    about = models.TextField(_('about'), null=True, blank=True)
#    location = models.CharField(_('location'), max_length=40, null=True, blank=True)
#    website = models.URLField(_('website'), null=True, blank=True, verify_exists=False)
    myjudge = models.ForeignKey(Judge, null=True, blank=True, related_name=_('myjudge'), limit_choices_to = {'is_active': True})
    
    def __unicode__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return ('profile_detail', None, {'username': self.user.username})
    get_absolute_url = models.permalink(get_absolute_url)

    def _get_full_name(self):
        return u'%s %s' % (self.firstname, self.lastname) if self.firstname else None
    name = property(_get_full_name)
    
    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

def create_profile(sender, instance=None, **kwargs):
    if instance is None:
        return
    profile, created = Profile.objects.get_or_create(user=instance)

post_save.connect(create_profile, sender=User)
