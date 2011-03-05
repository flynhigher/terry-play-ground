from django import template

register = template.Library()

@register.inclusion_tag("product/price_item.html")
def show_product_price(price):
    return {"price": price}

@register.inclusion_tag("product/price_post_subject.html")
def price_post_subject(price):
	return {"price": price,
					"product_name_len_greater_than_60" : False if price.product.name == None or len(price.product.name) <= 60 else True,
					"price_desc_len": 0 if price.description == None else len(price.description),
					}

@register.inclusion_tag("product/price_post_body.html")
def price_post_body(is_amazon, price):
	import string
	return {"is_amazon": is_amazon, "price": price,
					"product_name_len_greater_than_60" : False if price.product.name == None or len(price.product.name) <= 60 else True,
					"price_desc_len": 0 if price.description == None else len(price.description),
					"review_url": string.replace(price.cleaned_url, '/dp/', '/review/'),
					}

@register.filter
def weight(product):
	review = int(product.amazon_total_reviews) if product.amazon_total_reviews else 0
	rating = int(product.amazon_review_rating) if product.amazon_review_rating else 0
	rank = int(product.amazon_sales_rank) if product.amazon_sales_rank else 4022947
		
	return str((review/10000 * 200 + rating/5 * 300 + 1/rank * 500) * 1000)
#
#def do_get_tribe_form(parser, token):
#    try:
#        tag_name, as_, context_name = token.split_contents()
#    except ValueError:
#        tagname = token.contents.split()[0]
#        raise template.TemplateSyntaxError, "%(tagname)r tag syntax is as follows: {%% %(tagname)r as VARIABLE %%}" % locals()
#    return TribeFormNode(context_name)
#
#class TribeFormNode(template.Node):
#    def __init__(self, context_name):
#        self.context_name = context_name
#    def render(self, context):
#        context[self.context_name] = TribeForm()
#        return ''
#
#register.tag('get_tribe_form', do_get_tribe_form)