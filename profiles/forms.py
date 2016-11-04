from django import forms

from . import models


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = (
            'first_name',
            'last_name',
            'avatar',
            'bio',
            'skills'
        )