from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .models import Profile, EatCook, EatIngredient
from .service.models import create_model_profile

from food.service.models import get_model_cook__already, get_model_ingredient_item__already


class RegisterUserForm(forms.ModelForm):
    """Форма регистрации"""

    class Meta:
        model = User
        fields = ("username", "password")
        widgets = {
            "password": forms.TextInput(attrs={"type": "password"})
        }

    def __init__(self, *args, **kwargs):
        """Изменение поведение формы при инициализации. Добавляем в поля формы класс form-class"""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-class"

    def save(self, commit=True):
        """Изменение поведение формы при сохранении. Добавляем User и создаем пустой профиль"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        create_model_profile(user)
        return user


# AuthenticationForm Для проверки, пользователь авторизован, существует пользователь в системе или нет и тд
class LoginForm(AuthenticationForm, forms.ModelForm):
    """Форма авторизации"""

    class Meta:
        model = User
        fields = ("username", "password")


class ProfileSettingsForm(forms.ModelForm):
    """Форма для изменение данных профиля"""

    class Meta:
        model = Profile
        fields = ("calories_limit",)


class EatCookForm(forms.ModelForm):
    """Форма употребляемого блюда"""

    cook = forms.ModelChoiceField(
        queryset=get_model_cook__already(), widget=forms.Select(), empty_label="---------", label="Блюдо"
    )

    class Meta:
        model = EatCook
        fields = ("cook", "count_eat", "date")
        widgets = {
            "date": forms.DateTimeInput(attrs={"type": "datetime-local"})
        }


class EatIngredientForm(forms.ModelForm):
    """Форма употребляемого ингредиента"""

    ingredient_item = forms.ModelChoiceField(
        queryset=get_model_ingredient_item__already(), widget=forms.Select(), empty_label="---------", label="Продукт"
    )

    class Meta:
        model = EatIngredient
        fields = ("ingredient_item", "count_eat", 'date')
        widgets = {
            "date": forms.DateTimeInput(attrs={"type": "datetime-local"})
        }
