from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from product.models import Product
from wiki import models as wiki_models

#from product.thing import productThing

wiki_args = {'product_slug_field': 'name',
             'product_qs': Product.objects.all}


#		tt.urls(url_prefix='', name_prefix='product_thing') + \
urlpatterns = \
	patterns('', #product search
		url(r'^$', 'product.views.products', name="all_products"),
#		url(r'^(\d+)/$', 'product.views.product', name="product_detail"),
		url(r'^search/$', 'product.views.search', name="product_search"),
		url(r'^ptpost/(?P<boardid>\d+)/(?P<asin>[^/]+)/$', 'product.views.ptpost', name="product_ptpost"),
		url(r'^product/([^/]+)/$', 'product.views.product', name="product_detail"),
		url(r'^product/create/$', 'product.views.create', name="product_create"),
#				url(r'^(\w+)/edit/$', 'product.views.edit', name="product_edit"),
#        url(r'^(\w+)/delete/$', 'product.views.delete', name="product_delete"),
#				url(r'^your_products/$', 'product.views.your_products', name="your_products"),
        
        # company
#				url(r'^company/add/$', 'product.views.company_add', kwargs={"add": True}, name="product_company_add"),
		url(r'^company/([^/]+)/$', 'product.views.company', name="product_company"),
#				url(r'^company/(\d+)/edit/$', 'product.views.company_edit', kwargs={"edit": True}, name="product_company_edit"),
#				url(r'^company/(\d+)/delete/$', 'product.views.company_delete', name="product_company_delete"),
		url(r'^category/([^/]+)/$', 'product.views.category', name="product_category"),
					
				# price
		url(r'^price/add/([^/]+)/$', 'product.views.price_add', kwargs={"add": True}, name="product_price_add"),
		url(r'^price/post_preview/(\d+)/$', 'product.views.price_post_preview', name="price_post_preview"),
		url(r'^retailer/$', 'product.views.sitelist', kwargs={"view": "retailer"}, name="retailer_websites"),
		url(r'^dealsite/$', 'product.views.sitelist', kwargs={"view": "dealsite"}, name="deal_websites"),
		url(r'^retailer/edit$', 'product.views.sitelist', kwargs={"view": "retailer", "edit": True}, name="retailer_websites"),
		url(r'^dealsite/edit$', 'product.views.sitelist', kwargs={"view": "dealsite", "edit": True}, name="deal_websites"),
#		url(r'^retailer/$', direct_to_template, {"template": "product/retailer.html"}, name="retailer_websites"),
#		url(r'^dealsite/$', direct_to_template, {"template": "product/dealsite.html"}, name="deal_websites"),
#		url(r'^price/post/(\d+)/$', 'product.views.price_post', name="price_post"),
#				url(r'^price/(\d+)/$', 'product.views.price', name="product_price"),
#				url(r'^price/(\d+)/edit/$', 'product.views.price_edit', kwargs={"edit": True}, name="product_price_edit"),
#				url(r'^price/(\d+)/delete/$', 'product.views.price_delete', name="product_price_delete"),

#        url(r'^(\w+)/prices/$', 'product.views.prices', name="product_prices"),
        
        # wiki
        url(r'^product/(?P<product_slug>\w+)/wiki/', include('wiki.urls'), kwargs=wiki_args),
    )