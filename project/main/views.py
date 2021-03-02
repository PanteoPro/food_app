from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView as LoginViewParent, LogoutView as LogoutViewParent
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from .forms import RegisterUserForm, LoginForm


class MainView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "main_main.html")


class LoginView(LoginViewParent):
    template_name = "login_page.html"
    form_class = LoginForm
    success_url = reverse_lazy("main")

    def get_success_url(self):  # переопределям
        return self.success_url


class RegisterView(CreateView):

    model = User
    template_name = "register_page.html"
    form_class = RegisterUserForm
    success_url = reverse_lazy("main")

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        aut_user = authenticate(username=username, password=password)
        login(self.request, aut_user)
        return form_valid


class LogoutView(LogoutViewParent):
    next_page = reverse_lazy('main')

