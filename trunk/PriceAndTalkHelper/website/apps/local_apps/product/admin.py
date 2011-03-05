from django.contrib import admin
from product.models import Category, Product, Company, Price

class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'manufacturer', 'model', 'upc')
	ordering = ('name',)
	search_fields = ('name', 'model', 'part_number', '=upc', 'description')
	filter_horizontal = ('categories',)
	raw_id_fields = ('manufacturer', 'related_products')

class PriceAdmin(admin.ModelAdmin):
	date_hierarchy = 'created'
	list_display = ('product', 'price', 'list_price', 'shipping', 'retailer', 'created', 'expired', 'cleaned_url')
	list_filter = ('deal_type', 'retailer', 'creator')
	raw_id_fields = ('product', 'retailer')
	ordering = ('-created', 'product')
	search_fields = ('product__name', 'retailer__name', 'product_code', 'description')

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'amazon_id', 'deleted')
	list_filter = ('deleted',)
	ordering = ('name',)
	search_fields = ('name', '=amazon_id')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Company)
admin.site.register(Price, PriceAdmin)
