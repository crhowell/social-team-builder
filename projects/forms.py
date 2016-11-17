from django import forms

from . import models


class FormSetMedia(forms.ModelForm):
    class Media:
        js = (
            'js/jquery.formset.js',
        )


class ProjectCreateForm(FormSetMedia):
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

    class Meta:
        model = models.Project
        fields = ('title', 'description', 'requirements', 'timeline')


class PositionCreateForm(FormSetMedia):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Position name',
                'class': ''
            }
        )
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Position description',
                'class': ''
            }
        )
    )

    class Meta:
        model = models.Position
        fields = ('name', 'description')


PositionFormSet = forms.modelform_factory(
    models.Position,
    form=PositionCreateForm
)

PositionInlineFormSet = forms.modelformset_factory(
    models.Position,
    form=PositionCreateForm,
    fields=('name', 'description'),
    extra=0,
    min_num=1,
    max_num=8
)