from django.core.urlresolvers import reverse_lazy
from django.views import generic
from braces.views import LoginRequiredMixin, PrefetchRelatedMixin


from core.mixins import IsOwnerMixin
from . import forms
from . import models


class ShowProfile(LoginRequiredMixin, PrefetchRelatedMixin, generic.DetailView):
    model = models.UserProfile
    template_name = 'profile.html'
    context_object_name = 'profile'
    prefetch_related = ['user__projects', 'skills', 'user__projects__positions']

    def get_context_data(self, **kwargs):
        context = super(ShowProfile, self).get_context_data(**kwargs)
        context['skills'] = context['profile'].skills.all()
        context['projects'] = context['profile'].user.projects.all()
        return context


class EditProfile(LoginRequiredMixin, IsOwnerMixin, PrefetchRelatedMixin, generic.UpdateView):
    model = models.UserProfile
    form_class = forms.UserProfileUpdateForm
    template_name = 'profile_edit.html'
    context_object_name = 'profile'
    prefetch_related = ['user__projects', 'skills']

    def get_success_url(self):
        return reverse_lazy('profiles:show_profile', kwargs={'slug': self.object.slug})

