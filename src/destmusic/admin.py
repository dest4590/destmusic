from django.contrib import admin
from .models import Music, Author, Update

admin.site.register(Author)
admin.site.register(Update)

class MusicAdmin(admin.ModelAdmin):
    @admin.action(description='Mark selected musics as hidden')
    def music_make_hidden(modeladmin, request, queryset):
        queryset.update(hide=True)


    @admin.action(description='Mark selected musics as visible')
    def music_make_visible(modeladmin, request, queryset):
        queryset.update(hide=False)

    list_display = ('artwork_preview', 'name', 'author', 'genre', 'id')
    list_filter = ('genre', )
    search_fields = ('name__startswith', 'author__startswith')
    actions = [music_make_hidden, music_make_visible]

admin.site.register(Music, MusicAdmin)

# Cosmetics
admin.site.site_header = 'DestMusic Admin'
admin.site.site_title = 'DestMusic Admin Panel'
admin.site.index_title = 'Configure models'