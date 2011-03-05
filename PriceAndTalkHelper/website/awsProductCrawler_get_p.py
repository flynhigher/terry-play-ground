#!/usr/bin/env python
import sys

from os.path import abspath, dirname, join

APP_ROOT = abspath(join(dirname(__file__), "../"))
sys.path.insert(0, APP_ROOT)

if __name__ == "__main__" :
#	from ecs import setLicenseKey, setSecretKey
	from django.contrib.auth.models import User
	from awsProductCrawler import get_or_create_product

#	setLicenseKey("AKIAJPVEF4ZXJTBXRJOA");
#	setSecretKey('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')
	
	asin = sys.argv[1]
	userid = sys.argv[2]
	try:
		user = User.objects.get(username=userid)
	except:
		try:
			admin = User.objects.get(username="PriceAndTalk")
		except User.DoesNotExist:
			admin = User.objects.create_superuser(username="PriceAndTalk", email="priceandtalk@gmail.com", password="little12")
	
	p, created, pr, pr_created, pr_a, pr_a_created = get_or_create_product(asin, user)