from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^(?P<slug>\w+)/edit/$', views.EditProfile.as_view(), name='edit_profile'),
    url(r'^(?P<slug>\w+)/$', views.ShowProfile.as_view(), name='show_profile'),
]
