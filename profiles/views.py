from django.views import generic
from braces.views import LoginRequiredMixin

from . import models


class ShowProfile(LoginRequiredMixin, generic.DetailView):
    model = models.UserProfile
    template_name = 'profile.html'
    context_object_name = 'profile'

    def get_queryset(self):
        queryset = super(ShowProfile, self).get_queryset()
        return queryset.prefetch_related('user__projects', 'skills')

    def get_context_data(self, **kwargs):
        context = super(ShowProfile, self).get_context_data(**kwargs)
        context['projects'] = context['profile'].user.projects.all()
        context['skills'] = context['profile'].skills.all()
        return context


class EditProfile(LoginRequiredMixin, generic.UpdateView):
    model = models.UserProfile
    template_name = 'profile_edit.html'
    context_object_name = 'profile'
