#!/usr/bin/env python
import sys

from os.path import abspath, dirname, join
from site import addsitedir
#from django.template.defaultfilters import slugify
#from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth.models import User

trace = False

#APP_ROOT = abspath(join(dirname(__file__), "../"))
WEBSITE_ROOT = abspath(dirname(__file__))
APP_ROOT = WEBSITE_ROOT

path = addsitedir(join(APP_ROOT, "libs/external_libs"), set())
if path:
    sys.path = list(path) + sys.path
sys.path.insert(0, join(APP_ROOT, "apps/external_apps"))
sys.path.insert(0, join(APP_ROOT, "apps/local_apps"))

#from misc import unique_slugify
#import slugtool

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

from ecs import setLicenseKey, setSecretKey
#from site import addsitedir

#from django.core.management import execute_manager

#from string import *

from awsProductCrawler import LastSavedId, get_products_and_save

if __name__ == "__main__" :
	setLicenseKey("AKIAJPVEF4ZXJTBXRJOA");
	setSecretKey('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')
#	global last_browse_id
	last_browse_id = LastSavedId('last_browse_id.txt')
	if last_browse_id.last_id:
		last_saved_id = last_browse_id.last_id
	else:
		last_saved_id = '0'
#	global last_asin_id
#	last_asin_id = LastSavedId('last_id.txt')

#	global cart
#	cart = None
#
#	global admin
	try:
		admin = User.objects.get(username="PriceAndTalk")
	except User.DoesNotExist:
		admin = User.objects.create_superuser(username="PriceAndTalk", email="priceandtalk@gmail.com", password="little12")
	
#	e, created = Category.objects.get_or_create(slug='Electronics', name='Electronics', amazon_id=172282, creator=admin)
#	add_browse_node_children(e)
	counter = 0
	for category in Category.objects.filter(deleted=0).filter(amazon_id__gt=last_saved_id).order_by('amazon_id'):
		item_counter = get_products_and_save(category, admin)
		counter += 1
		last_browse_id.save_last_id(category.amazon_id)
		if counter == 10 or (item_counter and item_counter > 5000):
			sys.exit()
	
	last_browse_id.save_last_id('')
#	last_asin_id.save_last_id('')
