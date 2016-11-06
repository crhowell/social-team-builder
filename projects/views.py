from django.views import generic

from braces.views import LoginRequiredMixin, PrefetchRelatedMixin
from . import models


class ProjectListView(generic.ListView):
    model = models.Project
    template_name = 'project_list.html'
    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        return context


class ProjectDetailView(PrefetchRelatedMixin, generic.DetailView):
    model = models.Project
    template_name = 'project_detail.html'
    context_object_name = 'project'
    prefetch_related = ['creator__profile', 'positions', 'positions__related_skills']

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['profile'] = context['project'].creator.profile
        context['positions'] = context['project'].positions.all()
        return context


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Project
    template_name = 'project_create.html'
    fields = ('title', 'description', 'is_active')
