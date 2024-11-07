from home.models import User
from django import forms
from django.core.exceptions import ValidationError


class Login(forms.Form):


    def __init__(self, matricula, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['username'].initial = matricula

    username = forms.CharField(
        required= True,
        widget = forms.TextInput(
            attrs = {
                'name': 'matricula',
                'class': 'form',
                'readonly': 'readonly',
            }
        )
    )

    password = forms.CharField(
        required= True,
        widget = forms.PasswordInput(
            attrs = {
                'name': 'password',
                'class': 'form',
                'placeholder': 'Senha',
            }
        )
    )

    def clean(self):
        cleaned_data = self.cleaned_data
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = User.objects.get(username=username)
        if not user.check_password(password):
            self.add_error(
                'password',
                ValidationError(
                    'Login ou Senha incorretos', code='invalid'
                    )
            )
        return super().clean()

