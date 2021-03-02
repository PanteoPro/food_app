from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class RegisterUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("username", "password")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-class"

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


# AuthenticationForm Для проверки, пользователь авторизован, существует пользователь в системе или нет и тд
class LoginForm(AuthenticationForm, forms.ModelForm):

    class Meta:
        model = User
        fields = ("username", "password")
