from unittest import TestSuite

from django.contrib.auth.models import User, AnonymousUser
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from snapboard.models import *

class TestBasicViews(TestCase):
	'''
	Tests the board's basic views, that deal with boards and 
	posts. User settings and group administration are excluded.
	'''

	def setUp(self):
		self.john = User.objects.create_user('john', 'john@example.com', 'test')
		self.jane = User.objects.create_user('jane', 'jane@example.com', 'test')
	
	def test_new_post(self):
		gd = Board.objects.create(label='General discussion')
		c = Client()
		c.login(username='john', password='test')
		r = c.post(reverse('snapboard_new_post', args=(gd.id,)),{
			'subject': 'Test topic',
			'post': 'Lorem ipsum dolor sit amet.',
		})
		self.assertRedirects(r, reverse('snapboard_post', args=(1,)))
	
class TestBoardPermissions(TestCase):
	'''
	Tests that the specified permissions are honored.

	This DOES NOT test that the Board.can_xxx() methods do what they should.
	It only tests that the views use these methods correctly.
	'''
	
	def __init__(self, user, view_perms, read_perms, post_perms, new_board_perms, view_group=[], read_group=[], post_group=[], new_board_group=[]):
		self.view_perms, self.read_perms, self.post_perms, \
		self.new_board_perms, self.view_group, self.read_group,\
		self.post_group, self.new_board_group = view_perms, \
		read_perms, post_perms, new_board_perms, \
		view_group, read_group, post_group, \
		new_board_group
		self.password = 'test'
		self.test_user = user
		TestCase.__init__(self)

	def setUp(self):
		# Save the users, create the groups, create the board
		for user in self.view_group + self.read_group + self.post_group + self.new_board_group:
			if not user.pk:
				user.save()
		if not isinstance(self.test_user, AnonymousUser):
			self.test_user.set_password(self.password)
			self.test_user.save()
		self.super_user = User(username='super', email='root@example.com', password='')
		self.super_user.set_password(self.password)
		self.super_user.save()
		def _create_group(group):
			gobj = Group.objects.create(name='group')
			for user in group:
				gobj.users.add(user)
			return gobj
		self.view_group = _create_group(self.view_group)
		self.read_group = _create_group(self.read_group)
		self.post_group = _create_group(self.post_group)
		self.new_board_group = _create_group(self.new_board_group)
		self.board = Board.objects.create(label='board', view_perms=self.view_perms, read_perms=self.read_perms,
				post_perms=self.post_perms, new_board_perms=self.new_board_perms, view_group=self.view_group, read_group=self.read_group,
				post_group=self.post_group, new_board_group=self.new_board_group)
		sample_board = Board.objects.create(
				subject='Test',
				board=self.board)
		first_post = Post.objects.create(
				user=self.super_user,
				board=self.board,
				text='Lorem ipsum dolor sit amet.')

	def shortDescription(self):
		return u'Tests permissions of a board with permissions %s/%s/%s/%s and groups %s/%s/%s/%s.' % (
				self.board.get_view_perms_display(),
				self.board.get_read_perms_display(),
				self.board.get_post_perms_display(),
				self.board.get_new_board_perms_display(),
				list(self.board.view_group.users.all()),
				list(self.board.read_group.users.all()),
				list(self.board.post_group.users.all()),
				list(self.board.new_board_group.users.all()))

	def runTest(self):
		c = Client()
		user = self.test_user
		board_id = None
		post_id = None
		if not isinstance(user, AnonymousUser):
			self.failUnless(c.login(username=user.username, password=self.password))
		# Create a new post
		r = c.post(reverse('snapboard_new_board', args=(self.board.id,)),{
			'subject': 'Test topic',
			'post': 'Lorem ipsum dolor sit amet.',
		})
		if self.board.can_create_post(user):
			post_id = Post.objects.all().order_by('-pk')[0].id
			self.assertRedirects(r,
				reverse('snapboard_post', args=(post_id,)),
				target_status_code=200 if self.board.can_read(user) else 403)
		else:
			if isinstance(user, AnonymousUser):
				self.assertRedirects(r,
					'%s?next=%s' % (
						reverse('auth_login'),
						reverse('snapboard_new_post', args=(self.board.id,))))
			else:
				self.failUnlessEqual(r.status_code, 403)
		# Add a post; there is a sample post already in case the post was not created
		if not post_id:
			post_id = Post.objects.all().order_by('-pk')[0].id
		r = c.post(reverse('snapboard_post', args=(post_id,)),{
			'post': 'Testing.',
			'private': '',
		})
		post_id = Post.objects.all().order_by('-pk')[0].id
		if self.board.can_post(user):
			self.assertRedirects(r,
				reverse('snapboard_post', args=(post_id,)),
				target_status_code=302 if self.board.can_read(user) else 403)
		else:
			self.failUnlessEqual(r.status_code, 403) # forbidden
		# Quote a post
		r = c.post(reverse('snapboard_rpc_action'), {
			'action': 'quote',
			'oid': str(post_id),
		})
		if isinstance(user, AnonymousUser):
			self.assert_(r.status_code in (500, 403))
		else:
			self.failUnlessEqual(r.status_code, 200 if self.board.can_read(user) else 403)

def permutations(seq, k):
	if not len(seq):
		yield seq
	elif k == 1:
		for i in seq:
			yield [i]
	else:
		for i in seq:
			for tail in permutations(seq, k-1):
				yield [i] + tail

def suite():
	suite = TestSuite()
	suite.addTest(TestBasicViews('test_new_post'))
	# Test all sensible permission configurations
	jane = User(username='jane', email='jane@example.com', password='')
	john = User(username='john', email='john@example.com', password='')
	perms = (NOBODY, ALL, USERS, CUSTOM)
	groups = [[jane],] * 4
	for permissions in [p for p in permutations(perms, 4) if sorted(p, reverse=True) == p]:
		suite.addTest(TestBoardPermissions(jane, *(permissions + groups)))
		suite.addTest(TestBoardPermissions(john, *(permissions + groups)))
		suite.addTest(TestBoardPermissions(AnonymousUser(), *(permissions + groups)))
	return suite


