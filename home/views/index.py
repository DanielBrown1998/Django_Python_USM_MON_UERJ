from django.shortcuts import render
from home.models import Monitorias, Horas
from django.db.models import Q
from itertools import groupby
daysweek = [
    'Segunda-feira',
    'Terça-feira',
    'Quarta-feira',
    'Quinta-feira',
    'Sexta-feira',
]

def monitorias_marcadas_usuario(user):
    import datetime
    from datetime import timedelta, datetime
    data = Monitorias.objects.filter(
        Q(owner=user) & 
        Q(status__icontains='Marcada') &
        Q(date__range=(
            datetime.now(), 
            datetime.now() + timedelta(days=7)
            )
        )
    )
    return data

def monitorias_marcadas_monitor():
    import datetime
    from datetime import datetime 
    data = Monitorias.objects.filter(
        Q(date__range=(datetime.now(), datetime.now())) &
        Q(status__icontains='Marcada')
    )
    return data

def free_days_next_monitorias():
    import datetime
    from datetime import datetime, timedelta
    data = Monitorias.objects.filter(
        Q(date__range=(datetime.now() + timedelta(1), datetime.now() + timedelta(days=7))) &
        Q(status__icontains='Marcada')

        )
    monitorias = groupby(sorted([
        {'date': item.date, 'user': item.owner.username} for item in data], key=lambda date: date['date']
        ), key=lambda date: date['date'])
    
    days_monitoria = [daysweek.index(day['dayweek']) for day in days()]
    monitorias = [item[0] for item in monitorias 
                  if len(list(item[1])) < 5 
                  and item[0].weekday() in days_monitoria
                  ]
    return monitorias
    
def message(request, msg: str, sucesss=False, error=False):
    from django.contrib import messages
    if sucesss:
        return messages.success(request, msg)
    if error:
        return messages.error(request, msg)

    return messages.warning(request=request, message=msg)

def days():
    horarios = Horas.objects.all()
    weekday = {}
    data = [{"hora": item.time, 'day': item.day.day} for item in horarios]
    for item in data:
        if item['day'] not in weekday.keys():
            weekday[item['day']] = [item['hora']]
            continue
        weekday[item['day']].append(item['hora'])
    data = [{"dayweek": key, "time_start": str(value[0]), "time_final": str(value[-1])} for key, value in weekday.items()]
    return data

def index(request):

    context = {
        'title': 'HOME',
        'horarios': days(),
    }
    url = 'home/index.html'
    return render(request, url, context=context)
