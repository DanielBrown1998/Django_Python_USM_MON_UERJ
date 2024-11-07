from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from home.models import DataUser, Horas, Days
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from home.views.index import message
from home.views.index import daysweek

@login_required(login_url="home:home")
def update_hours(request):
    day = request.POST.get('daysweek', '').strip()
    time_start = request.POST.get('time_start', '').strip()
    time_end = request.POST.get('time_end', '').strip()
    if not day or not time_start or not time_end:
        message(request, 'Preencha todos os campos', error=True)
        return redirect('home:config')
    try:
        day = Days.objects.get(day=day)
    except Days.DoesNotExist:
        message(request, 'Dia não encontrado', error=True)
        return redirect('home:config')
    try:
        horas = Horas.objects.filter(
        day__day=day
        )
        for hora in horas:
            hora.delete()
    except Horas.DoesNotExist:
        ...
        
    horas_start = Horas(
        day=day,
        time=time_start
    )
    horas_start.save()
    horas_final = Horas(
        day=day,
        time=time_end
    )
    horas_final.save()
    return redirect('home:config')

@login_required(login_url="home:home")
def update_days(request):
    days = request.POST
    dias_cadastrados = Days.objects.all()
    dias_cadastrados.delete()
    time_start = request.POST.get('time_start', '07:00:00').strip()
    time_end = request.POST.get('time_end', '12:00:00').strip()
    for key, value in days.items():
        if key == 'csrfmiddlewaretoken':
            continue
        day = Days(day=value)
        day.save()
        horas_start = Horas(
            day=day,
            time=time_start
        )
        horas_start.save()
        horas_final = Horas(
            day=day,
            time=time_end
        )
        horas_final.save()
    return redirect('home:config')

@login_required(login_url="home:home") 
def update_monitorias(request):

    usuario = request.POST.get('username', '').strip()
    monitorias_presentes = request.POST.get('monitorias_presentes', '').strip()
    monitorias = DataUser.objects.get(owner__username=usuario)
    if monitorias.monitorias_marcadas >= int(monitorias_presentes):
        monitorias.monitorias_presentes = int(monitorias_presentes)
        monitorias.save()
        message(request, f'aluno {usuario} atualizado com sucesso', sucesss=True)
    else:
        message(request, f'Erro ao atualizar aluno {usuario}', error=True)
        #envie uma mensagem de erro
    return redirect('home:config')

@login_required(login_url="home:home") 
def search_config(request):

    search_value = str(request.GET.get('q', '')).strip()
    if not search_value:
        redirect('home:config')

    data_user = DataUser.objects.filter(
        Q(owner__username__icontains=search_value) |
        Q(owner__first_name__icontains=search_value) |
        Q(owner__last_name__icontains=search_value)
    )
    days = Days.objects.all()
    horas = Horas.objects.all().order_by('day')
    data = [{
        "usuario": user.owner, 
        "monitorias_presentes": user.monitorias_presentes, 
        "monitorias_marcadas": user.monitorias_marcadas} 
        for user in data_user
        ]
    hr = [
        {"time": h.time, "day": h.day.day} 
        for h in horas
        ]
    pagination = Paginator(data, 10)
    page_number = request.GET.get("page")
    data = pagination.get_page(page_number)
    context = {
        'title': f'Configurações-{search_value}',
        'data': data,
        'search': search_value,
        'daysweek': daysweek,
        'days': [str(dia).strip() for dia in days],
        'horas': hr,
    }
    url = 'home/config.html'
    return render(request, url, context=context)

@login_required(login_url="home:home") 
def config(request):

    data_user = DataUser.objects.all()
    days = Days.objects.all()

    horas = Horas.objects.all().order_by('day')
    data = [{
        "usuario": user.owner, 
        "monitorias_presentes": user.monitorias_presentes, 
        "monitorias_marcadas": user.monitorias_marcadas} 
        for user in data_user
        ]
    hr = [{"time": h.time, "day": h.day.day} for h in horas]

    pagination = Paginator(data, 10)
    page_number = request.GET.get("page")
    data = pagination.get_page(page_number)

    context = {
        'title': 'Configurações',
        'data': data,
        'daysweek': daysweek,
        'days': [str(dia).strip() for dia in days],
        'horas': hr,
    }
    
    url = 'home/config.html'
    return render(request, url, context=context)
