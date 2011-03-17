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

"""Package-wide variables:
"""

sample_url='http://feed.linksynergy.com/productsearch?token=11cf7fe1181f382b01dcfbbe7b1ea4b50679f8ec7e320792b728aa35ef6ade3f&keyword=Toshiba Satellite T135D S1326 13 3 inch Notebook&MaxResults=20&pagenumber=1&mid=24542'
TOKEN = '11cf7fe1181f382b01dcfbbe7b1ea4b50679f8ec7e320792b728aa35ef6ade3f'
MICROSOFT_ID = '24542'
#NEWEGG_ID = '1807847'
#BH_ID = '2478435'
#BUYCOM_ID = '1566996'
#MACMALL_ID = '242732'
LINKSHARE_URL = 'http://feed.linksynergy.com/productsearch'
LINKSHARE_WSDL = ''

def getProduct(advertiserId, productTitle):
	client = Client(CJ_WSDL, doctor=d)
	res = client.service.search(developerKey=DEVELOPER_KEY, 
														websiteId=PRICEANDTALK_ID,
														advertiserIds=advertiserId,
														serviceableArea='US',
														advertiserSku=productNumber)
	if res and res.products and len(res.products) > 0 and len(res.products[0]) > 0:
		return res.products[0][0]
	return None
"""
   adId = 10440897
   advertiserId = 1807847
   advertiserName = "Newegg.com"
   buyUrl = "http://www.kqzyfj.com/click-3385297-10440897?url=http%3A%2F%2Fwww.newegg.com%2FProduct%2FProduct.aspx%3FItem%3DN82E16822136283%26nm_mc%3DAFC-C8Junction%26cm_mmc%3DAFC-C8Junction-_-Hard%2BDrives-_-Western%2BDigital-_-22136283&cjsku=N82E16822136283"
   catalogId = "cjo:1460"
   currency = "USD"
   description = "The Western Digital Caviar Black 750 GB Hard Drive is a top-of-the-line high-capacity drive for your PC, running at 7200 RPM. Its dual processors with breakthrough 32 MB cache makes this hard drive suitable for high-performance home and business computing, as it can handle high-end data-intensive and multimedia applications.   This hard drive incorporates WDâ€™s Data Lifeguard, an exclusive set of data protection features, including shock protection, environmental protection, real-time embedded error detection and repair. Its mechanism ensures automatic discovery, isolation, and repair of problems which may develop in a hard drive. Cache: 32MB Features: High Performance Electronics Architecture Dual processor - Twice the processing power to maximize performance. 32 MB cache - Bigger, faster cache means faster performance.   Rock Solid Mechanical Architecture StableTrac - The motor shaft is secured at both ends to reduce system-induced vibration and stabilize platters for accurate tracking, during read and write operations. NoTouch  Parts: 5 years limited Labor: 5 years limited"
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