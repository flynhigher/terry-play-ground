#!/usr/bin/env python
import sys, traceback

from datetime import datetime
from os.path import abspath, dirname, join
from site import addsitedir
from django.template.defaultfilters import slugify
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth.models import User

trace = True

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

from awsProductCrawler import *

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

from ecs import *
from site import addsitedir


from string import *
	
if __name__ == "__main__" :
	setLicenseKey("AKIAJPVEF4ZXJTBXRJOA");
	setSecretKey('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')
	global last_browse_id
	last_browse_id = LastSavedId('last_browse_id.txt')
	global last_asin_id
	last_asin_id = LastSavedId('last_id.txt')

	global cart
	cart = None

	global admin
	try:
		admin = User.objects.get(username="PriceAndTalk")
	except User.DoesNotExist:
		admin = User.objects.create_superuser(username="PriceAndTalk", email="priceandtalk@gmail.com", password="little12")
	
	e, created = Category.objects.get_or_create(slug='Electronics', name='Electronics', amazon_id='172282', creator=admin)
#	add_browse_node_children(e, [], admin)

	p, created = Category.objects.get_or_create(slug=slugify('Audio & Video'), name='Audio & Video', amazon_id='1065836', creator=admin)
	p.parents.add(e)
	p.save()
	add_browse_node_children(p, [e.amazon_id, p.amazon_id], admin)

	p, created = Category.objects.get_or_create(slug=slugify('Camera & Photo'), name='Camera & Photo', amazon_id='502394', creator=admin)
	p.parents.add(e)
	p.save()
	add_browse_node_children(p, [e.amazon_id, p.amazon_id], admin)

	p, created = Category.objects.get_or_create(slug=slugify('Car Electronics'), name='Car Electronics', amazon_id='1077068', creator=admin)
	p.parents.add(e)
	p.save()
	add_browse_node_children(p, [e.amazon_id, p.amazon_id], admin)

	p, created = Category.objects.get_or_create(slug=slugify('Computers & Add-Ons'), name='Computers & Add-Ons', amazon_id='541966', creator=admin)
	p.parents.add(e)
	p.save()
	add_browse_node_children(p, [e.amazon_id, p.amazon_id], admin)

	p, created = Category.objects.get_or_create(slug=slugify('Home Audio & Theater'), name='Home Audio & Theater', amazon_id='667846011', creator=admin)
	p.parents.add(e)
	p.save()
	add_browse_node_children(p, [e.amazon_id, p.amazon_id], admin)
	
	p, created = Category.objects.get_or_create(slug=slugify('Office Electronics'), name='Office Electronics', amazon_id='172574', creator=admin)
	p.parents.add(e)
	p.save()
	add_browse_node_children(p, [e.amazon_id, p.amazon_id], admin)

	p, created = Category.objects.get_or_create(slug=slugify('Portable Audio & Video'), name='Portable Audio & Video', amazon_id='172623', creator=admin)
	p.parents.add(e)
	p.save()
	add_browse_node_children(p, [e.amazon_id, p.amazon_id], admin)

	p, created = Category.objects.get_or_create(slug=slugify('Security & Surveillance'), name='Security & Surveillance', amazon_id='524136', creator=admin)
	p.parents.add(e)
	p.save()
	add_browse_node_children(p, [e.amazon_id, p.amazon_id], admin)

	p, created = Category.objects.get_or_create(slug=slugify('Televisions & Video'), name='Televisions & Video', amazon_id='1266092011', creator=admin)
	p.parents.add(e)
	p.save()
	add_browse_node_children(p, [e.amazon_id, p.amazon_id], admin)
#
#	last_browse_id.save_last_id('')
#	last_asin_id.save_last_id('')
