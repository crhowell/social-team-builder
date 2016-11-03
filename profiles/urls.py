from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.ShowProfile.as_view(), name="view_profile"),
]
