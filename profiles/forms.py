from django import forms

from . import models


class UserProfileUpdateForm(forms.ModelForm):
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
