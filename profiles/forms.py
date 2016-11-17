from django import forms

from core.forms import FormSetMedia
from . import models


class SkillForm(FormSetMedia):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Skill',
            'class': ''
        })
    )

    class Meta:
        model = models.Skill
        fields = ('name',)


class UserProfileUpdateForm(FormSetMedia):
    first_name = forms.CharField(
     widget=forms.TextInput(attrs={
         'placeholder': 'First name',
         'class': ''
     })
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Last name',
            'class': ''
        })
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Tell us about yourself...',
            'class': ''
        })

    )

    class Meta:
        model = models.UserProfile
        fields = ['first_name', 'last_name', 'bio', 'skills']


SkillInlineFormSet = forms.modelformset_factory(
    models.Skill,
    form=SkillForm,
    fields=('name',),
    extra=1,
    min_num=0,
    max_num=25
)
