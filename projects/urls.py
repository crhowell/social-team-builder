from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^project/(?P<pk>\d+)/$', views.ProjectDetailView.as_view(), name='project_detail'),
    url(r'^project/add/$', views.ProjectCreateView.as_view(), name='add_project'),
    url(r'^$', views.ProjectListView.as_view(), name='project_list'),
]
