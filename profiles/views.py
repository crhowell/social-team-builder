from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.views import generic
from django.shortcuts import (get_object_or_404, reverse,
                              HttpResponseRedirect, Http404)

from braces.views import LoginRequiredMixin, PrefetchRelatedMixin

from core.mixins import IsOwnerMixin
from . import forms
from . import models


class ShowProfile(LoginRequiredMixin, PrefetchRelatedMixin, generic.TemplateView):
    model = models.UserProfile
    template_name = 'profile.html'
    context_object_name = 'profile'
    prefetch_related = [
        'my_projects', 'related_skills',
        'user__projects__positions', 'user__projects']

    def get_context_data(self, **kwargs):
        context = super(ShowProfile, self).get_context_data(**kwargs)
        context['skills'] = context['profile'].skills.all()
        context['p_projects'] = context['profile'].user.projects.all()
        context['u_projects'] = context['profile'].my_projects.all()
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
    form_class = forms.UserProfileForm
    template_name = 'profile_edit.html'
    context_object_name = 'profile'
    prefetch_related = ['my_projects', 'related_skills']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['s_formset'] = forms.SkillInlineFormSet(
            queryset=models.Skill.objects.filter(
                related_skills=context['profile']
            ),
            prefix='skill_formset'
        )
        context['p_formset'] = forms.UserProjectInlineFormSet(
            queryset=models.UserProject.objects.filter(
                profile=context['profile']
            ),
            prefix='project_formset'
        )
        return context

    def get_object(self, queryset=None):
        obj = get_object_or_404(
            models.UserProfile,
            user=self.request.user
        )
        if obj.user != self.request.user:
            raise Http404
        return obj

    def post(self, request, *args, **kwargs):
        profile = self.get_object()
        form = forms.UserProfileForm(self.request.POST, instance=profile)
        s_formset = forms.SkillInlineFormSet(
            self.request.POST,
            queryset=models.Skill.objects.filter(
                related_skills=profile
            ),
            prefix='skill_formset'
        )
        p_formset = forms.UserProjectInlineFormSet(
            self.request.POST,
            queryset=models.UserProject.objects.filter(
                profile=profile
            ),
            prefix='project_formset'
        )

        if form.is_valid():
            print('FORM is valid')
            profile = form.save(commit=False)
            if s_formset.is_valid() and p_formset.is_valid():
                skills = s_formset.save()
                projects = p_formset.save(commit=False)

                for skill in skills:
                    profile.skills.add(skill)
                profile.save()

                for project in projects:
                    project.profile = profile
                    project.save()
            else:
                print('formset not valid')

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


class UserApplicationStatus(LoginRequiredMixin, generic.TemplateView):

    def get(self, request, *args, **kwargs):
        position = self.kwargs.get('position')
        applicant = self.kwargs.get('applicant')
        status = self.kwargs.get('status')
        if status == 'approve' or status == 'deny':
            if position and applicant:
                bstatus = True if status == 'approve' else False
                models.UserApplication.objects.filter(
                    position=position, applicant=applicant
                ).update(is_accepted=bstatus)
        return HttpResponseRedirect(reverse('profiles:my_applications'))
