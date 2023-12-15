from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, re_path
import destmusic.views
from django.views.static import serve
from django.views.generic.base import TemplateView
from .settings import MEDIA_ROOT, STATIC_ROOT, DEVELOPMENT
from destmusic.sitemaps import AuthorSitemap, UpdateSitemap

sitemaps = {'authors': AuthorSitemap, 'updates': UpdateSitemap}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dash', destmusic.views.dash),
    path('', destmusic.views.index),
    path('updates', destmusic.views.updates),
    path('updates/<str:version>', destmusic.views.update),
    path('author/<str:name>', destmusic.views.author),

    # SEO
    path('robots.txt', TemplateView.as_view(template_name='files/robots.txt', content_type='text/plain')),
    re_path(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    re_path(r'^upload/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT})
]

if DEVELOPMENT:
    urlpatterns.append(path('develop', destmusic.views.index_development)) 

# urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)