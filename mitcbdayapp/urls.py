from django.contrib import admin
from django.urls import include, re_path, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^birthday/', include('birthday.urls')),
    re_path(r'^', include('staffapp.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
    # re_path(r'^api/', include('staffapp.urls'))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    