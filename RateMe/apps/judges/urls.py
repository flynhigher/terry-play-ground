from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'judges.views.judges', name='judge_list'),
#    url(r'^(?P<username>[\w\._-]+)/$', 'judges.views.bio', name='judge_bio'),
    url(r'^signup$', 'judges.views.signup', name='judge_signup'),
)
