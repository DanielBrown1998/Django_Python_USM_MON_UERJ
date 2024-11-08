from django.shortcuts import render, redirect
from home.models import Days
from datetime import datetime, timedelta
from django.db.models import Q
from django.core.paginator import Paginator
from home.models import Monitorias, DataUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from home.views import message, monitorias_marcadas_usuario, monitorias_marcadas_monitor, free_days_next_monitorias

@login_required(login_url='home:home')
def monitoria(request):
    user = get_user(request)
    if user.is_superuser:
        contacts = Monitorias.objects.all().order_by('-date')
    else:
        contacts = Monitorias.objects.filter(
            owner=user
        ).order_by('-date')

    data = [
        {
            'matricula': item.owner.username, 
            'nome': f"{item.owner.first_name} {item.owner.last_name}", 
            "data": item.date, 
            "status": item.status,
            "id": item.pk} 
        for item in contacts 
    ]
    paginator = Paginator(data, 10)
    page_number = request.GET.get("page")
    data = paginator.get_page(page_number)
    context = {
        'title': 'Monitoria',
        'data': data,
        'free_days_next_monitorias': free_days_next_monitorias(),
        'monitorias_marcadas': {
                item for item in monitorias_marcadas_monitor()
                } if user.is_superuser else {
                    item for item in monitorias_marcadas_usuario(user)
                }
    }
    url = 'home/monitorias.html'
    return render(request, url, context=context)


@login_required(login_url='home:home')
def update_monitoria(request, id):
    user = get_user(request)

    try:
        monitor = User.objects.get(
            is_superuser = True
        )
        monitoria = Monitorias.objects.get(
            id=id
        )
    except monitoria.DoesNotExists:
        message('Ocorreu um erro!', error=True)
        return redirect("home:monitorias")

    if request.POST:

        today = datetime.now().date()
        date = monitoria.date
        if user.is_superuser:
            if date > today:
                message(request, msg='Monitoria ainda não pode ser atualizada')
                message(request, msg= f"{date} > {today}")
                return redirect("home:monitorias")
        else:
            if today >= date:
                message(request, msg='Você não pode mais cancelar essa monitoria!', error=True)
                return redirect('home:monitorias')
        
        status = request.POST.get('status', 'MARCADA')
        monitoria.status = status
        monitoria.save()
        message(request, msg='Monitoria atualizada com sucesso!', sucesss=True)
        return redirect('home:monitorias')

    monitoria = {
            'monitor_name': f"{monitor.first_name}  {monitor.last_name}", 
            "username": monitoria.owner.username,
            "first_name": monitoria.owner.first_name,
            "last_name": monitoria.owner.last_name,
            "date": monitoria.date,
            "id": monitoria.pk,
            "status": str(monitoria.status).title(),
        }
    
    context = {
        'title': 'Monitoria',
        'monitoria': monitoria,
        "monitorias_marcadas": {
                item for item in monitorias_marcadas_monitor()
                } if user.is_superuser else {
                    item for item in monitorias_marcadas_usuario(user)
                 }
    }
    url = 'home/update_monitoria.html'
    return render(request, url, context=context)
    

@login_required(login_url='home:home')
def marcar_monitoria(request):
    all_weekdays = [
        'Segunda-feira', 
        'Terça-feira', 
        'Quarta-feira', 
        'Quinta-feira', 
        'Sexta-feira', 
        'Sábado', 
        'Domingo'
    ]
    today = datetime.today()
    today_str = datetime.strftime(today, '%Y-%m-%d')
    date = request.POST.get('date')
    if not date:
        message(request, 'Informe uma data')
        return redirect('home:monitorias')
    
    
    date_time = datetime.strptime(date, '%Y-%m-%d')

    if date_time > today + timedelta(days=10) or date_time < today:
        message(request, 'escolha entre os próximos 10 dias que possuem monitoria')
        return redirect('home:monitorias')

    weekday = datetime.weekday(date_time)
    weekdays_possible = Days.objects.all()
    
    weekdays_possible = [
        all_weekdays.index(item.day) 
        for item in weekdays_possible 
        if item.day in all_weekdays
        ]

    if weekday not in weekdays_possible:
        message(request, 'Verifique os dias disponíveis da monitoria')
        return redirect('home:monitorias')

    user = get_user(request)

    try:
        monitoria_user = Monitorias.objects.get(Q(date=date) & Q(owner=user))
    except Monitorias.DoesNotExist:
        monitoria_user = None
    
    if monitoria_user:
        message(request, 'Você já marcou monitoria para este dia')
        return redirect('home:monitorias')
    
    try:
        limit_monitoria = Monitorias.objects.filter(Q(date=date)&Q(status = 'MARCADA'))
    except Monitorias.DoesNotExist:
        limit_monitoria = []

    if len(limit_monitoria) == 5:
        message(request, 'Esse dia já atingiu o máximo de monitorias possíveis')
        return redirect('home:monitorias')

    try:
        data_user = DataUser.objects.get(owner = user)
    except DataUser.DoesNotExist:
        data_user = DataUser(owner=user)
        data_user.save()
    data_user.monitorias_marcadas += 1

    Monitorias.objects.create(
        date=date,
        owner=user,
    )
    data_user.save() 
    
    message(request, 'Monitoria marcada com sucesso', sucesss=True)
    return redirect('home:monitorias')
