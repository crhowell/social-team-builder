from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.shortcuts import get_object_or_404, redirect

from braces.views import LoginRequiredMixin, PrefetchRelatedMixin

from core.mixins import IsOwnerMixin
from . import forms
from . import models


class ShowProfile(LoginRequiredMixin, PrefetchRelatedMixin, generic.TemplateView):
    model = models.UserProfile
    template_name = 'profile.html'
    context_object_name = 'profile'
    prefetch_related = ['user__projects', 'skills', 'user__projects__positions']

    def get_context_data(self, **kwargs):
        context = super(ShowProfile, self).get_context_data(**kwargs)
        context['skills'] = context['profile'].skills.all()
        context['projects'] = context['profile'].user.projects.all()
        return context

    def get(self, request, **kwargs):
        slug = self.kwargs.get('slug')
        if slug:
            profile = get_object_or_404(models.UserProfile, slug=slug)
        else:
            profile = self.request.user.profile

        kwargs['profile'] = profile
        return super().get(request, **kwargs)


class EditProfile(LoginRequiredMixin, IsOwnerMixin, PrefetchRelatedMixin, generic.UpdateView):
    model = models.UserProfile
    form_class = forms.UserProfileUpdateForm
    template_name = 'profile_edit.html'
    context_object_name = 'profile'
    prefetch_related = ['user__projects', 'skills']

    def get_success_url(self):
        return reverse_lazy('profiles:show_profile', kwargs={'slug': self.object.slug})


class UserApplications(LoginRequiredMixin, PrefetchRelatedMixin, generic.ListView):
    model = models.UserApplication
    template_name = 'applications.html'
    context_object_name = 'application_list'
    prefetch_related = ['applicant__projects',
                        'applicant__projects__positions']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(project__creator=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = self.request.user.projects.all()
        return context
