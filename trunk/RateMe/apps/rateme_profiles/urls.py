from django.conf.urls.defaults import *

urlpatterns = patterns('',
    #url(r'^username_autocomplete/$', 'autocomplete_app.views.username_autocomplete_friends', name='profile_username_autocomplete'),
    url(r'^$', 'rateme_profiles.views.profiles', name='profile_list'),
    url(r'^profile/(?P<username>[\w\._-]+)/$', 'rateme_profiles.views.profile', name='profile_detail'),
    url(r'^edit/$', 'rateme_profiles.views.profile_edit', name='profile_edit'),
    url(r'^edit/judge/$', 'rateme_profiles.views.profile_judge_edit', name='profile_judge_edit'),
)
