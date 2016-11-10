from django import forms

from . import models


class ProjectCreateForm(forms.ModelForm):
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Project Title',
                'class': 'circle--input--h1'
            })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Project description...'})
    )
    requirements = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Applicant Requirements'})
    )
    timeline = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Project estimate',
                'class': 'circle--textarea--input'
            })
    )
    is_active = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'default': False})
    )

    class Meta:
        model = models.Project
        fields = ('title', 'description', 'requirements', 'timeline', 'is_active')

# TODO: Create custom form for positions for placeholders and classes

PositionInlineFormSet = forms.inlineformset_factory(
    models.Project,
    models.Position,
    extra=0,
    fields=('name', 'description', 'total'),
    min_num=1,
    max_num=8
)
