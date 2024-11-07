from django.shortcuts import render
from home.models import Monitorias
from django.db.models import Q

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
        Q(date__range=(datetime.now(), datetime.now() + timedelta(days=7)))
    )
    return data

def monitorias_marcadas_monitor():
    import datetime
    from datetime import timedelta, datetime 
    data = Monitorias.objects.filter(
        date__range=(datetime.now(), datetime.now())
    )
    return data

def message(request, msg: str, sucesss=False, error=False):
    from django.contrib import messages
    if sucesss:
        return messages.success(request, msg)
    if error:
        return messages.error(request, msg)

    return messages.warning(request=request, message=msg)

def days():
    from home.models import Horas
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
