"""mitcbdayapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views, api_views


urlpatterns = [ 
    re_path(r"^__reload__/", include("django_browser_reload.urls"))
]


# Staff
urlpatterns += [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^staff/$', views.staffListView.as_view(), name='stafflist'),
    re_path(r'^add/$', views.staffDetailsCreate.as_view(), name = 'addstaff'),
    re_path(r'^staff/(?P<pk>\d+)$', views.staffDetailsView.as_view(), name='staffdetails'),
    re_path(r'^staff/(?P<pk>\d+)/update/$', views.staffDetailsUpdate.as_view(), name='updatestaff'),
    re_path(r'^staff/(?P<pk>\d+)/delete/$', views.removeStaff, name='removestaff')
]


# Search
urlpatterns += [
    re_path(r'^search/$', views.searchQueryView.as_view(), name='searchresult')
]


# APIs
urlpatterns += [
    path('api/first_api_view/', api_views.all_staff)
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    