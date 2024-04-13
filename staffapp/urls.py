
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
    re_path(r'^add/$', views.staffDetailsCreate.as_view(), name='addstaff'),
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
    path('api/all-staff/', api_views.AllStaff.as_view(), name='all-staff-api')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    