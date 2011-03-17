from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.utils.translation import ugettext_lazy as _
from django.db import IntegrityError

class JudgeManager(models.Manager):
    def create_judge(self, user, bio):
        try:
            return self.create(user=user, bio=bio)
        except IntegrityError:
            return None

    def get_query_set(self):
        return super(JudgeManager, self).get_query_set().filter(is_active=True)

class Judge(models.Model):
    user = models.ForeignKey(User, unique=True, verbose_name=_('user'))
    bio = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
#    objects = JudgeManager()
#    all_objects = models.Manager()
    objects = models.Manager()
    active_objects = JudgeManager()

    def __unicode__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.is_active:
            is_judge = Permission.objects.get(codename="is_judge")
            self.user.user_permissions.add(is_judge)
        elif self.user.has_perm("judges.is_judge"):
            is_judge = Permission.objects.get(codename="is_judge")
            self.user.user_permissions.remove(is_judge)
        super(Judge, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.is_active:
            is_judge = Permission.objects.get(codename="is_judge")
            self.user.user_permissions.remove(is_judge)
        super(Judge, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = _('judge')
        verbose_name_plural = _('judges')
        permissions = ( ("is_judge", "Indicates that the user is a judge"), )
