
from django.contrib import admin
from blog.models import *
# Register your models here.
admin.site.register(Tavar)
admin.site.register(Tavar_nomi)
admin.site.register(Mijoz)
admin.site.register(Tavar_rasmiylashtirish)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user']


@admin.register(MijozTavar)
class MijozTavarAdmin(admin.ModelAdmin):
    list_display = ['mijoz', 'tavar']

@admin.register(Kassa)
class KassaAdmin(admin.ModelAdmin):
    list_display = ['yuk']