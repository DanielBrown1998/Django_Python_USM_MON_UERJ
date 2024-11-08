from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from home.views.index import free_days_next_monitorias, monitorias_marcadas_monitor, monitorias_marcadas_usuario


@login_required(login_url='home:home')
def search_monitoria(request):
    from home.models import Monitorias
    user = get_user(request)
    num_items = request.GET.get('num_items', 10)
    order_items = request.GET.get('order_items', 'date')
    search_value = request.GET.get('q', '').strip()
    
    if search_value == '' and num_items == '10' and order_items == 'date':
        return redirect('home:monitorias')
    
    if search_value == 'hoje':
        search_value = datetime.now()
        search_value = datetime.strftime(search_value, "%Y-%m-%d")
    
    elif search_value == 'amanha':
        search_value = (datetime.now() + timedelta(days=1))
        search_value = datetime.strftime(search_value, "%Y-%m-%d")
    
    elif search_value == 'ontem':
        search_value = (datetime.now() - timedelta(days=1))
        search_value = datetime.strftime(search_value, "%Y-%m-%d")
    
    if order_items != 'date' and order_items is not None:
        contacts = Monitorias.objects\
            .filter(
                Q(owner__username__icontains=search_value) | 
                Q(owner__first_name__icontains=search_value) |
                Q(owner__last_name__icontains=search_value) |
                Q(date__icontains=search_value)
                )\
            .order_by(f'owner__{order_items}')
    else:
        contacts = Monitorias.objects\
            .filter(
                Q(owner__username__icontains=search_value) | 
                Q(owner__first_name__icontains=search_value) |
                Q(owner__last_name__icontains=search_value) | 
                Q(date__icontains=search_value)
                )\
            .order_by('-date')


    data = [
        {
            'matricula': item.owner.username, 
            'nome': f"{item.owner.first_name} {item.owner.last_name}", 
            "data": item.date,
            "status": item.status,
            "id": item.pk
        }
        for item in contacts 
    ]
    pagination = Paginator(data, int(num_items))
    page_number = request.GET.get("page")
    data = pagination.get_page(page_number)
    
    context = {
        'title': 'Monitoria',
        'data': data,
        'search': search_value,
        'free_days_next_monitorias': free_days_next_monitorias(),
        "monitorias_marcadas": {
                item for item in monitorias_marcadas_monitor()
                } if user.is_superuser else {
                    item for item in monitorias_marcadas_usuario(user)
                }
        }
    url = 'home/monitorias.html'
    return render(request, url, context=context)
    