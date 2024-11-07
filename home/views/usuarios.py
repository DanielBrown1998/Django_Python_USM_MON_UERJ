from django.shortcuts import render, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required(login_url="home:home")
def update_usuarios(request):
    user_ = request.POST.get('username', '')
    user = User.objects.get(username=user_)
    super_user = request.POST.get('is_superuser', '')
    is_staff = request.POST.get('is_staff', '')
    delete = request.POST.get('delete', '')
    active = request.POST.get('is_active', '')


    if delete:
        user.delete()
        return redirect('home:search_usuarios')
    
    if active:
        if not user.is_active:
            user.is_active = True
    else:
        user.is_active = False

    if super_user:
        if not user.is_superuser:
            user.is_superuser = True
    else:
        user.is_superuser = False
    
    if is_staff:
        if not user.is_staff:
            user.is_staff = True
    else:
        user.is_staff = False

    user.save()
    
    return redirect('home:search_usuarios')

@login_required(login_url="home:home")
def search_usuarios(request):
    search_value = str(request.GET.get('q', '')).strip()
    if not search_value:
        return redirect('home:usuarios')
    users = User.objects.filter(
        Q(username__icontains=search_value) |
        Q(first_name__icontains=search_value) |
        Q(last_name__icontains=search_value)
    )
    pagination = Paginator(users, 10)
    page_number = request.GET.get('page')
    users = pagination.get_page(page_number)
    
    context = {
        'title': 'Usuários',
        'search': search_value,
        'data': users,
    }

    url = 'home/usuarios.html'
    return render(request, url, context=context)


@login_required(login_url="home:home")
def usuarios(request):
    users = User.objects.all().order_by('username')
    pagination = Paginator(users, 10)
    page_number = request.GET.get('page')
    users = pagination.get_page(page_number)
    
    context = {
        'title': 'Usuários',
        'data': users,
    }

    url = 'home/usuarios.html'
    return render(request, url, context=context)
