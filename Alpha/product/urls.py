from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from product.models import Product, Schedule

urlpatterns = \
	patterns('', #product search
#		url(r'^$', 'product.views.products', name="all_products"),
#		url(r'^(\d+)/$', 'product.views.product', name="product_detail"),
#		url(r'^search/$', 'product.views.search', name="product_search"),
		url(r'^(?P<slug>[\w-]+)$', 'product.views.product', name="product_detail"),
#		url(r'^create/$', 'product.views.create', name="product_create"),
#		url(r'^category/(?P<slug>[\w-]+)$', 'product.views.category', name="product_category"),
		# schedule
#		url(r'^schedule/add/([^/]+)/$', 'product.views.schedule_add', kwargs={"add": True}, name="product_schedule_add"),
#		url(r'^schedule/edit/(\d+)/$', 'product.views.schedule_edit', name="schedule_edit"),
#		url(r'^schedule/post_preview/(\d+)/$', 'product.views.schedule_post_preview', name="schedule_post_preview"),
		url(r'^schedule/(?P<state>[\w]{2})$', 'product.views.schedule_list', name="schedule_list"),
		url(r'^schedule/(?P<slug>[\w-]+)$', 'product.views.schedule', name="schedule_detail"),
		url(r'^schedule/json/', 'product.views.schedule_json', name="schedule_json"),
		url(r'^signup/(?P<id>[0-9]+)$', 'product.views.signup', name='schedule_signup'),

#        url(r'^(\w+)/prices/$', 'product.views.prices', name="product_prices"),
    )