from django.shortcuts import get_object_or_404
from django.views import generic
from braces.views import LoginRequiredMixin

from . import models


class ShowProfile(LoginRequiredMixin, generic.DetailView):
    model = models.UserProfile
    template_name = 'profile.html'
    context_object_name = 'profile'


class EditProfile(LoginRequiredMixin, generic.TemplateView):
    template_name = 'profile_edit.html'
