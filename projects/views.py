from django.views import generic

from braces.views import LoginRequiredMixin
from . import models


class ProjectListView(generic.ListView):
    model = models.Project
    template_name = 'project_list.html'
    context_object_name = 'projects'


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Project
    template_name = 'project_create.html'
    fields = ('title', 'description', 'is_active')
