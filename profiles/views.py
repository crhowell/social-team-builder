from django.core.urlresolvers import reverse_lazy
from django.views import generic
from braces.views import LoginRequiredMixin, PrefetchRelatedMixin

from . import forms
from . import models


class ShowProfile(LoginRequiredMixin, PrefetchRelatedMixin, generic.DetailView):
    model = models.UserProfile
    template_name = 'profile.html'
    context_object_name = 'profile'
    prefetch_related = ['user__projects', 'skills']

    def get_context_data(self, **kwargs):
        context = super(ShowProfile, self).get_context_data(**kwargs)
        context['projects'] = context['profile'].user.projects.all()
        context['skills'] = context['profile'].skills.all()
        return context


class EditProfile(LoginRequiredMixin, PrefetchRelatedMixin, generic.UpdateView):
    model = models.UserProfile
    form_class = forms.UserProfileUpdateForm
    template_name = 'profile_edit.html'
    context_object_name = 'profile'
    prefetch_related = ['user__projects', 'skills']

    def get_success_url(self):
        return reverse_lazy('profiles:show_profile', kwargs={'slug': self.object.slug})
