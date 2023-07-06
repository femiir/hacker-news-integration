from django.contrib import admin

from .models import HackerNewsComment, HackerNewsItem


# Register your models here.
class HackerNewsItemAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'title', 'by', 'score', 'descendants', 'item_type')
    list_filter = ('by',)
    search_fields = ('title', 'score', 'descendants')
    ordering = ('-id',)
class HackerNewsCommentAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'by', 'parent', 'news_item')
    list_filter = ('by', 'news_item')
    search_fields = ('text', 'by')

admin.site.register(HackerNewsItem, HackerNewsItemAdmin)
admin.site.register(HackerNewsComment, HackerNewsCommentAdmin)
