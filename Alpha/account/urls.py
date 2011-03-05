from django.conf.urls.defaults import *
#from account.forms import *

urlpatterns = patterns('',
		url(r'^$', 'account.views.profile', name='profile_detail'),
    url(r'^signup/$', 'account.views.signup', name="acct_signup"),
    url(r'^login/$', 'account.views.login', name="acct_login"),
    url(r'^password_change/$', 'account.views.password_change', name="acct_passwd"),
    url(r'^password_reset/$', 'account.views.password_reset', name="acct_passwd_reset"),
    url(r'^logout/$', 'account.views.logout', name="acct_logout"),
    # ajax validation
#    (r'^validate/$', 'ajax_validation.views.validate', {'form_class': SignupForm}, 'signup_form_validate'),
)
