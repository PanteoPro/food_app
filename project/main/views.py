from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView as LoginViewParent, LogoutView as LogoutViewParent
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from .forms import RegisterUserForm, LoginForm, ProfileSettingsForm, EatIngredientForm
from .models import Profile

from config.service.views import set_model_get_in_context, set_model_all_in_context, set_model_filter_in_context

from .forms import EatCookForm
from .service.essential import update_profile
from .service.views import set_info_for_profile_in_context, change_profile, create_eat_cook, message_manager, \
    create_eat_ingredient
from food.models import Cook, IngredientItem


class LoginView(LoginViewParent):
    """Показывает страницу с Авторизацией"""
    template_name = "login_page.html"
    form_class = LoginForm
    success_url = reverse_lazy("main")

    def get_success_url(self):  # переопределям
        return self.success_url


class RegisterView(CreateView):
    """Показывает страницу с Регистрацией"""

    model = User
    template_name = "register_page.html"
    form_class = RegisterUserForm
    success_url = reverse_lazy("main")

    def form_valid(self, form):
        """Правильно сохранение пароля в django"""
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        aut_user = authenticate(username=username, password=password)
        login(self.request, aut_user)
        return form_valid


class LogoutView(LogoutViewParent):
    """Выход из аккаунта"""
    next_page = reverse_lazy('main')


class ProfileView(View):
    """Показывает страницу профиля"""

    def get(self, request, *args, **kwargs):
        context = dict()
        update_profile(request.user)
        set_model_get_in_context(Profile, context, user=request.user)
        set_info_for_profile_in_context(context, request.user)
        return render(request, "profile_page.html", context=context)


class ProfileSettingsView(View):
    """Показывает страницу настроек профиля"""

    def get(self, request, *args, **kwargs):
        context = dict()
        return render(request, "profile_settings.html", context=context)


class ProfileSettingsApplyView(View):
    """Принятие настроек пользователя"""

    def post(self, request, *args, **kwargs):
        result = change_profile(request)
        message_manager(request, result)
        if not result["success"]:
            return redirect("/main/profile_settings")
        return redirect("/main")


class EatCookView(View):
    """Показывает страницу употребления блюда"""

    def get(self, request, *args, **kwargs):
        form = EatCookForm()
        context = dict()
        context["form"] = form
        set_model_filter_in_context(Cook, context, is_ended=False, is_overdue=False)
        return render(request, "eat_cook.html", context=context)


class EatCookAddView(View):
    """Принимает post запрос, для добавления употребляемого блюда"""

    def post(self, request, *args, **kwargs):
        result = create_eat_cook(request)
        message_manager(request, result)
        return redirect("/main/eat_cook")


class EatIngredientView(View):
    """Показывает страницу употребления продукта"""

    def get(self, request, *args, **kwargs):
        form = EatIngredientForm()
        context = dict()
        context["form"] = form
        set_model_filter_in_context(IngredientItem, context, name_field="ingredient_items",
                                    is_ended=False, is_overdue=False)
        return render(request, "eat_ingredient_item.html", context=context)


class EatIngredientAddView(View):
    """Принимает post запрос, для добавления употребляемого продукта"""

    def post(self, request, *args, **kwargs):
        result = create_eat_ingredient(request)
        message_manager(request, result)
        return redirect("/main/eat_ingredient_item")


