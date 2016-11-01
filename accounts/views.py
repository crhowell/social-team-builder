from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from authtools import views as authviews

from braces import views as bracesviews


User = get_user_model()


class LoginView(bracesviews.AnonymousRequiredMixin, authviews.LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm


class LogoutView(authviews.LogoutView):
    url = reverse_lazy('home')


class SignUpView(bracesviews.AnonymousRequiredMixin,
                 bracesviews.FormValidMessageMixin,
                 generic.CreateView):
    model = User
    template_name = 'signup.html'
    success_url = reverse_lazy('home')
    form_class = UserCreationForm
    form_valid_message = "You're signed up!"
