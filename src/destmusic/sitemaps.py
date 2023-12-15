from django.contrib.sitemaps import Sitemap
from .models import Author, Update

class AuthorSitemap(Sitemap):
    changefreq = 'hourly'
    priority = 0.5

    def items(self):
        return list(Author.objects.order_by('-id'))

class UpdateSitemap(Sitemap):
    changefreq = 'hourly'
    priority = 0.8

    def items(self):
        return list(Update.objects.order_by('-id'))