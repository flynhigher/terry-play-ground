#!/usr/bin/env python
import sys

from traceback import format_exc
from datetime import datetime
from os.path import abspath, dirname, join
from site import addsitedir
from django.template.defaultfilters import slugify
from django.core.exceptions import MultipleObjectsReturned
from product.models import Category
#from django.contrib.auth.models import User

trace = False
std_out = False

def write_trace(log, force=False):
	if trace or force:
		if std_out:
			print log
		f = open('trace.txt', 'a')
		f.write(datetime.today().strftime('%c') + ': ' + log.encode('ascii', 'ignore') + '\n')
        
def write_error(error):
	if std_out:
		print error
#	f = open('error.txt', 'a')
#	f.write(datetime.today().strftime('%c') + ': ' + error.encode('ascii', 'ignore') + '\n')
	raise error.encode('ascii', 'ignore')

#APP_ROOT = abspath(join(dirname(__file__), "../"))

WEBSITE_ROOT = abspath(dirname(__file__))
APP_ROOT = WEBSITE_ROOT

path = addsitedir(join(APP_ROOT, "libs/external_libs"), set())
if path:
    sys.path = list(path) + sys.path
sys.path.insert(0, join(APP_ROOT, "apps/external_apps"))
sys.path.insert(0, join(APP_ROOT, "apps/local_apps"))

#from misc import unique_slugify
import slugtool

try:
    import settings # Assumed to be in the same directory.
except ImportError:
    e = "Error: Can't find the file 'settings.py' in the directory containing %r. "
    e += "It appears you've customized things.\nYou'll have to run django-admin.py, "
    e += "passing it your settings module.\n(If the file settings.py does indeed exist, "
    e += "it's causing an ImportError somehow.)\n"
    sys.stderr.write(e % __file__)
    sys.exit(1)

from product.models import *

from ecs import CartCreate, CartGet, CartAdd, BrowseNodeLookup, ItemSearch, ItemLookup, CartClear

#from django.core.management import execute_manager

def GetOrCreateCart(item):
	global cart
	cart = None
	if not cart:
		cart = CartCreate([item,], [1,])
		write_trace("*** Cart created!!!")
	else:
		cart = CartGet(cart)
		CartClear(cart)
		cart = CartAdd(cart, [item,], [1,])
		write_trace("*** Add item to existsing Cart!!!")
	if hasattr(cart, "CartItems"):
		if hasattr(cart.CartItems, "CartItem"):
			write_trace(cart.CartItems.CartItem.Price.FormattedPrice)

def GetPriceFromCart(p_info):
	GetOrCreateCart(p_info)
	if hasattr(cart, 'SubTotal'):
		return GetDecimal(cart.SubTotal.Amount)
	elif hasattr(cart, 'ItemTotal'):
		return GetDecimal(cart.ItemTotal.Amount)
	else:
		write_trace("Error! Cart is not valid!!!")
		write_trace(cart)
		write_trace(dir(cart))
		sys.exit()

def GetDecimal(amount):
    return amount[:-2] + '.' + amount[-2:]

def GetPrice(p_info):
	if p_info.formatted_price == 'Too low to display':
		return GetPriceFromCart(p_info)
	else:
		return GetDecimal(p_info.price_amount)

from string import *

def add_browse_node_children(category, parent_id_list, creator):
	write_trace("* Browse Node: " + category.name + "|" + category.amazon_id)
	node = None
	
	try:
		node = BrowseNodeLookup(category.amazon_id)
	except:
		write_error("Exception while doing category lookup, %s %s" % (category.amazon_id, format_exc()))

	if node:
		for item in node:
			if hasattr(item, 'Children'):
				parent_id_list.append(category.amazon_id)
				write_trace("Going through children, parent:" + str(parent_id_list))
				for child in item.Children:
#					write_trace('child id:%d and parent_id_list.count(int(child.BrowseNodeId)):%d' % (int(child.BrowseNodeId),parent_id_list.count(int(child.BrowseNodeId))))
					if find(lower(child.Name), 'accessories') >= 0:
						write_trace('accessories skip')
						continue
					elif child.BrowseNodeId == '319574011':
						write_trace('Marine Electronics skip')
						continue
					elif child.BrowseNodeId == '16285901':
						write_trace('Service & Replacement Plans')
						continue
					elif parent_id_list.count(child.BrowseNodeId) > 0:
						write_trace('Circular detected: %s %s' % (child.Name, child.BrowseNodeId))
						continue 
					c, created = Category.objects.get_or_create(name=child.Name, amazon_id=child.BrowseNodeId, defaults={'creator':creator,'slug':slugify(child.Name)})
					c.parents.add(category)
					c.save()
					add_browse_node_children(c, parent_id_list, creator)
				write_trace("End of children %s|%s" % (category.name, category.amazon_id) )
				parent_id_list.remove(category.amazon_id)
#			else: #leaf
#				if last_browse_id.last_id and last_browse_id.last_id != browse_node_id:
#					write_trace('skip')
#					return
#				else:
#					last_browse_id.save_last_id(browse_node_id)
#					get_products_and_save(category, browse_node_id)

class ProductInfo():
	def __init__(self, p=None):
		if not p:
			return
		self.asin = p.ASIN
		try:
			self.upc = p.UPC
		except:
			self.upc = None
			
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
		self.node = None
		if hasattr(p, 'BrowseNodes') and hasattr(p.BrowseNodes, 'BrowseNode'):
			self.node = p.BrowseNodes.BrowseNode[0] if hasattr(p.BrowseNodes.BrowseNode, '__getitem__') else p.BrowseNodes.BrowseNode
			self.node = get_top_node(self.node)
			self.node.Name = self.node.Name.replace('&', 'and')
			write_trace(self.asin + "'s category: " + self.node.Name)
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
		self.a_merchantId = None
		self.a_merchantName = None
		self.a_OfferListingId = None
		self.a_free_shipping = None
		self.a_formatted_price = None
		self.a_price_amount = None
		if hasattr(p, 'Offers') and hasattr(p.Offers, 'Offer'):
			o = p.Offers.Offer[0] if hasattr(p.Offers.Offer, '__getitem__') else p.Offers.Offer
			if hasattr(o, 'Merchant'):
				self.merchantId = o.Merchant.MerchantId if hasattr(o.Merchant, 'MerchantId') else None
				self.merchantName = o.Merchant.Name if hasattr(o.Merchant, 'Name') else None
			if hasattr(o, 'OfferListing'):
				self.OfferListingId = o.OfferListing.OfferListingId if hasattr(o.OfferListing, 'OfferListingId') else None
				self.free_shipping = o.OfferListing.IsEligibleForSuperSaverShipping if hasattr(o.OfferListing, 'IsEligibleForSuperSaverShipping') else None
				if hasattr(o.OfferListing, 'SalePrice'):
					self.formatted_price = o.OfferListing.SalePrice.FormattedPrice if hasattr(o.OfferListing.SalePrice, 'FormattedPrice') else None
					self.price_amount = o.OfferListing.SalePrice.Amount if hasattr(o.OfferListing.SalePrice, 'Amount') else None
				elif hasattr(o.OfferListing, 'Price'):
					self.formatted_price = o.OfferListing.Price.FormattedPrice if hasattr(o.OfferListing.Price, 'FormattedPrice') else None
					self.price_amount = o.OfferListing.Price.Amount if hasattr(o.OfferListing.Price, 'Amount') else None
			amazonid = 'ATVPDKIKX0DER'
			o = None
			if self.merchantId != amazonid and hasattr(p.Offers.Offer, '__getitem__'):
				for offer in p.Offers.Offer:
					if hasattr(offer, 'Merchant') and hasattr(offer.Merchant, 'MerchantId') and offer.Merchant.MerchantId == amazonid:
						self.a_merchantId = amazonid
						self.a_merchantName = offer.Merchant.Name if hasattr(offer.Merchant, 'Name') else None
						if hasattr(offer, 'OfferListing'):
							self.a_OfferListingId = offer.OfferListing.OfferListingId if hasattr(offer.OfferListing, 'OfferListingId') else None
							self.a_free_shipping = offer.OfferListing.IsEligibleForSuperSaverShipping if hasattr(offer.OfferListing, 'IsEligibleForSuperSaverShipping') else None
							if hasattr(offer.OfferListing, 'SalePrice'):
								self.a_formatted_price = offer.OfferListing.SalePrice.FormattedPrice if hasattr(offer.OfferListing.SalePrice, 'FormattedPrice') else None
								self.a_price_amount = offer.OfferListing.SalePrice.Amount if hasattr(offer.OfferListing.SalePrice, 'Amount') else None
							elif hasattr(offer.OfferListing, 'Price'):
								self.a_formatted_price = offer.OfferListing.Price.FormattedPrice if hasattr(offer.OfferListing.Price, 'FormattedPrice') else None
								self.a_price_amount = offer.OfferListing.Price.Amount if hasattr(offer.OfferListing.Price, 'Amount') else None
						break

def get_top_node(node):
	if hasattr(node, 'Ancestors') and hasattr(node.Ancestors, 'BrowseNode'):
		return get_top_node(node.Ancestors.BrowseNode)
	else:
		return node

class LastSavedId():
	def __init__(self, filename):
		self.__filename = filename
		self.last_id = None		
		try:
			f = open(self.__filename)
			self.last_id = f.read()
			f.close()
		except:
			pass

	def save_last_id(self, id):
		self.last_id = None
		f = open(self.__filename, 'w')
		f.write(id)
		f.close()

def get_or_create_product(itemId, creator, idType="ASIN", category=None, requireOffer=False):
	p = None
	p_created = False
	p_info = None
	pr = None
	pr_a = None
	pr_created = None
	pr_a_created = None
	from django.db.models import Q
	try:
		if idType != 'ASIN':
			item = ItemLookup(ItemId=itemId, IdType=idType, SearchIndex='All', MerchantId='Featured', Condition='New', ResponseGroup="ItemAttributes,OfferFull,Images,SalesRank,Reviews,BrowseNodes")
		else:
			item = ItemLookup(ItemId=itemId, MerchantId='Featured', Condition='New', ResponseGroup="ItemAttributes,OfferFull,Images,SalesRank,Reviews,BrowseNodes")
		if hasattr(item, '__getitem__'):
			p_info = ProductInfo(item[0])
		else:
			return (p, p_created)
		if requireOffer and not p_info.OfferListingId:
			return (p, p_created)

		manufacturer_i, created = Company.objects.get_or_create(name=p_info.manufacturer[:199], defaults={'slug':slugify(p_info.manufacturer[:199]), 'creator':creator})
		try:
			p = Product.objects.get(upc=p_info.upc) if p_info.upc else Product.objects.get(other_id=p_info.asin)
			p = Product(id=p.id, created=p.created, creator=p.creator, name=p_info.title[:349], upc=p_info.upc, model=p_info.model, \
				manufacturer=manufacturer_i, description=p_info.desc, updater=creator, updated=datetime.now(), \
				amazon_sales_rank=p_info.rank if p_info.rank else 400000, swatch_image_url=p_info.swatch, \
				small_image_url=p_info.small, medium_image_url=p_info.medium, large_image_url=p_info.large, \
				amazon_review_rating=p_info.rating, amazon_total_reviews=p_info.total_review, part_number=p_info.m_part_number,other_id=p_info.asin)
			slugtool.unique_slugify(p, p_info.title[:349])
			p.save()
	#				continue
		except Product.DoesNotExist:
			p = Product(name=p_info.title[:349], upc=p_info.upc, model=p_info.model, \
				manufacturer=manufacturer_i, description=p_info.desc, creator=creator, amazon_sales_rank=p_info.rank if p_info.rank else 400000, \
				swatch_image_url=p_info.swatch, small_image_url=p_info.small, medium_image_url=p_info.medium, large_image_url=p_info.large, \
				amazon_review_rating=p_info.rating, amazon_total_reviews=p_info.total_review, part_number=p_info.m_part_number,other_id=p_info.asin)
			slugtool.unique_slugify(p, p_info.title[:349])
			p.save()
			if not category and p_info.node:
				write_trace(p_info.node.Name)
				category, created = Category.objects.get_or_create(slug=slugify(p_info.node.Name), name=p_info.node.Name, amazon_id=p_info.node.BrowseNodeId, creator=creator)
			if category:
				p.categories.add(category)
				p.save()
			p_created = True
			write_trace( p.name.encode('ascii', 'ignore') + ' created')
		if p_info.OfferListingId:
			if p_info.a_OfferListingId:
				a_p_info = ProductInfo()
				a_p_info.asin = p_info.asin
				a_p_info.list_price = p_info.list_price
				a_p_info.OfferListingId = p_info.a_OfferListingId
				a_p_info.merchantName = p_info.a_merchantName
				a_p_info.merchantId = p_info.a_merchantId
				a_p_info.free_shipping = p_info.a_free_shipping
				a_p_info.price_amount = p_info.a_price_amount
				a_p_info.formatted_price = p_info.a_formatted_price
				pr_a, pr_a_created = create_retailer_price(p, a_p_info, creator)
			pr, pr_created = create_retailer_price(p, p_info, creator)
	except:
#		raise
		write_error("Exception while getting a product, %s %s" % (itemId, format_exc().encode('ascii', 'ignore')))
	return (p, p_created, pr, pr_created, pr_a, pr_a_created)

def create_retailer_price(product, p_info, creator):
	m, created = Company.objects.get_or_create(name=p_info.merchantName, defaults={'slug':slugify(p_info.merchantName), 'creator':creator})
	price = GetPrice(p_info)
	shipping = 0 if p_info.free_shipping == '1' else None
	general_url = 'http://www.amazon.com/dp/' + p_info.asin
	url = general_url + '?m='  + p_info.merchantId
	price_i = None
	try: 
		price_i, created = Price.objects.get_or_create(product=product, price=price, shipping=shipping, retailer=m,
			defaults={'list_price':p_info.list_price, 'source_url':general_url, 'cleaned_url':url, 'creator':creator, 'product_code':p_info.asin})
	except MultipleObjectsReturned:
		pass
	if created:
		write_trace(product.name.encode('ascii', 'ignore') + ' $' + price + ' created')
	else:
		last_p = None
		try:
			last_p = Price.objects.filter(product=product, retailer=m).order_by('-created')[0]
		except:
			pass
		if last_p and price_i and price_i.price != last_p.price:
			price_i = Price.objects.create(product=product, price=price, shipping=shipping, retailer=m,	list_price=p_info.list_price,
			                               source_url=general_url, cleaned_url=url, creator=creator, product_code=p_info.asin)
			write_trace(product.name.encode('ascii', 'ignore') + ' $' + price + ' created (changed)')
			created = True
	return price_i, created
		
def get_products_and_save(category, creator):
#	last_asin_id.save_last_id('')
	counter = 0
	try:
		items = ItemSearch(None, SearchIndex="Electronics", BrowseNode=category.amazon_id,\
										MerchantId='Featured', Condition='New', Sort='salesrank', ResponseGroup="ItemAttributes")
		write_trace('Product count in category, %s (%s): %d' % (category.name, category.amazon_id, len(items)))
		for p in items:
			counter += 1
			if not hasattr(p, 'ASIN'): #not a real product
				continue
			write_trace( '* Product: ' + p.ASIN)
#			if last_asin_id.last_id and last_asin_id.last_id != p.ASIN:
#				write_trace('skip')
#				continue
#			else:
#				last_asin_id.save_last_id(p.ASIN)
			if not hasattr(p, 'UPC'): #not a real product
				continue
			if not hasattr(p, 'Manufacturer') and not hasattr(p, 'Brand'): #not a real product
				continue
#In order to save memory usage get full information for each product instead of fetching everything at ItemSearch
			get_or_create_product(p.ASIN, creator, category, requireOffer=True)
	except:
#		raise
		write_error("Exception while getting items under category, %s %s" % (category.amazon_id, format_exc().encode('ascii', 'ignore')))
	return counter

		
def search_products(query, page):
	result = []
	total = 0
	num_items_per_page = 20
	counter = 0
	if page and int(page) > 1:
		start_num = (int(page) - 1) * num_items_per_page + 1
		end_num = int(page) * num_items_per_page
	else:
		start_num = 1
		end_num = num_items_per_page
	try:
		items = ItemSearch(query, SearchIndex="All", MerchantId='Featured', Condition='New')
#		write_trace('Product count for query, %s: %d' % (query, len(items)))
		total = len(items)
		for p in items:
			if not hasattr(p, 'ASIN'): #not a real product
				continue
			counter += 1
			if counter < start_num:
				continue
			result.append((p.ASIN, p.Title)) #str(dir(p))
			if counter == end_num:
				break
	except:
#		raise
		write_error("Exception while getting search result for the query, %s %s" % (query, format_exc().encode('ascii', 'ignore')))
	return total, result
