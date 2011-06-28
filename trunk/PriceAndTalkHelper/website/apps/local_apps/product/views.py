import re

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden, HttpResponseNotFound

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from product.models import *
from product.admin import *
from product.forms import *
from django.core.urlresolvers import reverse

try:
    from notification import models as notification
except ImportError:
    notification = None

try:
    from friends.models import Friendship
    friends = True
except ImportError:
    friends = False

try:
    from threadedcomments.models import ThreadedComment
    forums = True
except ImportError:
    forums = False

try:
    from wiki.models import Article
    from wiki.views import get_ct
    wiki = True
except ImportError:
    wiki = False

from zwitschern.models import TweetInstance

import hotshot
import os
import time
import settings

try:
    PROFILE_LOG_BASE = settings.PROFILE_LOG_BASE
except:
    PROFILE_LOG_BASE = os.path.join(os.path.dirname(__file__), "profile")


def profile(log_file):
    """Profile some callable.

    This decorator uses the hotshot profiler to profile some callable (like
    a view function or method) and dumps the profile data somewhere sensible
    for later processing and examination.

    It takes one argument, the profile log name. If it's a relative path, it
    places it under the PROFILE_LOG_BASE. It also inserts a time stamp into the 
    file name, such that 'my_view.prof' become 'my_view-20100211T170321.prof', 
    where the time stamp is in UTC. This makes it easy to run and compare 
    multiple trials.     
    """

    if not os.path.isabs(log_file):
        log_file = os.path.join(PROFILE_LOG_BASE, log_file)

    def _outer(f):
        def _inner(*args, **kwargs):
            # Add a timestamp to the profile output when the callable
            # is actually called.
            (base, ext) = os.path.splitext(log_file)
            base = base + "-" + time.strftime("%Y%m%dT%H%M%S", time.gmtime())
            final_log_file = base + ext

            prof = hotshot.Profile(final_log_file)
            try:
                ret = prof.runcall(f, *args, **kwargs)
            finally:
                prof.close()
            return ret

        return _inner
    return _outer

def products(request):
    products = Product.objects.filter(amazon_sales_rank__lt=1000).order_by("amazon_sales_rank", "-amazon_total_reviews", "-amazon_review_rating")
    return render_to_response("product/products.html", {
        "products": products,
    }, context_instance=RequestContext(request))

from django.http import HttpResponseRedirect

def handle_upc(request, upc):
	return handle_itemid(request, upc, idType='UPC')

def handle_asin(request, asin):
	return handle_itemid(request, asin)

def handle_newegg(request, neweggid):
    return handle_itemid_newegg(request, neweggid)

def handle_itemid(request, itemId, idType='ASIN'):
	from awsProductCrawler import get_or_create_product

	#getting the information from db always
	#	p = Product.objects.filter(price__product_code=itemId)
	#getting the latest information from amazon always
	p = None
	if p and p.count > 0:
		return HttpResponseRedirect(reverse('product_detail', args=[p[0].slug]))
	else:
		if request.user.is_authenticated():
			user = request.user
		else:
			user = User.objects.get(username="PriceAndTalk")
	#		ret = subprocess.call([settings.PYTHON_CMD, settings.PRODUCT_RETRIEVER, asin, user.username], shell=True)
	#		if ret == 0:
	#			p = Product.objects.filter(price__product_code=itemId)
	#			if p and p.count > 0:
	#				return HttpResponseRedirect(reverse('product_detail', args=[p[0].slug]))
		p, created, pr, pr_created, pr_a, pr_a_created = get_or_create_product(itemId, user, idType)
		if p:
			if request.user.is_authenticated():
				request.user.message_set.create(message="Item has just been " + ("created" if created else "updated"))
			return HttpResponseRedirect(reverse('product_detail', args=[p.slug]))
	return None

def ptpost(request, asin, boardid = 4):
	boardid = int(boardid)
	from awsProductCrawler import get_or_create_product, write_trace

	user = User.objects.get(username="PriceAndTalk")
	p, created, pr, pr_created, pr_a, pr_a_created = get_or_create_product(asin, user, 'ASIN')
	price = None
	if pr_a and pr_a_created:
		price = pr_a
	elif pr_created:
		price = pr
	if not price:
		if p:
			if request.user.is_authenticated():
				request.user.message_set.create(message="The price has not yet been changed")
			return HttpResponseRedirect(reverse('product_detail', args=(p.slug,)))
		else:
			raise Http404
	from django.template import loader
	from templatetags.product_tags import price_post_body, price_post_subject
	from snapboard.models import Post, Board
	from snapboard.views import post_article_to_pt
	t = loader.get_template("product/price_post_body.html")
	ts = loader.get_template("product/price_post_subject.html")
	board = get_object_or_404(Board, pk=boardid)
	# create the post
	post = Post(
					subject = ts.render(RequestContext(request, price_post_subject(price))),
					user = user,
					board = board,
					text = t.render(RequestContext(request, price_post_body(price))),
					)
	post.save()
	# post to P&T - commented due to imported article's user does not appear to match current user (level)
	category = 'Other'
	try:
		category = p.categories.all()[0].name
	except:
		pass
	post_article_to_pt(post, category, boardid)
	# redirect to new thread
	return HttpResponseRedirect(reverse('snapboard_post', args=(post.id,)))

def handle_itemid_newegg(request, itemId, idType='ASIN'):
    import cj

    #p = cj.getProduct(cj.NEWEGG_ID, itemId)
    #if p:

    if request.user.is_authenticated():
        user = request.user
    else:
        user = User.objects.get(username="PriceAndTalk")
    p, created = cj.get_or_create_cj_product(itemId, user, idType)
    if p:
        if request.user.is_authenticated():
            request.user.message_set.create(message="Item has just been " + ("created" if created else "updated"))
        return HttpResponseRedirect(reverse('product_detail', args=[p.slug]))

    return None

def handle_search_query_old(request, query):
    #match amazon url
    m = re.search('(http.+/(dp|-|gp\/product)/)(\w+)[/\?]?.*', query)
    asin = None
    newegg = None

    if m:
        asin = m.group(3)
    elif query.startswith('B') and len(query) == 10: #asin
        asin = query
    elif query.startswith('N82'):
        newegg = query
        #asin = 'B0021LT066'

    if asin:
        response = handle_asin(request, asin)
        if response:
            return response
    elif newegg:
        response = handle_newegg(request, newegg)
        if response:
                return response
        else:
                request.user.message_set.create(message="Can't get the newegg product at this time. Please try later.")
                return HttpResponseRedirect('/product/')
    elif query.startswith('http'):
        response = handle_search_query(request, query)
        if response:
            return response
        else:
            request.user.message_set.create(message="Can't get the product at this time. Please try later.")
            return HttpResponseRedirect('/product/')

def handle_search_query(request, query):
    if not query.startswith('http'):
        return None
    from scraper import scraper
    s = scraper.get_scraper(query)
    if not s:
        raise 'Can''t get the scraper...'
        return None
    pd = s.get_product()

    if request.user.is_authenticated():
        user = request.user
    else:
        user = User.objects.get(username="PriceAndTalk")
    p, created, pr, pr_created, pr_a, pr_a_created = get_or_create_product2(pd, user)
    if p:
        if request.user.is_authenticated():
            request.user.message_set.create(message="Item has just been " + ("created" if created else "updated"))
        return HttpResponseRedirect(reverse('product_detail', args=[p.slug]))
    else:
        raise 'Can''t get the product...'
        return None

def search(request):
    from awsProductCrawler import search_products

    products = []
    query = request.GET.get('q', '')
    page = request.GET.get('page', '')
    if query:
        response = handle_search_query_old(request, query)
        if response:
            return response
        else:
            m = re.search('\d{12}', query)
            upc = None
            if m:
                upc = m.group()
                response = handle_upc(request, upc)
                if response:
                    return response
            q = get_queryset(Product.objects.all(), query, ProductAdmin.search_fields)
            products = q.order_by("amazon_sales_rank", "-amazon_total_reviews", "-amazon_review_rating")
            amazon_count, amazon_results = search_products(query, page)
            return render_to_response("product/search.html", {"products": products,
                                                "query" : query,
                                                "page" : page,
                                                "amazon_count" : amazon_count,
                                                "amazon_results" : amazon_results},
                              context_instance=RequestContext(request))

def create(request, form_class=ProductForm, template_name="product/create.html"):
    if request.user.is_authenticated() and request.method == "POST":
        if request.POST["action"] == "create":
            product_form = form_class(request.POST)
            if product_form.is_valid():
                product = product_form.save(commit=False)
                product.creator = request.user
                product.save()
#                product.members.add(request.user)
#                product.save()
                if notification:
                    # @@@ might be worth having a shortcut for sending to all users
                    notification.send(User.objects.all(), "product_new_product", {"product": product}, queue=True)
                    if friends: # @@@ might be worth having a shortcut for sending to all friends
                        notification.send((x['friend'] for x in Friendship.objects.friends_for_user(product.creator)), "product_friend_product", {"product": product})
                #return render_to_response("base.html", {
                #}, context_instance=RequestContext(request))
                return HttpResponseRedirect(product.get_absolute_url())
        else:
            product_form = form_class()
    else:
        product_form = form_class()

    return render_to_response(template_name, {
        "product_form": product_form,
    }, context_instance=RequestContext(request))

def delete(request, slug, redirect_url=None):
    product = get_object_or_404(Product, slug=slug)
    if not redirect_url:
        redirect_url = "/product/" # @@@ can't use reverse("product") -- what is URL name using things?

    # @@@ eventually, we'll remove restriction that product.creator can't leave product but we'll still require product.members.all().count() == 1
    if request.user.is_authenticated() and request.method == "POST" and request.user.is_staff:
        product.deleted = True
        product.save()
        request.user.message_set.add(message="Product %s deleted." % product)
        # @@@ no notification as the deleter must be the only member

    return HttpResponseRedirect(redirect_url)

def your_product(request, template_name="product/your_product.html"):
    return render_to_response(template_name, {
        "product": Product.objects.filter(deleted=False, members=request.user).order_by("name"),
    }, context_instance=RequestContext(request))
your_product = login_required(your_product)

#@profile("product_view.prof")
def product(request, slug, form_class=ProductUpdateForm,
        template_name="product/product.html"):
    product = get_object_or_404(Product, slug=slug)

#    if product.deleted:
#        raise Http404

    if request.user.is_authenticated() and request.method == "POST":
        if request.POST["action"] == "update" and request.user == product.creator:
            product_form = form_class(request.POST, instance=product)
            if product_form.is_valid():
                product = product_form.save()
        else:
            product_form = form_class(instance=product)
        if request.POST["action"] == "join":
            product.members.add(request.user)
            request.user.message_set.add(message="You have joined the product %s" % product.name)
            if notification:
                notification.send([product.creator], "product_addd_new_member", {"user": request.user, "product": product})
                notification.send(product.members.all(), "product_new_member", {"user": request.user, "product": product})
                if friends: # @@@ might be worth having a shortcut for sending to all friends
                    notification.send((x['friend'] for x in Friendship.objects.friends_for_user(request.user)), "product_friend_joined", {"user": request.user, "product": product})
        elif request.POST["action"] == "leave":
            product.members.remove(request.user)
            request.user.message_set.add(message="You have left the product %s" % product.name)
            if notification:
                pass # @@@
    else:
        product_form = None #form_class(instance=product)

    prices = Price.objects.filter(product=product).order_by('-updated')
    if not prices:
        prices = Price.objects.filter(product_code=product.other_id).order_by('-updated')
    total_prices = prices.count()
#    prices = prices[:5]
#    articles = Article.objects.filter(
#        content_type=get_ct(product),
#        object_id=product.id).order_by('-last_update')
#    total_articles = articles.count()
#    articles = articles[:5]

#    tweets = TweetInstance.objects.tweets_for(product).order_by("-sent")

#    are_member = request.user in product.members.all()

    return render_to_response(template_name, {
        "product_form": product_form,
        "product": product,
        "prices": prices,
		"total_prices": total_prices,
#        "articles": articles,
#        "tweets": tweets,
#        "total_articles": total_articles,
#        "are_member": are_member,
    }, context_instance=RequestContext(request))

def company(request, slug,
					template_name="product/company.html"):
	pass

def category(request, slug,
					template_name="product/category.html"):
	pass

def price(request, id, form_class=PriceForm,
        template_name="product/price.html"):
    product = get_object_or_404(Price, id=id)

    if product.deleted:
        raise Http404

    if request.method == "POST":
      if request.user.is_authenticated():
        topic_form = form_class(request.POST)
        if topic_form.is_valid():
          topic = topic_form.save(commit=False)
          topic.price = price
          topic.creator = request.user
          topic.save()
          request.user.message_set.add(message="You have started the topic %s" % topic.title)
#                    if notification:
#                        notification.send(product.members.all(), "product_new_topic", {"topic": topic})
          topic_form = form_class() # @@@ is this the right way to reset it?
      else:
        return HttpResponseForbidden()
    else:
      topic_form = form_class()

    return render_to_response(template_name, {
        "price": price,
        "topic_form": topic_form,
    }, context_instance=RequestContext(request))

@login_required
def price_post_preview(request, id, template_name="product/price_post_preview.html"):
	price = get_object_or_404(Price, id=id)
#	
#	if request.method == "POST":
#		topic_form = form_class(request.POST)
#		if topic_form.is_valid():
#			topic = topic_form.save(commit=False)
#			topic.price = price
#			topic.creator = request.user
#			topic.save()
#			request.user.message_set.add(message="You have started the topic %s" % topic.title)
##										if notification:
##												notification.send(product.members.all(), "product_new_topic", {"topic": topic})
#			topic_form = form_class() # @@@ is this the right way to reset it?
#	else:
#		pass
##		topic_form = form_class()

	return render_to_response(template_name, {
            "is_amazon": True if price.cleaned_url.find('amazon.com') >= 0 else False,
			"price": price,
			"price_desc_len": 0 if price.description == None else len(price.description),
	}, context_instance=RequestContext(request))

def price_add(request, form_class=PriceForm, template_name="product/price_add.html"):
    if request.user.is_authenticated() and request.method == "POST":
        if request.POST["action"] == "create":
            product_form = form_class(request.POST)
            if product_form.is_valid():
                product = product_form.save(commit=False)
                product.creator = request.user
                product.save()
#                product.members.add(request.user)
#                product.save()
                if notification:
                    # @@@ might be worth having a shortcut for sending to all users
                    notification.send(User.objects.all(), "product_new_product", {"product": product}, queue=True)
                    if friends: # @@@ might be worth having a shortcut for sending to all friends
                        notification.send((x['friend'] for x in Friendship.objects.friends_for_user(product.creator)), "product_friend_product", {"product": product})
                #return render_to_response("base.html", {
                #}, context_instance=RequestContext(request))
                return HttpResponseRedirect(product.get_absolute_url())
        else:
            product_form = form_class()
    else:
        product_form = form_class()

    return render_to_response(template_name, {
        "product_form": product_form,
    }, context_instance=RequestContext(request))

class Site:
	def __init__(self, array):
		self.name = array[0]
		self.url = array[1]
		self.message = array[2] if len(array) > 2 else None

def sitelist(request, view='retailer', edit=False, template_name="product/sitelist.html"):
	from os.path import join
	from django.conf import settings
	message=None
	filename = join(settings.WEB_ROOT, view + '.txt')
	pagename = 'Web Retailer List for Price & Talk' if view == 'retailer' else 'Deal Site List for Price & Talk'
	f = open(filename, 'r')
	file_content = f.read()
	f.close()
	if request.method == "POST" and request.POST['content']:
		if request.user.is_authenticated():
			if request.POST['content'] != file_content:
				f=open(filename, 'w')
				f.write(request.POST['content'])
				f.close()
				file_content = request.POST['content']
				request.user.message_set.create(message="You have just changed the website list")
		else:
			message="Please login to make modification"

	sites = [Site(line.split('|')) for line in file_content.split('\n')]
	return render_to_response(template_name, {
	    "pagename": pagename,
	    "sites": sites,
	    "file_content": file_content,
	    "message": message,
	    "edit": edit,
	}, context_instance=RequestContext(request))
#
#def topic(request, id, edit=False, template_name="product/topic.html"):
#    topic = get_object_or_404(Topic, id=id)
#    
#    if topic.product.deleted:
#        raise Http404
#    
#    if request.method == "POST" and edit == True and \
#        (request.user == topic.creator or request.user == topic.product.creator):
#        topic.body = request.POST["body"]
#        topic.save()
#        return HttpResponseRedirect(reverse('product_topic', args=[topic.id]))
#    return render_to_response(template_name, {
#        'topic': topic,
#        'edit': edit,
#    }, context_instance=RequestContext(request))
#
#def topic_delete(request, pk):
#    topic = Topic.objects.get(pk=pk)
#    
#    if topic.product.deleted:
#        raise Http404
#    
#    if request.method == "POST" and (request.user == topic.creator or \
#        request.user == topic.product.creator): 
#        if forums:
#            ThreadedComment.objects.all_for_object(topic).delete()
#        topic.delete()
#    
#    return HttpResponseRedirect(request.POST["next"])
