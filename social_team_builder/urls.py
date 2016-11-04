from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

from core.views import HomepageView
from projects.views import ProjectListView


urlpatterns = [
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^users/', include('profiles.urls', namespace='profiles')),
    url(r'^', include('projects.urls', namespace='projects')),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
