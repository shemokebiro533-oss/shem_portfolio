from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from core.sitemaps import StaticViewSitemap


# Sitemap configuration
sitemaps = {
    "static": StaticViewSitemap,
}


urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Sitemap
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="sitemap",
    ),

    # Core application
    path("", include("core.urls")),
]


# Media and static files during development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
