from django.views import generic
from django.db.models import Q

from braces.views import LoginRequiredMixin, PrefetchRelatedMixin

from core.mixins import IsOwnerMixin
from . import models


class ProjectListView(PrefetchRelatedMixin, generic.ListView):
    model = models.Project
    template_name = 'project_list.html'
    context_object_name = 'projects'
    prefetch_related = ['positions']

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context['project_needs'] = models.Skill.objects.filter(
            positions__project__in=context['projects']
        )
        context['curr_filter'] = self.request.GET.get('filter')
        context['curr_term'] = self.request.GET.get('s')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.GET.get('s')
        if search_term:
            queryset = queryset.filter(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term)
            )
        filter_term = self.request.GET.get('filter')
        if filter_term:
            queryset = queryset.filter(positions__related_skills__name=filter_term)
        return queryset.filter(is_active=True)


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


class ProjectEditView(LoginRequiredMixin, IsOwnerMixin, generic.UpdateView):
    model = models.Project
    template_name = 'project_edit.html'
    fields = ('title', 'description', 'is_active')

    def get_context_data(self, **kwargs):
        context = super(ProjectEditView, self).get_context_data(**kwargs)
        context['profile'] = context['project'].creator.profile
        return context