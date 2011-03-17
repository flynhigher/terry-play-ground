from django.contrib import admin
from pictures.models import Image, Pool

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('question','date_added','is_public','member','safetylevel','tags',)

class PoolAdmin(admin.ModelAdmin):
    list_display = ('photo', )

admin.site.register(Image, PhotoAdmin)
admin.site.register(Pool, PoolAdmin)
