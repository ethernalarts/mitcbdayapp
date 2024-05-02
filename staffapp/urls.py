from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views, api_views

# Staff
urlpatterns = [
    re_path(r'^$', views.HomePageView.as_view(), name='index'),
    re_path(r'^staff/$', views.StaffListView.as_view(), name='stafflist'),
    re_path(r'^add/$', views.StaffCreateView.as_view(), name='addstaff'),
    re_path(r'^staff/(?P<pk>\d+)$', views.StaffDetailsView.as_view(), name='staffdetails'),
    re_path(r'^staff/(?P<pk>\d+)/update/$', views.StaffUpdateView.as_view(), name='updatestaff'),
    re_path(r'^staff/(?P<pk>\d+)/delete/$', views.StaffDeleteView.as_view(), name='deletestaff'),
    re_path(r'^staffdeleted/$', views.staff_deleted, name='staffdeleted'),
]


# Search
urlpatterns += [
    re_path(r'^staff/search/$', views.SearchQueryView.as_view(), name='searchresult')
]


# APIs
urlpatterns += [
    path('api/all-staff/', api_views.AllStaff.as_view(), name='all-staff-api')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    