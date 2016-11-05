from django.views import generic

from braces.views import LoginRequiredMixin
from . import models


class ProjectListView(generic.ListView):
    model = models.Project
    template_name = 'project_list.html'
    context_object_name = 'projects'


class ProjectDetailView(generic.DetailView):
    model = models.Project
    template_name = 'project_detail.html'
    context_object_name = 'project'

    def get_queryset(self):
        queryset = super(ProjectDetailView, self).get_queryset()
        return queryset.prefetch_related('creator__profile')

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['profile'] = context['project'].creator.profile
        return context


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Project
    template_name = 'project_create.html'
    fields = ('title', 'description', 'is_active')
