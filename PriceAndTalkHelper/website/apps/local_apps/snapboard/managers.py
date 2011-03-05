import logging
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q

_log = logging.getLogger('snapboard.managers')

class PostManager(models.Manager):
    def get_query_set(self):
        select = {}
        extra_abuse_count = """
            SELECT COUNT(*) FROM snapboard_abusereport
                WHERE snapboard_post.id = snapboard_abusereport.post_id
            """
        select['abuse'] = extra_abuse_count

        return super(PostManager, self).get_query_set().extra(
            select = select).exclude(revision__isnull=False).order_by('-gsticky', '-date')#('odate')

    def get_user_query_set(self, user):
        try:
            us = user.sb_usersettings
        except ObjectDoesNotExist:
            pass
        else:
            if us.frontpage_filters.count():
                return self.get_query_set().filter(
                    board__in=us.frontpage_filters.all())
        return self.get_query_set()

    def posts_for_board(self, board_id, user):
        '''
        Returns a query set filtered to contain only the posts the user is 
        allowed to see with regards the post's ``private`` and ``censor`` 
        attributes.
        This does not perform any board permissions check.
        '''
        # XXX: Before the Post.private refactor, the query here used to return
        # duplicate values, forcing the use of SELECT DISTINCT.
        # Do we still have such a problem, and if so, why?
        qs = self.get_query_set().filter(board__id=board_id).select_related().distinct()
        if user.is_authenticated():
            qs = qs.filter((Q(user=user) | Q(is_private=False) | Q(private__exact=user)))
        else:
            qs = qs.exclude(is_private=True)
        if not getattr(user, 'is_staff', False):
            qs = qs.exclude(censor=True)
        return qs

    def get_favorites(self, user):
        wl = user.sb_watchlist.all()
        return self.get_query_set().filter(pk__in=[x.post_id for x in wl])

    def get_private(self, user):
        return self.get_query_set().filter(private__exact=user).select_related()

    def get_board(self, board_id):
        return self.get_query_set().filter(board__id=board_id)

class BoardManager(models.Manager):
    def get_query_set(self):
        post_count = """
            SELECT COUNT(*) FROM snapboard_post
            WHERE snapboard_post.board_id = snapboard_board.id
            """
        return super(BoardManager, self).get_query_set().extra(
            select = {'post_count': post_count})
                
# vim: ai ts=4 sts=4 et sw=4
