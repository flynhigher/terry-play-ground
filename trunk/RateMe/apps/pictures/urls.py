from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # all pictures or latest pictures
    #url(r'^$', 'pictures.views.photos', name="photos"),
    # a photos details
    #url(r'^details/(?P<id>\d+)/$', 'pictures.views.details', name="photo_details"),
    # upload pictures
    url(r'^upload/$', 'pictures.views.upload', name="photo_upload"),
    # rate pictures for judges
    url(r'^rate/$', 'pictures.views.rate', name="photo_rate"),
    # your pictures
    #url(r'^yourpictures/$', 'pictures.views.yourphotos', name='photos_yours'),
    # a members pictures
    #url(r'^member/(?P<username>[\w]+)/$', 'pictures.views.memberphotos', name='photos_member'),
    #destory photo
    #url(r'^destroy/(?P<id>\d+)/$', 'pictures.views.destroy', name='photo_destroy'),
    #edit photo
    #url(r'^edit/(?P<id>\d+)/$', 'pictures.views.edit', name='photo_edit'),

    # for voting
    url(r'^review/(?P<image_id>\d+)/?',
        'reviews.views.do_review', name="pictures_review"),
)