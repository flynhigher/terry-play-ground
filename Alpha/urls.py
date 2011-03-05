import os

from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
		url(r'^$', direct_to_template, {"template": "content/index.html"}, name="home"),
		url(r'^aboutus.html$', direct_to_template, {"template": "content/aboutus.html"}, name="aboutus"),
		url(r'^schedule.html$', direct_to_template, {"template": "content/schedule.html"}, name="schedule"),
		url(r'^register_class.html$', direct_to_template, {"template": "content/register_class.html"}, name="register_class"),
		url(r'^resources.html$', direct_to_template, {"template": "content/resources.html"}, name="resources"),
		url(r'^contactus.html$', "tools.views.contact", name="contact_us"),
		url(r'^contacttks.html$', direct_to_template, {"template": "content/contacttks.html"}, name="contacttks"),
		url(r'^privacypolicy.html$', direct_to_template, {"template": "content/privacypolicy.html"}, name="privacypolicy"),
		url(r'^servsafe.html$', direct_to_template, {"template": "content/servsafe.html"}, name="servsafe"),
		url(r'^haccp.html$', direct_to_template, {"template": "content/haccp.html"}, name="haccp"),
		url(r'^international.html$', direct_to_template, {"template": "content/international.html"}, name="international"),
		url(r'^phonesystems.html$', direct_to_template, {"template": "content/phonesystems.html"}, name="phonesystems"),
		url(r'^termsofservice.html$', direct_to_template, {"template": "content/termsofservice.html"}, name="phonesystems"),
		url(r'^product/', include("product.urls")),
		(r'^account/', include('account.urls')),
#		url(r'^aboutus.html$', direct_to_template, {"template": "content/aboutus.html"}, name="home"),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': os.path.join(os.path.dirname(__file__), "media")}),
    )
