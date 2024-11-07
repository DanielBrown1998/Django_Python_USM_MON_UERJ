from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from home.models import User
from datetime import datetime
from django.db.models import Q
from django.core.paginator import Paginator

def dados(request):

    context = {
        'title': 'Estatísticas',
        'data': [],
    }
    url = 'home/data.html'
    return render(request, url, context=context)
