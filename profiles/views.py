from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.shortcuts import get_object_or_404, reverse, HttpResponseRedirect, Http404
from django.db.models import Q

from braces.views import LoginRequiredMixin, PrefetchRelatedMixin

from core.mixins import IsOwnerMixin
from . import forms
from . import models


class ShowProfile(LoginRequiredMixin, PrefetchRelatedMixin, generic.TemplateView):
    model = models.UserProfile
    template_name = 'profile.html'
    context_object_name = 'profile'
    prefetch_related = ['user__projects', 'related_skills', 'user__projects__positions']

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
    prefetch_related = ['user__projects', 'related_skills']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['formset'] = forms.SkillInlineFormSet(
            queryset=models.Skill.objects.filter(
                pk__in=models.UserRelatedSkill.objects.filter(
                    profile=context['profile']
                )
            ),
            prefix='skill_formset'
        )
        return context

    def get_object(self, queryset=None):
        obj = get_object_or_404(models.UserProfile,
                          user=self.request.user)
        if obj.user != self.request.user:
            raise Http404
        return obj

    def post(self, request, *args, **kwargs):
        form = forms.UserProfileUpdateForm(self.request.POST)
        formset = forms.SkillInlineFormSet(self.request.POST)

        if form.is_valid():
            form.save()
            if formset.is_valid():
                formset.save_m2m()
                return HttpResponseRedirect(reverse('profiles:my_profile'))
        return HttpResponseRedirect(reverse('profiles:my_profile'))

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
