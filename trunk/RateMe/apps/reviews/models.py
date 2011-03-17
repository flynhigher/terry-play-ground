from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User

import datetime
from pictures.models import Image

class Review(models.Model):
    image           = models.ForeignKey(Image)
    score           = models.IntegerField(default=0)
    comment         = models.TextField()
    user            = models.ForeignKey(User, blank=True, null=True, related_name="votes")
    date_added      = models.DateTimeField(default=datetime.datetime.now, editable=False)
    date_changed    = models.DateTimeField(default=datetime.datetime.now, editable=False)

    def save(self, *args, **kwargs):
        self.date_changed = datetime.datetime.now()
        super(Review, self).save()
