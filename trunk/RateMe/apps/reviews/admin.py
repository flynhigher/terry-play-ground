from django.contrib import admin
from reviews.models import Review

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('image', 'user', 'score', 'comment', 'date_added', 'date_changed')
    list_filter = ('image', 'user', 'date_changed')

admin.site.register(Review, ReviewAdmin)
