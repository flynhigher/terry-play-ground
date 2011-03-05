from django.contrib import admin
from product.models import Category, Product, Schedule, Signup

class ProductAdmin(admin.ModelAdmin):
#	list_display = ('name', 'manufacturer', 'model', 'upc')
	ordering = ('name',)
#	search_fields = ('name', 'model', 'part_number', '=upc', 'description')
#	filter_horizontal = ('categories',)
#	raw_id_fields = ('manufacturer', 'related_products')

class ScheduleAdmin(admin.ModelAdmin):
#	date_hierarchy = 'created'
	list_display = ('buycode', 'title_or_product_title', 'venue', 'city', 'state', 'start')
#	list_filter = ('deal_type', 'retailer', 'creator')
#	raw_id_fields = ('product', 'retailer')
#	ordering = ('-created', 'product')
#	search_fields = ('product__name', 'retailer__name', 'product_code', 'description')
	def title_or_product_title(self, obj):
		if obj.title:
			return obj.title
		else:
			return obj.product.name + ', ' + obj.city + ', ' + obj.state

#class CategoryAdmin(admin.ModelAdmin):
#	list_display = ('name', 'amazon_id', 'deleted')
#	list_filter = ('deleted',)
#	ordering = ('name',)
#	search_fields = ('name', '=amazon_id')

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Signup)
