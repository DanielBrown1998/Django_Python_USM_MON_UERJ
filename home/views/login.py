from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from home.forms.login import Login
from home.forms.update_create_form import CreateForm
from django.contrib.auth.models import User
from django.db.models import Q
from home.models import Matriculas
from home.views import days, message
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth 
from django.contrib.auth.decorators import login_required

def login(request):
    
    matricula = str(request.POST.get('matricula', '')).strip()
    password = request.POST.get('password', '')
    if password:
        form_auth = AuthenticationForm(
            request, data=request.POST)
        form = Login(
            matricula,
            request.POST
        )
        if form_auth.is_valid():
            user = form_auth.get_user()
            auth.login(request, user)
            message(request, 'Login realizado', sucesss=True)
            context = {
            'title': 'Home',
            'horarios': days(),
            'form': form,
            }
            url = 'home/index.html'
            return render(request, url, context=context)
        
        message(request, 'Login inválido, seu usuário pode estar inativo', error=True)
        context = {
            'title': 'login',
            'horarios': days(),
            'form': form,
        }
        url = 'home/login.html'
        return render(request, url, context=context)

    if len(matricula) != 12:
        message(request, 'Matrícula inválida', error=True)
        return redirect('home:home')

    if matricula:

        try:
            matriculas_cadastradas = Matriculas.objects.get(matricula = matricula)
        except Matriculas.DoesNotExist:
            matriculas_cadastradas = None
        
        try:
            user = User.objects.get(username= matricula)
        except User.DoesNotExist:
            user = None
        
        if not matriculas_cadastradas:
            msg ='Não foi possível encontrar sua matrícula'
            message(request, msg, error=True)
            return redirect('home:home')
        
        if not user:
            msg = 'não foi possível encontrar seu usuário, cadastre-se!!!'
            message(request, msg)                
            form = CreateForm(
                matricula = matricula
            )
            context = {
                'title': 'Cadastro',
                'form': form
            }
            url = 'home/cadastro.html'
            return render(request, url, context)
    
    msg = 'usuário encontrado!'
    message(request, msg, sucesss=True)
    context = {
        'title': 'login',
        'username': matricula,
        'horarios': days(),
        'form': Login(
            matricula
            )
        }
    url = 'home/login.html'
    return render(request, url, context=context)

@login_required(login_url="home:home")
def logout(request):
    auth.logout(request)
    message(request, 'Logout realizado', sucesss=True)
    return redirect('home:home')

