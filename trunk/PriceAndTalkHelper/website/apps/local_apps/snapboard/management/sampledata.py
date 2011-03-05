import os

from django.db.models import signals 
from django.conf import settings

from snapboard import models as snapboard_app

def test_setup(**kwargs):
    from random import choice
    from django.contrib.auth.models import User
    from snapboard.models import Post, Board
    from snapboard import sampledata

    if not settings.DEBUG:
        return 

    if Post.objects.all().count() > 0:
        # return, since there seem to already be posts in the database.
        return
    
    # ask for permission to create the test
    msg = """
    You've installed SNAPboard with DEBUG=True, do you want to populate
    the board with random users/boards/posts to test-drive the application?
    (yes/no):
    """
    populate = raw_input(msg).strip()
    while not (populate == "yes" or populate == "no"):
        populate = raw_input("\nPlease type 'yes' or 'no': ").strip()
    if populate == "no":
        return

    # create 10 random users

    users = ('john', 'sally', 'susan', 'amanda', 'bob', 'tully', 'fran')
    for u in users:
        user = User.objects.get_or_create(username=u)
        # user.is_staff = True

    cats = ('Random Topics',
            'Good Deals',
            'Skiing in the Vermont Area',
            'The Best Restaurants')
    for c in cats:
        cat = Board.objects.get_or_create(label=c)

    # create up to 30 posts
    tc = range(1, 50)
    for i in range(0, 35):
        print 'post ', i, 'created'
        cat= choice(Board.objects.all())
        subj = choice(sampledata.objects.split('\n'))

        for j in range(0, choice(tc)):
            text = '\n\n'.join([sampledata.sample_data() for x in range(0, choice(range(2, 5)))])
            # create a post
            post = Post(
                    subject = subj,
                    user=choice(User.objects.all()),
                    board=cat,
                    text=text,
                    ip='.'.join([str(choice(range(1,255))) for x in (1,2,3,4)]),
                    )
            # allows setting of arbitrary ip
            post.management_save()

signals.post_syncdb.connect(test_setup, sender=snapboard_app) 
# vim: ai ts=4 sts=4 et sw=4

