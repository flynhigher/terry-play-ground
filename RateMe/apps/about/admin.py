from django.contrib import admin
from about.models import Contact

class ContactAdmin(admin.ModelAdmin):
	ordering = ('submitteddate',)

admin.site.register(Contact, ContactAdmin)
