import operator
from datetime import datetime
from traceback import format_exc

from django.template.defaultfilters import slugify

from django.db import models
from django.db.models import signals
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic

from django.contrib.auth.models import User

from tagging.fields import TagField
import slugtool
from logger import *

try:
    from notification import models as notification
except ImportError:
    notification = None

from wiki.views import get_articles_for_object

class Category(models.Model):
    """
    a category is a product category
    """
    
    slug = models.SlugField(_('slug'), max_length=200)
    name = models.CharField(_('name'), max_length=200)
    amazon_id = models.CharField(max_length=20)
    creator = models.ForeignKey(User, related_name="created_categories", verbose_name=_('creator'))
    created = models.DateTimeField(_('created'), default=datetime.now)
    updater = models.ForeignKey(User, related_name="updated_categories", verbose_name=_('updater'), null=True, blank=True)
    updated = models.DateTimeField(_('updated'), null=True, blank=True)
    description = models.TextField(_('description'), null=True, blank=True)
    parents = models.ManyToManyField('self', verbose_name=_('parents'), null=True, blank=True)
    
    deleted = models.BooleanField(_('deleted'), default=False)
    
    def __unicode__(self):
        return self.name

class Company(models.Model):
		"""
		a company that either manufactures or sells products
		"""

		slug = models.SlugField(_('slug'), max_length=200)
		name = models.CharField(_('name'), max_length=200)
		address = models.CharField(_('address'), max_length=200, blank=True, null=True)
		city = models.CharField(_('city'), max_length=100, blank=True, null=True)
		state = models.CharField(_('state_province'), max_length=50, blank=True, null=True)
		zipcode = models.CharField(_('zipcode'), max_length=20, blank=True, null=True)
		country = models.CharField(_('country'), max_length=50, blank=True, null=True)
		website = models.URLField(_('website'), max_length=200, blank=True, null=True)
		creator = models.ForeignKey(User, related_name="created_companies", verbose_name=_('creator'))
		created = models.DateTimeField(_('created'), default=datetime.now)
		updater = models.ForeignKey(User, related_name="updated_companies", verbose_name=_('updater'), blank=True, null=True)
		updated = models.DateTimeField(_('updated'), blank=True, null=True)
		tax_states = models.CharField(_('tax_states'), max_length=400, blank=True, null=True) #Comma separated states
		tax_rate = models.FloatField(_('tax_rate'), default=0, blank=True, null=True)
		description = models.TextField(_('description'), blank=True, null=True)
		
#		categories = models.ManyToManyField('self', verbose_name=_('categories'))
		
		def __unicode__(self):
				return self.name
		
		# @@@ this might be better as a filter provided by wikiapp
		def wiki_articles(self):
				return get_articles_for_object(self)

class Product(models.Model):
    """
    a product 
    """
    
    slug = models.SlugField(_('slug'), max_length=350)
    name = models.CharField(_('name'), max_length=350)
    upc = models.CharField(_('upc'), max_length=20, db_index=True, null=True)
    part_number = models.CharField(_('mfg_part_no'), max_length=100, blank=True, null=True)
    model = models.CharField(_('model'), max_length=100, blank=True, null=True)
    msrp = models.DecimalField(_('msrp'), default=0, decimal_places=2, max_digits=20)
    manufacturer = models.ForeignKey(Company, related_name="manufactured_products", verbose_name=_('manufacturer'))
    creator = models.ForeignKey(User, related_name="created_products", verbose_name=_('creator'))
    created = models.DateTimeField(_('created'), default=datetime.now)
    updater = models.ForeignKey(User, related_name="updated_products", verbose_name=_('updater'), blank=True, null=True)
    updated = models.DateTimeField(_('updated'), blank=True, null=True)
    description = models.TextField(_('description'), blank=True, null=True)
    discontinued = models.DateTimeField(_('discontinued'), blank=True, null=True)
    
    categories = models.ManyToManyField(Category, verbose_name=_('categories'))
#    prices = models.ManyToManyField(Price, verbose_name=_('prices'))
    related_products = models.ManyToManyField('self', verbose_name=_('related_products'), blank=True, null=True)
    
    amazon_sales_rank = models.IntegerField(_('amazon_sales_rank'), blank=True, default=4022947)
    swatch_image_url = models.URLField(_('swatch_image_url'), blank=True, null=True)
    small_image_url = models.URLField(_('small_image_url'), blank=True, null=True)
    medium_image_url = models.URLField(_('medium_image_url'), blank=True, null=True)
    large_image_url = models.URLField(_('large_image_url'), blank=True, null=True)
    amazon_review_rating = models.FloatField(_('amazon_review_rating'), blank=True, null=True)
    amazon_total_reviews = models.IntegerField(_('amazon_total_reviews'), blank=True, null=True)

    owned_by = models.ManyToManyField(User, related_name="owned_products", blank=True, null=True)
    interested_by = models.ManyToManyField(User, related_name="interested_products", blank=True, null=True)
    other_id = models.CharField(_('other_id'), max_length=45, blank=True, null=True)
        
    def __unicode__(self):
        return self.name
		
		# @@@ this might be better as a filter provided by wikiapp
    def wiki_articles(self):
				return get_articles_for_object(self)

class Price(models.Model):
	"""
	a (list) price for a product at a retailer
	"""

	DEAL_TYPES = (
		('coupon', 'coupon'),
		('rebate', 'rebate'),
		('cashback', 'cashback'),
		('discount', 'discount'),
		('refurbished', 'refurbished'),
		('store credit', 'store credit'),
		('black friday', 'black friday')
	)
	
	list_price = models.DecimalField(_('list_price'), default=0, decimal_places=2, max_digits=20, blank=True, null=True)
	price = models.DecimalField(_('price'), default=0, decimal_places=2, max_digits=20)
	creator = models.ForeignKey(User, related_name="created_prices", verbose_name=_('creator'))
	created = models.DateTimeField(_('created'), default=datetime.now)
	updater = models.ForeignKey(User, related_name="updated_prices", verbose_name=_('updater'), blank=True, null=True)
	updated = models.DateTimeField(_('updated'), default=datetime.now)
	product = models.ForeignKey(Product)
	retailer = models.ForeignKey(Company)
	product_code = models.CharField(_('product_code'), max_length=100)
	shipping = models.DecimalField(_('shipping'), decimal_places=2, max_digits=20, blank=True, null=True)
	source_url = models.URLField(_('source_url'), max_length=200, blank=True, null=True)
	cleaned_url = models.URLField(_('cleaned_url'), max_length=200, blank=True, null=True)
	title = models.CharField(_('title'), max_length=500) #auto-filled?
	description = models.TextField(_('description'), blank=True, null=True)
	started = models.DateTimeField(_('started'), blank=True, null=True)
	expiring = models.DateTimeField(_('expiring'), blank=True, null=True)
	expired = models.BooleanField(_('expired'), default=False)
	deal_type = models.CharField(_('deal_type'), max_length=50, choices=DEAL_TYPES, null=True)

	def __unicode__(self):
		return self.title

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

def get_or_create_product2(dic, user):
    p = None
    p_created = False
    try:
        if 'manufacturer' in dic.keys():
            manufacturer_i, created = Company.objects.get_or_create(name=dic['manufacturer'][:199], defaults={'slug':slugify(dic['manufacturer'][:199]), 'creator':user})

        try:
            p = Product.objects.get(other_id=dic['product_id'])
            p = Product(id=p.id, created=p.created, creator=p.creator, name=dic['name'], \
                manufacturer=manufacturer_i, description=dic['description'], updater=user, updated=datetime.now(), \
                swatch_image_url=dic['image'], \
                small_image_url=dic['image'], medium_image_url=dic['image'], large_image_url=dic['image'], \
                amazon_review_rating=float(dic['review']), amazon_total_reviews=int(dic['review2']), part_number=dic['part_number'])
            slugtool.unique_slugify(p, p.name[:349])
            p.save()
        except Product.DoesNotExist:
            try:
                rank = int(dic['sales_rank']) if 'sales_rank' in dic.keys() and dic['sales_rank'] else 0
            except:
                rank = 0
            try:
                review = float(dic['review']) if 'review' in dic.keys() and dic['review'] else None
            except:
                review = None
            try:
                review2 = int(dic['review2']) if 'review2' in dic.keys() and dic['review2'] else None
            except:
                review2 = None
            upc = dic['upc'] if 'upc' in dic.keys() else None
            p = Product(name=dic['name'], upc=upc, model=dic['part_number'], \
                manufacturer=manufacturer_i, description=dic['description'], creator=user, amazon_sales_rank=rank, \
                swatch_image_url=dic['image'], small_image_url=dic['image'], medium_image_url=dic['image'], large_image_url=dic['image'], \
                amazon_review_rating=review, amazon_total_reviews=review2, part_number=dic['part_number'], other_id=dic['product_id'])
            slugtool.unique_slugify(p, dic['name'][:349])
            p.save()
            #if category:
            #	p.categories.add(category)
            #	p.save()
            p_created = True
            write_trace( p.name.encode('ascii', 'ignore') + ' created')
#amazon        pr_a, pr_a_created = create_retailer_price(p, dic, user)
        pr, pr_created = create_retailer_price(p, dic, user)
    except:
#		raise
        key_value = ''
        for key in dic.keys():
            key_value += key + ':' + dic[key] + ','
        write_error("Exception while getting a product, %s\n\n%s" % (format_exc().encode('ascii', 'ignore'), key_value))
    return (p, p_created, pr, pr_created, None, None)

def create_retailer_price(product, dic, creator):
    m, created = Company.objects.get_or_create(name=dic['site'], defaults={'slug':slugify(dic['site']), 'creator':creator})
    price = dic['price2'] if 'price2' in dic.keys() else dic['price']
    shipping = 0 if dic['shipping'].lower().find('free') >= 0 else float(dic['shipping'])
    general_url = dic['product_url_format'] % dic
    #url = general_url + '?m='  + p_info.merchantId
    url = general_url
    price_i = None
    try:
        price_i, created = Price.objects.get_or_create(product=product, price=price, shipping=shipping, retailer=m,
            defaults={'list_price':None, 'source_url':general_url, 'cleaned_url':url, 'creator':creator, 'product_code':dic['product_id']})
    except MultipleObjectsReturned:
        pass
    if created:
        write_trace(product.name.encode('ascii', 'ignore') + ' $' + price + ' created')
    else:
        last_p = None
        try:
            last_p = Price.objects.filter(product=product, retailer=m).order_by('-updated')[0]
        except:
            pass
        if last_p and price_i and price_i.price != last_p.price:
            price_i = Price.objects.create(product=product, price=price, shipping=shipping, retailer=m,	list_price=0,
                                           source_url=general_url, cleaned_url=url, creator=creator, product_code=dic['product_id'])
            write_trace(product.name.encode('ascii', 'ignore') + ' $' + price + ' created (changed)')
            created = True
        elif price_i:
            price_i.updated = datetime.now()
            price_i.updater = user
            price_i.save()
            write_trace(product.name.encode('ascii', 'ignore') + ' $' + price + ' updated')
        else:
            write_trace(product.name.encode('ascii', 'ignore') + ' $' + price + ' could not be created')

    return price_i, created
