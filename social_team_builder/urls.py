from django.conf.urls import url, include
from django.contrib import admin

from . import views


urlpatterns = [
    url(r'^$', views.HomepageView.as_view(), name='home'),
    url(r'^', include('accounts.urls', namespace='accounts')),
    url(r'^admin/', admin.site.urls),
]
