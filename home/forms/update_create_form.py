from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CreateForm(UserCreationForm):

    def __init__(
                self, 
                *args: Any, 
                matricula: Any =None,
                **kwargs: Any, 
                ):
        super(CreateForm, self).__init__(*args, **kwargs)
        if matricula:
            self.fields['username'].initial = matricula
        


    class Meta:
        model = User
        fields = [
            'username',
            'first_name', 
            'last_name', 
            'email',
            ]
        
        
        widgets = {
            'first_name': forms.TextInput(
                attrs = {
                    'class': 'form-cadastro',
                    'required': 'required',
                },
            ),
            'last_name': forms.TextInput(
                attrs = {
                    'class': 'form-cadastro',
                    'required': 'required',
                }
            ),
            'email': forms.EmailInput(
                attrs = {
                    'class': 'form-cadastro',
                    'required': 'required',

                }

            ),
        }
    
    username = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'readonly': 'readonly',
                'class': 'form-cadastro'
            }
        ),
    )

    password1 = forms.CharField(
        label = 'senha',
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-cadastro'
            }
        ),      
        help_text=[
            'Sua senha deve conter pelo menos 8 caracteres',
            'Sua senha não pode ser inteiramente numérica',
            'Sua senha não pode ser comum (óbvia)',

        ]
    )
    
    password2 = forms.CharField(
        label = 'confirma senha',
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-cadastro'
            }
        ),
        help_text=[
            'Digite a mesma senha que foi digitada anteriormente',
        ],
    )


    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name == '':
            self.add_error(
                'first_name',
                ValidationError(
                'primeiro nome não pode ser vazio',
                code = 'invalid',
            ),
        )
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name == '':
            self.add_error(
                'last_name',
                ValidationError(
                'último nome não pode ser vazio',
                code = 'invalid',
            ),
        )
        return last_name


class UpdateForm(forms.ModelForm):

    def __init__(
                self, 
                *args: Any,
                **kwargs: Any, 
                ):
        super(UpdateForm, self).__init__(*args, **kwargs)


    class Meta:
        model = User
        fields = [
            'username',
            'first_name', 
            'last_name', 
            'email',
            ]
        
        
        widgets = {
            'first_name': forms.TextInput(
                attrs = {
                    'class': 'form-cadastro',
                    'required': 'required',
                },
            ),
            'last_name': forms.TextInput(
                attrs = {
                    'class': 'form-cadastro',
                    'required': 'required',
                }
            ),
            'email': forms.EmailInput(
                attrs = {
                    'class': 'form-cadastro',
                    'required': 'required',

                }

            ),
        }
    
    username = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'readonly': 'readonly',
                'class': 'form-cadastro'
            }
        ),
    )

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name == '':
            self.add_error(
                'first_name',
                ValidationError(
                'primeiro nome não pode ser vazio',
                code = 'invalid',
            ),
        )
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name == '':
            self.add_error(
                'last_name',
                ValidationError(
                'último nome não pode ser vazio',
                code = 'invalid',
            ),
        )
        return last_name


class UpdatePassword(forms.ModelForm):

    def __init__(
                self,
                *args: Any,
                **kwargs: Any, 
                ):
        super(UpdatePassword, self).__init__(*args, **kwargs)
    
    class Meta:
        model = User
        fields = [
            'password1',
            'password2',
        ]

    password1 = forms.CharField(
        label = 'senha',
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-cadastro'
            }
        ),      
        help_text=[
            'Sua senha deve conter pelo menos 8 caracteres',
            'Sua senha não pode ser inteiramente numérica',
            'Sua senha não pode ser comum (óbvia)',

        ]
    )
    
    password2 = forms.CharField(
        label = 'confirma senha',
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-cadastro'
            },
        ),
        help_text=[
            'Digite a mesma senha que foi digitada anteriormente',
        ],

    )


    def save(self, commit=True):
        password = self.cleaned_data.get('password1')
        user = super().save(commit=False)
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = self.cleaned_data
        username = self.instance.username
        first_name = self.instance.first_name
        last_name = self.instance.last_name
        email = self.instance.email
        
        password = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if User.objects.get(username=username).check_password(password):
            msg = ValidationError(
                'A senha atual não pode ser igual a nova senha',
                code = 'invalid',
                )
            self.add_error('password1', msg)
        if email in password:
            msg = ValidationError(
                'A senha não pode conter o email',
                code = 'invalid',
                )
            self.add_error('password1', msg)
        if first_name in password:
            msg = ValidationError(
                'A senha não pode conter o primeiro nome',
                code = 'invalid',
                )
            self.add_error('password1', msg)
        if last_name in password:
            msg = ValidationError(
                'A senha não pode conter o último nome',
                code = 'invalid',
                )
            self.add_error('password1', msg)
        if len(password) < 8:
            msg = ValidationError(
                'A senha deve conter pelo menos 8 caracteres',
                code = 'invalid',
                )
            self.add_error('password1', msg)
        if str(password).isnumeric():
            msg = ValidationError(
                'A senha não pode ser inteiramente numérica',
                code = 'invalid',
                )
            self.add_error('password1', msg)
        if password.isalpha():
            msg = ValidationError(
                'A senha não pode ser inteiramente alfabética',
                code = 'invalid',
                )
            self.add_error('password1', msg)
        if password != password2:
            msg = ValidationError(
                'As senhas devem ser congruentes',
                code = 'invalid',
                )
            self.add_error('password1', msg)
            self.add_error('password2', msg)
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        if first_name and last_name:
            if first_name == last_name:
                msg = ValidationError(
                    'primeiro nome não pode ser igual ao último nome',
                    code = 'invalid',
                    )
                self.add_error('first_name', msg)
                self.add_error('last_name', msg)
        else:
            if first_name == '':
                msg = ValidationError(
                    'primeiro nome não pode ser vazio',
                    code = 'invalid',
                    )
                self.add_error('first_name', msg)
            
            if last_name == '':
                msg = ValidationError(
                    'último nome não pode ser vazio',
                    code = 'invalid',
                    )
                self.add_error('last_name', msg)
        return super().clean()
    
    
