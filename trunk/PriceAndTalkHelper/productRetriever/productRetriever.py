# coding: utf-8
import sys
import re
from os.path import abspath, dirname, join
#from site import addsitedir

trace = True

def write_trace(log):
    if trace:
        print log
#
#APP_ROOT = abspath(join(dirname(__file__), "../"))
#WEBSITE_ROOT = abspath(dirname(__file__))
#
#path = addsitedir(join(APP_ROOT, "libs/external_libs"), set())
#if path:
#    sys.path = list(path) + sys.path
#sys.path.insert(0, join(APP_ROOT, "apps/external_apps"))
#sys.path.insert(0, join(APP_ROOT, "apps/local_apps"))
#
#from django.contrib.auth.models import User
#from django.template.defaultfilters import slugify

#try:
#    import settings # Assumed to be in the same directory.
#except ImportError:
#    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
#    sys.exit(1)

#from product.models import *

from ecs import *
#from site import addsitedir

#from django.core.management import execute_manager

def GetOrCreateCart(item):
	global cart
	if not cart:
		cart = CartCreate([item,], [1,])
	else:
		cart = CartGet(cart)
		CartClear(cart)
		cart = CartAdd(cart, [item,], [1,])

def GetPriceFromCart(p_info):
	GetOrCreateCart(p_info)
	return GetDecimal(cart.SubTotal.Amount)

def GetDecimal(amount):
    return amount[:-2] + '.' + amount[-2:]

def GetPrice(p_info):
	return GetPriceFromCart(p_info) if p_info.formatted_price == 'Too low to display' else GetDecimal(p_info.price_amount)

from string import *

#def add_browse_node_children(category, browse_node_id):
#	write_trace("* Browse Node: " + category.name + "|" + browse_node_id)
#	if find(lower(category.name), 'accessories') >= 0:
#		write_trace('accessories skip')
#		return
#	elif browse_node_id == '319574011':
#		write_trace('Marine Electronics skip')
#		return
#	elif browse_node_id == '16285901':
#		write_trace('Service & Replacement Plans')
#		return
#	node = BrowseNodeLookup(browse_node_id)
#	for item in node:
#		if hasattr(item, 'Children'):
#			for child in item.Children:
#				c, created = Category.objects.get_or_create(slug=slugify(child.Name), name=child.Name, creator=admin)
#				c.parents.add(category)
#				c.save()
#				add_browse_node_children(c, child.BrowseNodeId)
#		else: #leaf
#			if last_browse_id.last_id and last_browse_id.last_id != browse_node_id:
#				write_trace('skip')
#				return
#			else:
#				last_browse_id.save_last_id(browse_node_id)
#				get_products_and_save(category, browse_node_id)

class ProductInfo():
	def __init__(self, p):
		self.asin = p.ASIN
		self.upc = p.UPC
		self.manufacturer = p.Manufacturer if hasattr(p, 'Manufacturer') else p.Brand if hasattr(p, 'Brand') else None
		self.title = p.Title if hasattr(p, 'Title') else None
		self.desc = ""
		if hasattr(p, 'Feature'):
			if hasattr(p.Feature, '__getitem__'):
				for f in p.Feature:
					self.desc += f + "\r\n"
			else:
				self.desc = p.Feature
		self.swatch = None
		self.small = None
		self.medium = None
		self.large = None
		if hasattr(p, 'ImageSets') and hasattr(p.ImageSets, 'ImageSet'):
			imageSet = p.ImageSets.ImageSet[0] if hasattr(p.ImageSets.ImageSet, '__getitem__') else p.ImageSets.ImageSet
			self.swatch = imageSet.SwatchImage.URL if hasattr(imageSet, 'SwatchImage') and hasattr(imageSet.SwatchImage, 'URL') else None
			self.small = imageSet.SmallImage.URL if hasattr(imageSet, 'SmallImage') and hasattr(imageSet.SmallImage, 'URL') else None
			self.medium = imageSet.MediumImage.URL if hasattr(imageSet, 'MediumImage') and hasattr(imageSet.MediumImage, 'URL') else None
			self.large = imageSet.LargeImage.URL if hasattr(imageSet, 'LargeImage') and hasattr(imageSet.LargeImage, 'URL') else None
		self.rating = None
		self.total_review = None
		if hasattr(p, 'CustomerReviews'):
			self.rating = p.CustomerReviews.AverageRating if hasattr(p.CustomerReviews, 'AverageRating') else None
			self.total_review = p.CustomerReviews.TotalReviews if hasattr(p.CustomerReviews, 'TotalReviews') else None
		self.rank = p.SalesRank if hasattr(p, 'SalesRank') else None
		self.model = p.Model if hasattr(p, 'Model') else None
		self.m_part_number = p.MPN if hasattr(p, 'MPN') else None
		self.list_price = GetDecimal(p.ListPrice.Amount) if hasattr(p, 'ListPrice') else None
		self.merchantId = None
		self.merchantName = None
		self.OfferListingId = None
		self.free_shipping = None
		self.formatted_price = None
		self.price_amount = None
#		if hasattr(p, 'Offers') and hasattr(p.Offers, 'Offer'):
#			o = p.Offers.Offer[0] if hasattr(p.Offers.Offer, '__getitem__') else p.Offers.Offer
#			if hasattr(o, 'Merchant'):
#				self.merchantId = o.Merchant.MerchantId if hasattr(o.Merchant, 'MerchantId') else None
#				self.merchantName = o.Merchant.Name if hasattr(o.Merchant, 'Name') else None
#			if hasattr(o, 'OfferListing'):
#				self.OfferListingId = o.OfferListing.OfferListingId if hasattr(o.OfferListing, 'OfferListingId') else None
#				self.free_shipping = o.OfferListing.IsEligibleForSuperSaverShipping if hasattr(o.OfferListing, 'IsEligibleForSuperSaverShipping') else None
#				if hasattr(o.OfferListing, 'Price'):
#					self.formatted_price = o.OfferListing.Price.FormattedPrice if hasattr(o.OfferListing.Price, 'FormattedPrice') else None
#					self.price_amount = o.OfferListing.Price.Amount if hasattr(o.OfferListing.Price, 'Amount') else None
		if hasattr(p, 'Offers') and hasattr(p.Offers, 'Offer'):
			if hasattr(p.Offers.Offer, '__getitem__'):
				for o in p.Offers.Offer:
					if(o.Merchant.Name == 'Amazon.com'):
						self.printProd(o)
						return
				self.printProd(p.Offers.Offer[0])
			else:
				self.printProd(p.Offers.Offer)
						
	def printProd(self, o):
		if hasattr(o, 'Merchant'):
			self.merchantId = o.Merchant.MerchantId if hasattr(o.Merchant, 'MerchantId') else None
			self.merchantName = o.Merchant.Name if hasattr(o.Merchant, 'Name') else None
		if hasattr(o, 'OfferListing'):
			self.OfferListingId = o.OfferListing.OfferListingId if hasattr(o.OfferListing, 'OfferListingId') else None
			self.free_shipping = o.OfferListing.IsEligibleForSuperSaverShipping if hasattr(o.OfferListing, 'IsEligibleForSuperSaverShipping') else None
			if hasattr(o.OfferListing, 'Price'):
				self.formatted_price = o.OfferListing.Price.FormattedPrice if hasattr(o.OfferListing.Price, 'FormattedPrice') else None
				self.price_amount = o.OfferListing.Price.Amount if hasattr(o.OfferListing.Price, 'Amount') else None
#		if hasattr(o, 'Merchant'):
#			print 'MerchantId: ' + o.Merchant.MerchantId if hasattr(o.Merchant, 'MerchantId') else None
#			print 'Name: ' + o.Merchant.Name if hasattr(o.Merchant, 'Name') else None
#		if hasattr(o, 'OfferListing'):
#			print 'OfferListingId: ' + o.OfferListing.OfferListingId if hasattr(o.OfferListing, 'OfferListingId') else None
#			print 'IsEligibleForSuperSaverShipping: ' + o.OfferListing.IsEligibleForSuperSaverShipping if hasattr(o.OfferListing, 'IsEligibleForSuperSaverShipping') else None
#			if hasattr(o.OfferListing, 'Price'):
#				print 'FormattedPrice: ' + o.OfferListing.Price.FormattedPrice if hasattr(o.OfferListing.Price, 'FormattedPrice') else None
						

#class LastSavedId():
#	def __init__(self, filename):
#		self.__filename = filename
#		self.last_id = None		
#		try:
#			f = open(self.__filename)
#			self.last_id = f.read()
#			f.close()
#		except:
#			pass
#
#	def save_last_id(self, id):
#		self.last_id = None
#		f = open(self.__filename, 'w')
#		f.write(id)
#		f.close()

def get_product(productId):
#	last_asin_id.save_last_id('')
#	try:
#		items = ItemSearch(None, SearchIndex="Electronics", BrowseNode=category_browse_node_id,\
#										MerchantId='Featured', Condition='New', Sort='salesrank', ResponseGroup="ItemAttributes,OfferFull,Images,SalesRank,Reviews")
#		for p in items:
#			if not hasattr(p, 'ASIN'): #not a real product
#				continue
#			write_trace( '* Product: ' + p.ASIN)
#			if last_asin_id.last_id and last_asin_id.last_id != p.ASIN:
#				write_trace('skip')
#				continue
#			else:
#				last_asin_id.save_last_id(p.ASIN)
	items = ItemLookup(productId, MerchantId='Featured', Condition='New', ResponseGroup="ItemAttributes,OfferFull,Images,SalesRank,Reviews")
	for pp in items:
		if not hasattr(pp, 'ASIN'): #not a real product
			continue
		p = ProductInfo(pp)
#			manufacturer_i, created = Company.objects.get_or_create(slug=slugify(p_info.manufacturer[:199]), name=p_info.manufacturer[:199], creator=admin)
#				product_i = Product(slug=slugify(p_info.title[:349]), name=p_info.title[:349], upc=p_info.upc, model=p_info.model, \
#					manufacturer=manufacturer_i, description=p_info.desc, creator=admin, amazon_sales_rank=p_info.rank, \
#					swatch_image_url=p_info.swatch, small_image_url=p_info.small, medium_image_url=p_info.medium, large_image_url=p_info.large, \
#					amazon_review_rating=p_info.rating, amazon_total_reviews=p_info.total_review, part_number=p_info.m_part_number)
#				product_i.categories.add(category)
	if p.OfferListingId:
		p.price = GetPrice(p)
		p.shipping = 'free shipping' if p.free_shipping == '1' else None
		p.subject = '{0.title} ${0.price} @ {0.merchantName}'.format(p)
		url = 'http://www.amazon.com/dp/{0.asin}?tag=pric048-20'.format(p)
		p.body = '<a href="{1}">{0.title} {0.merchantName} ${0.price}</a><br /><a href="{1}"><img src="{0.large}" border="0" /></a>'.format(p,url)
	return p

from ArticlePoster import ArticlePoster

if __name__ == "__main__" :
	if(len(sys.argv) < 3):
		print 'Usage: python productRetriever.py user_id amazon_url|asin'
		sys.exit()
	
	m = re.search('(http.+/(dp|-|gp\/product)/)?(\w+)[/\?]?.*', sys.argv[2])
	if m:
		asin = m.group(3)
	else:
		print 'No Amazon ASIN number found'
		sys.exit()
	for a in sys.argv:
		print a
	print asin
	setLicenseKey("AKIAJPVEF4ZXJTBXRJOA");
	setSecretKey('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')
	setLocale('us')
	global cart
	cart = None

	if sys.argv[1] == "print":
		p = get_product(asin)
		print p.subject
		print p.body
	else:
		poster = ArticlePoster(sys.argv[1])
		poster.article_add(get_product(asin))
		poster.write()
