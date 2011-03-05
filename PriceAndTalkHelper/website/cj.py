"""Python wrapper for Commission Junction Serive APIs.

The CJ's web APIs specication is described here:
http://help.cj.com/en/web_services/web_services.htm
"""

from suds.client import Client
from suds.xsd.doctor import ImportDoctor, Import

import os, urllib, string, inspect
import hmac,hashlib,base64
from time import strftime, gmtime
from xml.dom import minidom

import slugtool
"""Package-wide variables:
"""
DEVELOPER_KEY = '00ae3f16e0f7b86c1e564ac102ebcba9d7e45e4afb03aa3675b052da4e06da24bb6a4a5ecc06bbc88889062c7d778d53a8e7b9c17e8aae2fbd2cc9adf62f149edf/6a16353ac0f7c2b3f1bbcfa994a04a070c9e302e85bbb32e922ccf86e3fb1a930f57580dc2a73f1446e56f0fb240eb7284cc2a96db53df8b8ba1c48d1e17b511'
PRICEANDTALK_ID = '3385297'
NEWEGG_ID = '1807847'
BH_ID = '2478435'
BUYCOM_ID = '1566996'
MACMALL_ID = '242732'
CJ_WSDL = 'https://product.api.cj.com/wsdl/version2/productSearchServiceV2.wsdl'

def getProduct(advertiserId, productNumber):
	
	imp1 = Import('http://product.domain.cj.com')
	imp1.filter.add('http://product.service.cj.com')
	imp2 = Import('http://product.service.cj.com')
	imp2.filter.add('http://api.cj.com')
	d=ImportDoctor(imp1,imp2)
	client = Client(CJ_WSDL, doctor=d)
	res = None
	
	if client:
		res = client.service.search(developerKey=DEVELOPER_KEY, 
														websiteId=PRICEANDTALK_ID,
														advertiserIds=advertiserId,
														serviceableArea='US',
														advertiserSku=productNumber)
	if res and res.products and len(res.products) > 0 and len(res.products[0]) > 0:
		return res.products[0][0]
	return None

def get_or_create_cj_product(itemId, creator, idType="ASIN", category=None, requireOffer=False):

    #p = cj.getProduct(cj.NEWEGG_ID, itemId)
    #if p:
	from django.db.models import Q
	p = None
	p_created = False
	newweggProd = None
	try:
		#if idType != 'ASIN':
		#	item = ItemLookup(ItemId=itemId, IdType=idType, SearchIndex='All', MerchantId='Featured', Condition='New', ResponseGroup="ItemAttributes,OfferFull,Images,SalesRank,Reviews")
		#else:
		#	item = ItemLookup(ItemId=itemId, MerchantId='Featured', Condition='New', ResponseGroup="ItemAttributes,OfferFull,Images,SalesRank,Reviews")
		#if hasattr(item, '__getitem__'):
		#	p_info = ProductInfo(item[0])
		#else:
		#	return (p, p_created)
		#if requireOffer and not p_info.OfferListingId:
		#	return (p, p_created)
	
		#manufacturer_i, created = Company.objects.get_or_create(name=p_info.manufacturer[:199], defaults={'slug':slugify(p_info.manufacturer[:199]), 'creator':creator})
		try:
			try:
				newweggProd = getProduct(NEWEGG_ID, itemId)
			except:
				return (p, p_created)	
			p = Product.objects.get(other_id=itemId)
			p = Product(id=p.id, created=p.created, creator=p.creator, name=p.name, \
				manufacturer=newweggProd.manufacturerName, description=newweggProd.description, updater=creator, updated=datetime.now(), \
				swatch_image_url=newweggProd.imageUrl, \
				small_image_url='', medium_image_url='', large_image_url='', \
				amazon_review_rating=0, amazon_total_reviews=0, part_number='')
			slugtool.unique_slugify(p, p.name[:349])
			p.save()
	#				continue
		except Product.DoesNotExist:
			p = Product(name=newweggProd.name, model='', \
				manufacturer='', description='', creator=creator, amazon_sales_rank=0, \
				swatch_image_url='', small_image_url='', medium_image_url='', large_image_url='', \
				amazon_review_rating=0, amazon_total_reviews=0, part_number='')
			slugtool.unique_slugify(p, p_info.title[:349])
			p.save()
			#if category:
			#	p.categories.add(category)
			#	p.save()
			p_created = True
			write_trace( p.name.encode('ascii', 'ignore') + ' created')
	except:
#		raise
		write_error("Exception while getting a product, %s %s" % (itemId, format_exc().encode('ascii', 'ignore')))
	return (p, p_created)

"""
   adId = 10440897
   advertiserId = 1807847
   advertiserName = "Newegg.com"
   buyUrl = "http://www.kqzyfj.com/click-3385297-10440897?url=http%3A%2F%2Fwww.newegg.com%2FProduct%2FProduct.aspx%3FItem%3DN82E16822136283%26nm_mc%3DAFC-C8Junction%26cm_mmc%3DAFC-C8Junction-_-Hard%2BDrives-_-Western%2BDigital-_-22136283&cjsku=N82E16822136283"
catalogId = 'cjo:1460'
   currency = "USD"
description = ''
imageUrl = "http://images10.newegg.com/ProductImageCompressAll200/22-136-283-03.jpg"
   inStock = None
   isbn = None
   manufacturerName = "Western Digital"
   manufacturerSku = "WD7501AALS"
   name = "Western Digital Caviar Black 750GB 3.5" SATA 3.0Gb/s Hard Drive -Bare Drive"
   price = 79.99
   retailPrice = 0.0
   salePrice = 79.99
   sku = "N82E16822136283"
   upc = None
"""