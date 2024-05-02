from django.urls import re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "bday"

urlpatterns = [
    re_path(r'^$', views.BirthdayCheckView.as_view(), name='birthday'),
    re_path(r'^staff/(?P<pk>\d+)/sendmessage/$', views.send_birthday_message, name='send-birthday-message'),
    # re_path(r'^staff/sendmessage/$', views.send_birthday_message_button, name='get_birthday_message_button'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
