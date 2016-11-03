from django import forms
from django.contrib.auth import authenticate, get_user_model
from authtools import forms as authforms


class LoginForm(forms.ModelForm):

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError('Email or password is invalid')

        return self.cleaned_data


class SignUpForm(authforms.UserCreationForm):

    email = forms.CharField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'E-mail'})
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Verify password'})
    )

    class Meta:
        model = get_user_model()
        fields = ('email',)
