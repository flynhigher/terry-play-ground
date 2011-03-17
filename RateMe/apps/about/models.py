from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
	"""
	a contact information
	"""

	name = models.CharField(max_length=50)
	email = models.EmailField(max_length=100)
#	phone = models.CharField(max_length=20)
	message = models.TextField(max_length=1000)
	submitter = models.ForeignKey(User, related_name="submitted_contacts", verbose_name='submitter', blank=True, null=True)
	submitteddate = models.DateTimeField(auto_now=True, blank=True, null=True);

	def __unicode__(self):
		return self.name
