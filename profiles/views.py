from django.views import generic
from braces.views import LoginRequiredMixin


class ShowProfile(LoginRequiredMixin, generic.TemplateView):
    template_name = 'profile.html'


class EditProfile(LoginRequiredMixin, generic.TemplateView):
    template_name = 'profile_edit.html'
