import operator
from datetime import datetime

from django.db import models
from django.db.models import signals
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic


from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import USStateField

class Category(models.Model):
    """
    a category is a product category
    """
    
    slug = models.SlugField(_('slug'), max_length=200)
    name = models.CharField(_('name'), max_length=200)
    description = models.TextField(_('description'), null=True, blank=True)
    parents = models.ManyToManyField('self', verbose_name=_('parents'), null=True, blank=True)
    deleted = models.BooleanField(_('deleted'), default=False)
    
    def __unicode__(self):
        return self.name

class Product(models.Model):
    """
    a product 
    """
    
    slug = models.SlugField(_('slug'), max_length=350)
    code = models.CharField(_('code'), max_length=100, blank=True, null=True)
    name = models.CharField(_('name'), max_length=350)
    price = models.DecimalField(_('price'), default=0, decimal_places=2, max_digits=20)
    creator = models.ForeignKey(User, related_name="created_products", verbose_name=_('creator'))
    created = models.DateTimeField(_('created'), default=datetime.now)
    updater = models.ForeignKey(User, related_name="updated_products", verbose_name=_('updater'), blank=True, null=True)
    updated = models.DateTimeField(_('updated'), blank=True, null=True)
    description = models.TextField(_('description'), blank=True, null=True)
    discontinued = models.DateTimeField(_('discontinued'), blank=True, null=True)
    
    categories = models.ManyToManyField(Category, verbose_name=_('categories'))
#    prices = models.ManyToManyField(Price, verbose_name=_('prices'))
    related_products = models.ManyToManyField('self', verbose_name=_('related_products'), blank=True, null=True)
    image_url = models.URLField(_('image_url'), blank=True, null=True)
    
    bought_by = models.ManyToManyField(User, related_name="bought_products", blank=True, null=True)
    interested_by = models.ManyToManyField(User, related_name="interested_products", blank=True, null=True)
        
    def __unicode__(self):
        return self.name

class Schedule(models.Model):
	"""
	a schedule for a product
	"""
	
	slug = models.SlugField(_('slug'), max_length=350)
	buycode = models.CharField(_('buycode'), max_length=45)
	title = models.CharField(_('title'), max_length=500, blank=True, null=True) #auto-filled?
	description = models.TextField(_('description'), blank=True, null=True)
	venue = models.CharField(_('venue'), max_length=100)
	address1 = models.CharField(_('address1'), max_length=300)
	address2 = models.CharField(_('address2'), max_length=300, blank=True, null=True)
	city = models.CharField(_('city'), max_length=50)
	state = models.CharField(_('state'), max_length=50)
	zipcode = models.CharField(_('zipcode'), max_length=15)
	start = models.DateTimeField(_('start'), blank=True, null=True)
	end = models.DateTimeField(_('end'), blank=True, null=True)
	buyurl = models.URLField(_('buyurl'), max_length=200, blank=True, null=True)
	price = models.DecimalField(_('price'), default=0, decimal_places=2, max_digits=20)
	product = models.ForeignKey(Product)
	creator = models.ForeignKey(User, related_name="created_prices", verbose_name=_('creator'))
	created = models.DateTimeField(_('created'), default=datetime.now)
	updater = models.ForeignKey(User, related_name="updated_prices", verbose_name=_('updater'), blank=True, null=True)
	updated = models.DateTimeField(_('updated'), blank=True, null=True)

	def __unicode__(self):
		return self.title

class Signup(models.Model):
	firstname = models.CharField(max_length=50)
	middlename = models.CharField(max_length=50, blank=True, null=True)
	lastname = models.CharField(max_length=50)
	address1 = models.CharField(max_length=300, blank=True, null=True)
	address2 = models.CharField(max_length=300, blank=True, null=True)
	city = models.CharField(max_length=50, blank=True, null=True)
	state = USStateField(blank=True, null=True)
	zipcode = models.CharField(max_length=15, blank=True, null=True)
	country = models.CharField(max_length=100, blank=True, null=True)
	businessname = models.CharField(max_length=100, blank=True, null=True)
	businesstype = models.CharField(max_length=100, blank=True, null=True)
	position = models.CharField(max_length=100, blank=True, null=True)
	numberofstudents = models.IntegerField(blank=True, null=True);
	phone = models.CharField(max_length=50)
	numberofemployees = models.IntegerField(blank=True, null=True);
	email = models.EmailField(blank=True, null=True)
	schedulecode = models.CharField(max_length=20)
	comment = models.TextField(blank=True, null=True)

	def __unicode__(self):
	    return self.lastname + ', ' + self.firstname

	class Meta:
	    verbose_name = 'Signup information'
	    verbose_name_plural = 'Signup information'


# Apply keyword searches.
def construct_search(field_name):
	if field_name.startswith('^'):
			return "%s__istartswith" % field_name[1:]
	elif field_name.startswith('='):
			return "%s__iexact" % field_name[1:]
	elif field_name.startswith('@'):
			return "%s__search" % field_name[1:]
	else:
			return "%s__icontains" % field_name

def get_queryset(initial_queryset, query, search_fields):
	qs = initial_queryset

	if search_fields and query:
		for word in query.split():
				or_queries = [models.Q(**{construct_search(str(field_name)): word}) for field_name in search_fields]
				qs = qs.filter(reduce(operator.or_, or_queries))
		for field_name in search_fields:
				if '__' in field_name:
						qs = qs.distinct()
						break
	return qs
